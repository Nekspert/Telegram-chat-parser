from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    api_id: str
    api_hash: str
    admin_ids: list[int]


@dataclass
class DataBase:
    name_db: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            api_id=env('API_ID'),
            api_hash=env('API_HASH'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DataBase(
            name_db=env('NAME_DB')
        )
    )
