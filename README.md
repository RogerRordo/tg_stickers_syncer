# tg_stickers_syncer

A python script for syncing stickers from Telegram to a Github repo

## Usage

1. `pip3 install -r requirements.txt`
2. 创建一个空白 Github Repo 用于存放同步的 TG 表情
3. 根据[该 Github Doc](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)获取一个 Token，其至少包含 repo 的所有权限
4. 将 [`secret_example.py`](./secret_example.py) 复制为 `secret.py`，并将上一步获得的 Token 填入 `TOKEN` 中
5. 将 [`config_example.py`](./config_example.py) 复制为 `config.py`，并按需配置，如 TG 代理等信息
6. `python3 run.py`。首次使用需要根据提示登录 TG

## An example

https://github.com/RogerRordo/tg_stickers
