import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Set

from google.protobuf import text_format
from github.Repository import Repository
from pyrogram import Client
from pyrogram.raw.types import StickerSet, Document, DocumentEmpty, DocumentAttributeFilename
from pytz import utc, timezone

from .errors import NoFileNameAttrForDocError
from .run_config import RunConfig
from .gif_utils import convert_sticker_to_gif
from .github_utils import (
    create_branch_from_master,
    delete_branch,
    delete_file,
    get_cdn_github_url,
    get_file_content,
    get_github_repo,
    merge_branch_to_master,
    create_file,
)
from .telegram_utils import (
    get_all_msg_sticker_sets,
    get_sticker_doc_id_to_emoticon,
    get_sticker_document_file_id,
    get_tg_client,
)
from .proto.generated.dir_struct_pb2 import (
    DirStruct as DirStructPb,
    StickerSet as StickerSetPb,
)


def _get_utc() -> str:
    return int(datetime.now().strftime('%s'))


def _init_tmp_dir(tmp_dir: Path):
    tmp_dir.mkdir(parents=True, exist_ok=True)
    (tmp_dir / 'src').mkdir(parents=True, exist_ok=True)
    (tmp_dir / 'dest').mkdir(parents=True, exist_ok=True)


def _generate_branch_name() -> str:
    branch_name = 'auto_commit_{}'.format(_get_utc())
    return branch_name


def _clear_sticker_set(
        github_repo: Repository, branch_name: str, remote_gif_dir_path: Path,
        remote_collection_dir_path: Path, sticker_set_pb: StickerSetPb):
    # Delete collection readme
    rel_path = remote_collection_dir_path / '{}.md'.format(
        sticker_set_pb.short_name)
    delete_file(
        repo=github_repo,
        rel_path=rel_path,
        commit_message='Delete {}'.format(rel_path),
        branch_name=branch_name,
        should_check_exist=False,
    )

    # Delete gif files
    for file_id in sticker_set_pb.sticker:
        rel_path = remote_gif_dir_path / '{}.gif'.format(file_id)
        delete_file(
            repo=github_repo,
            rel_path=rel_path,
            commit_message='Delete {}'.format(rel_path),
            branch_name=branch_name,
            should_check_exist=False,
        )


def _generate_collection_readme_content(github_repo: Repository,
                                        sticker_set_pb: StickerSetPb,
                                        remote_gif_dir_path: Path,
                                        timezone_str: str,
                                        with_title: bool = True) -> str:
    content = '# {}\n\n'.format(sticker_set_pb.title) if with_title else ''
    update_date_time_str = \
        datetime.utcfromtimestamp(sticker_set_pb.update_timestamp) \
        .replace(tzinfo=utc) \
        .astimezone(tz=timezone(timezone_str)) \
        .strftime('%Y%m%d %H:%M')
    content += 'Last updated: {}\n\n'.format(update_date_time_str)
    content += 'https://t.me/addstickers/{}\n\n'.format(
        sticker_set_pb.short_name)
    for sticker in sticker_set_pb.sticker.values():
        rel_path = remote_gif_dir_path / '{}.gif'.format(sticker.file_id)
        gif_url = get_cdn_github_url(github_repo, rel_path)
        content += '![{}]({})\n'.format(sticker.file_id, gif_url)
    content += '\n'
    return content


