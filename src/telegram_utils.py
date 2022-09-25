import logging
from typing import Dict, List, Optional, Tuple

from pyrogram import Client
from pyrogram.file_id import FileId, FileType
from pyrogram.raw.functions.messages import GetAllStickers, GetStickerSet
from pyrogram.raw.types.messages import AllStickers, AllStickersNotModified, StickerSet as MsgStickerSet
from pyrogram.raw.base.sticker_pack import StickerPack as StickerPackBase
from pyrogram.raw.types import StickerSet, StickerPack, InputStickerSetID, Document


def get_tg_client(client_name: str, api_id: int, api_hash: str,
                  proxy_schema: Optional[str], proxy_host: Optional[str],
                  proxy_port: Optional[int]) -> Client:
    """Get a Telegram client instance

    Args:
        client_name (str): Telegram client name.
        api_id (int): Telegram API ID.
        api_hash (str): Telegram API Hash.
        proxy_schema (Optional[str]): The protocol of the proxy.
        proxy_host (Optional[str]): The proxy host.
        proxy_port (Optional[int]): The proxy port.

    Returns:
        Client: The telegram client instance.
    """
    params = {
        'session_name': client_name,
        'api_id': api_id,
        'api_hash': api_hash,
    }
    if proxy_schema or proxy_host or proxy_port:
        if proxy_schema and proxy_host and proxy_port:
            params.update({
                'proxy': {
                    "scheme": proxy_schema,
                    'hostname': proxy_host,
                    'port': proxy_port,
                },
            })
        else:
            logging.warning(
                'Proxy params are incomplete, connect without proxy.')
    return Client(**params)


def get_all_msg_sticker_sets(tg_client: Client,
                             all_stickers_hash: int,
                             skip_archived: bool = True
                             ) -> Tuple[Dict[int, MsgStickerSet], int]:
    """Get a dict mapping sticker set ID to MsgStickerSet with hash checked

    Args:
        tg_client (Client): The Telegram client instance.
        all_stickers_hash (int): Old hash of AllStickers.
            If it does not change, empty dict and the origin hash will be returned.
        skip_archived (bool, optional): Whether to skip archived sticker sets. Defaults to True.

    Returns:
        Dict[int, MsgStickerSet]: A dict mapping sticker set ID to MsgStickerSet.
        int: The hash of the AllStickers result.
    """
    msg_sticker_sets: Dict[int, MsgStickerSet] = {}
    all_stickers = tg_client.send(GetAllStickers(hash=all_stickers_hash))
    if isinstance(all_stickers, AllStickersNotModified):
        logging.debug('All stickers unchanged.')
        return msg_sticker_sets, all_stickers_hash
    assert isinstance(all_stickers, AllStickers)
    for sticker_set in all_stickers.sets or []:
        assert isinstance(sticker_set, StickerSet)
        if skip_archived and sticker_set.archived:
            continue
        msg_sticker_sets[sticker_set.id] = tg_client.send(
            GetStickerSet(
                stickerset=InputStickerSetID(
                    id=sticker_set.id,
                    access_hash=sticker_set.access_hash,
                ),
                hash=0,
            ))
        assert isinstance(msg_sticker_sets[sticker_set.id], MsgStickerSet)
    return msg_sticker_sets, all_stickers.hash


def get_sticker_doc_id_to_emoticon(
        sticker_packs: List[StickerPackBase]) -> Dict[int, str]:
    """Get a dict mapping sticker document id to emoticon

    Args:
        sticker_packs (List[StickerPackBase]): List of StickerPackBase.

    Returns:
        Dict[int, str]: The dict mapping sticker document id to emoticon.
    """
    sticker_doc_id_to_emoticon: Dict[int, str] = {}
    for sticker_pack in sticker_packs:
        assert isinstance(sticker_pack, StickerPack)
        for doc_id in sticker_pack.documents:
            sticker_doc_id_to_emoticon[doc_id] = sticker_pack.emoticon
    return sticker_doc_id_to_emoticon


def get_sticker_document_file_id(document: Document, sticker_set_id: int,
                                 sticker_set_access_hash: str) -> str:
    """Get file id of sticker document file

    Args:
        document (Document): The sticker document.
        sticker_set_id (int): The sticker set ID.
        sticker_set_access_hash (str): The access hash of the sticker set.

    Returns:
        str: The file ID of the sticker
    """
    file_id = FileId(
        file_type=FileType.STICKER,
        dc_id=document.dc_id,
        file_reference=document.file_reference,
        media_id=document.id,
        access_hash=document.access_hash,
        sticker_set_id=sticker_set_id,
        sticker_set_access_hash=sticker_set_access_hash,
    ).encode()
    return file_id
