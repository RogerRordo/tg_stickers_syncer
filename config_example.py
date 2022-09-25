# Usage:
#   1. Copy this file to config.py
#   2. Modify the content of the file according to your needs

from .src import RunConfig

config = RunConfig(
    # If set true, stickers will be updated though their hashes unchanged
    force_run=False,

    # The name of your Github repo that storing stickers
    github_repo_name='tg_stickers',

    # The client of your Telegram client
    tg_client_name='rordo',

    # Proxy used only for Telegram connections
    # tg_proxy_schema='socks5',
    # tg_proxy_host='127.0.0.1',
    # tg_proxy_port=20170,
)