def _generate_root_readme_content(
        github_repo: Repository, dir_struct: DirStructPb,
        remote_gif_dir_path: Path, remote_collection_dir_path: Path,
        skip_sticker_sets: Set[int], timezone_str: str) -> str:
    content = '# TG Stickers\n\n'
    sticker_set_pbs = sorted(
        dir_struct.sticker_set.values(),
        key=lambda sticker_set: sticker_set.update_timestamp or 0,
        reverse=True)

    # Generate added/updated content
    for sticker_set_pb in sticker_set_pbs:
        if sticker_set_pb.id in skip_sticker_sets:
            continue
        collection_url = get_cdn_github_url(
            github_repo, remote_collection_dir_path / '{}.md'.format(
                sticker_set_pb.short_name))
        content += '## [{}]({})\n\n'.format(sticker_set_pb.title,
                                            collection_url)
        content += _generate_collection_readme_content(
            github_repo,
            sticker_set_pb,
            remote_gif_dir_path,
            timezone_str,
            with_title=False)

    # Generate skipped content
    content += '## MORE OLDER\n\n'
    for sticker_set_pb in sticker_set_pbs:
        if sticker_set_pb.id not in skip_sticker_sets:
            continue
        collection_readme_path = remote_collection_dir_path / '{}.md'.format(
            sticker_set_pb.short_name)
        content += '- [{}]({})\n'.format(sticker_set_pb.title,
                                         collection_readme_path)
    content += '\n'
    return content


def _get_document_extension(document: Document) -> str:
    for attr in document.attributes:
        if isinstance(attr, DocumentAttributeFilename):
            return Path(attr.file_name).suffix
    raise NoFileNameAttrForDocError


def _process_sticker(sticker_document: Document, sticker_set_id: int,
                     sticker_set_access_hash: str,
                     sticker_doc_id_to_emoticon: Dict[int, str],
                     sticker_set_pb: StickerSetPb, src_dir_path: Path,
                     dest_dir_path: Path, remote_gif_dir_path: Path,
                     tg_client: Client, github_repo: Repository,
                     branch_name: str, log_prefix: str, gif_size_limit: int):
    file_id = get_sticker_document_file_id(sticker_document, sticker_set_id,
                                           sticker_set_access_hash)
    extension = _get_document_extension(sticker_document)
    logging.info(log_prefix + 'File ID = {}'.format(file_id))

    # Download
    src_file_path = src_dir_path / '{}{}'.format(file_id, extension)
    tg_client.download_media(message=file_id, file_name=src_file_path)
    logging.info(log_prefix + 'Downloaded to {}'.format(src_file_path))

    # Convert
    dest_file_path = dest_dir_path / '{}.gif'.format(file_id)
    convert_sticker_to_gif(
        src_file_path, dest_file_path, gif_size_limit=gif_size_limit)
    logging.info(log_prefix + 'Converted to {}'.format(dest_file_path))

    # Upload
    rel_path = remote_gif_dir_path / '{}.gif'.format(file_id)
    create_file(
        repo=github_repo,
        rel_path=rel_path,
        content=dest_file_path.read_bytes(),
        commit_message='Upload {}'.format(rel_path),
        branch_name=branch_name,
        should_check_exist=False,
    )
    logging.info(log_prefix + 'Uploaded to {}'.format(dest_file_path))

    sticker_pb = sticker_set_pb.sticker[file_id]
    sticker_pb.file_id = file_id
    sticker_pb.doc_id = sticker_document.id
    sticker_pb.emoticon = sticker_doc_id_to_emoticon.get(sticker_document.id)
    sticker_pb.original_size = src_file_path.stat().st_size
    sticker_pb.gif_size = dest_file_path.stat().st_size
    sticker_pb.extension = extension
    logging.info(log_prefix + 'Finish processing.')


