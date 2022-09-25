from dataclasses import dataclass
from typing import Optional


@dataclass
class RunConfig():
    tmp_dir: str = '/tmp/tg_sticker_to_wechat'
    force_run: bool = False
    timezone = 'Asia/Shanghai'

    # Github configs
    github_token: str = ''
    github_repo_name: str = ''
    github_auto_upload_msg: str = 'Auto Upload'
    github_dir_struct_file: str = 'dir_struct.proto.txt'
    github_root_readme_file: str = 'README.md'
    github_gif_dir: str = 'gifs'
    github_collection_dir: str = 'collections'

    # Telegram configs
    tg_client_name: str = ''
    tg_api_id: int = 2525119
    tg_api_hash: str = '6437414729a9e59131e8a8fc67da1e9f'
    tg_proxy_schema: Optional[str] = None
    tg_proxy_host: Optional[str] = None
    tg_proxy_port: Optional[int] = None

    # GIF configs
    gif_size_limit: int = 1 * 1024 * 1024
