from dataclasses import dataclass
from pathlib import Path

from yaml import (
    load as yaml_load,
    SafeLoader,
)
from marshmallow_dataclass import class_schema


@dataclass
class BotConfig:
    token: str


@dataclass
class AppConfig:
    bot: BotConfig


AppConfigSchema = class_schema(AppConfig)


def load_config(file: Path) -> AppConfig:
    return AppConfigSchema().load(
        yaml_load(file.read_text(), Loader=SafeLoader)
    )