def _with_resources(tmp_dir: Path, github_repo: Repository, branch_name: str,
                    tg_client: Client, config: RunConfig):
    remote_gif_dir_path = Path(config.github_gif_dir)
    remote_collection_dir_path = Path(config.github_collection_dir)
    remote_dir_struct_path = Path(config.github_dir_struct_file)
    remote_root_readme_path = Path(config.github_root_readme_file)
    skip_sticker_sets = set()

    # Init dir struct
    old_dir_struct = DirStructPb()
    if not config.force_run:
        old_dir_struct_str = get_file_content(github_repo, branch_name,
                                              remote_dir_struct_path)
        text_format.Parse(old_dir_struct_str, old_dir_struct)
    old_sticker_set_hashes = {
        sticker_set_id: (sticker_set.hash or 0)
        if sticker_set is not None else 0
        for sticker_set_id, sticker_set in dict(old_dir_struct.sticker_set)
        .items()
    }
    dir_struct = DirStructPb()

    # Get all stickers
    old_dir_struct_hash = (old_dir_struct.hash
                           or 0) if not config.force_run else 0
    msg_sticker_sets, dir_struct.hash = get_all_msg_sticker_sets(
        tg_client, old_dir_struct_hash)
    if dir_struct.hash == old_dir_struct_hash:
        logging.info('All stickers unchanged, skip running.')
        return
    msg_sticker_sets_cnt = len(msg_sticker_sets)
    logging.info('Found {} sticker sets.'.format(msg_sticker_sets_cnt))

    # Create/update sticker sets
    for sticker_set_index, msg_sticker_set in enumerate(
            msg_sticker_sets.values()):
        sticker_set = msg_sticker_set.set
        assert isinstance(sticker_set, StickerSet)
        sticker_set_log_prefix = 'Sticker set {} [{}/{}]: '.format(
            sticker_set.short_name, sticker_set_index + 1,
            msg_sticker_sets_cnt)
        sticker_set_pb = dir_struct.sticker_set[sticker_set.id]
        if sticker_set.id in old_sticker_set_hashes:
            if not config.force_run and \
                old_sticker_set_hashes[sticker_set.id] == sticker_set.hash:
                logging.info(
                    sticker_set_log_prefix + 'Sticker set unchanged, skip.')
                sticker_set_pb.CopyFrom(
                    old_dir_struct.sticker_set[sticker_set.id])
                skip_sticker_sets.add(sticker_set.id)
                continue
            logging.info(
                sticker_set_log_prefix + 'Sticker set changed, will update.')
            _clear_sticker_set(github_repo, branch_name, remote_gif_dir_path,
                               remote_collection_dir_path,
                               old_dir_struct.sticker_set[sticker_set.id])

        sticker_set_pb.id = sticker_set.id
        sticker_set_pb.hash = sticker_set.hash
        sticker_set_pb.short_name = sticker_set.short_name
        sticker_set_pb.title = sticker_set.title
        sticker_set_pb.update_timestamp = _get_utc()

        sticker_documents = msg_sticker_set.documents
        sticker_doc_id_to_emoticon = get_sticker_doc_id_to_emoticon(
            msg_sticker_set.packs)
        sticker_cnt = len(sticker_documents)
        logging.info(
            sticker_set_log_prefix + 'Found {} stickers.'.format(sticker_cnt))
        for sticker_index, sticker_document in enumerate(sticker_documents):
            sticker_log_prefix = 'Sticker set {} [{}/{}], Sticker [{}/{}]: '.format(
                sticker_set.short_name, sticker_set_index + 1,
                msg_sticker_sets_cnt, sticker_index + 1, sticker_cnt)
            if isinstance(sticker_document, DocumentEmpty):
                logging.warning(sticker_log_prefix + 'Empty document, skip.')
                continue
            assert isinstance(sticker_document, Document)
            _process_sticker(
                sticker_document=sticker_document,
                sticker_set_id=sticker_set.id,
                sticker_set_access_hash=sticker_set.access_hash,
                sticker_doc_id_to_emoticon=sticker_doc_id_to_emoticon,
                sticker_set_pb=sticker_set_pb,
                src_dir_path=tmp_dir / 'src',
                dest_dir_path=tmp_dir / 'dest',
                remote_gif_dir_path=remote_gif_dir_path,
                tg_client=tg_client,
                github_repo=github_repo,
                branch_name=branch_name,
                log_prefix=sticker_log_prefix,
                gif_size_limit=config.gif_size_limit)

        # Generate collection readme
        collection_readme_content = _generate_collection_readme_content(
            github_repo, sticker_set_pb, remote_gif_dir_path, config.timezone)
        delete_file(
            repo=github_repo,
            rel_path=remote_collection_dir_path / '{}.md'.format(
                sticker_set.short_name),
            commit_message='Update collection readme (pre-delete)',
            branch_name=branch_name,
            should_check_exist=True,
        )
        create_file(
            repo=github_repo,
            rel_path=remote_collection_dir_path / '{}.md'.format(
                sticker_set.short_name),
            content=collection_readme_content,
            commit_message='Update collection readme',
            branch_name=branch_name,
            should_check_exist=False,
        )
        logging.info(sticker_set_log_prefix + 'Updated collection readme.')

    # Remove old sticker sets
    for sticker_set_id, sticker_set in old_dir_struct.sticker_set.items():
        if sticker_set_id in dir_struct.sticker_set:
            continue
        _clear_sticker_set(github_repo, branch_name, remote_gif_dir_path,
                           remote_collection_dir_path,
                           old_dir_struct.sticker_set[sticker_set_id])
        logging.info('Removed sticker set {}.'.format(sticker_set.short_name))

    # Generate new root readme
    root_readme_content = _generate_root_readme_content(
        github_repo, dir_struct, remote_gif_dir_path,
        remote_collection_dir_path, skip_sticker_sets, config.timezone)
    delete_file(
        repo=github_repo,
        rel_path=remote_root_readme_path,
        commit_message='Update root readme (pre-delete)',
        branch_name=branch_name,
        should_check_exist=True,
    )
    create_file(
        repo=github_repo,
        rel_path=remote_root_readme_path,
        content=root_readme_content,
        commit_message='Update root readme',
        branch_name=branch_name,
        should_check_exist=False,
    )
    logging.info('Updated root readme.')

    # Upload new dir struct
    delete_file(
        repo=github_repo,
        rel_path=remote_dir_struct_path,
        commit_message='Update dir struct (pre-delete)',
        branch_name=branch_name,
        should_check_exist=True,
    )
    create_file(
        repo=github_repo,
        rel_path=remote_dir_struct_path,
        content=text_format.MessageToString(dir_struct),
        commit_message='Update dir struct',
        branch_name=branch_name,
        should_check_exist=False,
    )
    logging.info('Updated dir struct.')

    # Merge to master
    pr_url = merge_branch_to_master(
        github_repo,
        branch_name,
        commit_message='Auto commit {}'.format(
            datetime.now().strftime('%Y%m%d')))
    logging.info('Merged {} to master: {}'.format(branch_name, pr_url))


