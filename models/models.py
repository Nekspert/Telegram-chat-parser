from .methods import DataBase
from config_data.config import (Config, load_config)

config: Config = load_config()
db = DataBase(
    name_db=config.db.name_db
)