def _run(config: RunConfig):
    # Init tmp dir
    tmp_dir = Path(config.tmp_dir)
    _init_tmp_dir(tmp_dir)

    # Init github
    github_repo = get_github_repo(config.github_token, config.github_repo_name)

    # Init tg client
    with get_tg_client(
            client_name=config.tg_client_name,
            api_id=config.tg_api_id,
            api_hash=config.tg_api_hash,
            proxy_schema=config.tg_proxy_schema,
            proxy_host=config.tg_proxy_host,
            proxy_port=config.tg_proxy_port,
    ) as tg_client:
        # Init github branch
        branch_name = _generate_branch_name()
        create_branch_from_master(github_repo, branch_name)
        logging.info('Created new branch: {}'.format(branch_name))

        try:
            _with_resources(tmp_dir, github_repo, branch_name, tg_client,
                            config)
        except Exception as e:
            if delete_branch(github_repo, branch_name):
                logging.info('Deleted branch {}.'.format(branch_name))
            raise e
        else:
            if delete_branch(github_repo, branch_name):
                logging.info('Deleted branch {}.'.format(branch_name))


class Runner():
    config: RunConfig = RunConfig()

    def __init__(self, config: RunConfig):
        self.config = config

    def run(self):
        logging.info('Start running...')
        _run(self.config)
        logging.info('Finish running.')
