# src/path_model/validators.py

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import ValidationError

if TYPE_CHECKING:
    from .path_model import PathModel


def validate_node_bool(v) -> "NodeBoolModel":
    from .path_model import NodeBoolModel

    return NodeBoolModel(v)


def validate_path(self) -> "PathModel":
    if not self.path:
        self.path = Path(self.name).absolute()
    else:
        if not self.path.is_absolute():
            raise ValueError(f"Expected '{self.path}' to be absolute")
        if Path(self.name).exists() and not Path(self.name).samefile(self.path):
            raise ValueError(f"Expected {self.name} to be the same path as {self.path}")
    return self


def validate_children(self) -> "PathModel":
    if self.children:
        validated_children = list(self.children)
        for i, child in enumerate(validated_children):
            child_dict = child.dict()
            child_dict["path"] = self.path / child_dict["name"]
            child_dict["config"] = self.config
            validated_children[i] = self.__class__(**child_dict)
        self.children = validated_children
    return self


def validate_is_dir(self) -> "PathModel":
    if self.children:
        if not self.is_dir:
            raise ValueError(
                f"'{self.path}' should be a directory because it has children."
            )
        self.is_dir = True
    if self.is_dir and self.path.exists():
        if not self.path.is_dir():
            raise ValueError(f"Expected '{self.path}' to be a directory.")
    return self


def validate_symlinks(self) -> "PathModel":
    from loguru import logger

    if self.resolve and self.path.exists():
        if not self.path.is_symlink():
            raise ValueError(f"Expected path '{self.path}' to be a symlink.")
        if not Path(self.resolve).exists():
            raise ValueError(
                f"Resolved path for '{self.name}' does not exist: "
                f"{Path(self.resolve).resolve()}"
            )
        if not self.path.samefile(Path(self.resolve)):
            raise ValueError(
                f"Expected path '{self.path}' to be a symlink resolving to "
                f"'{Path(self.resolve).resolve()}' "
                f"instead of resolving to '{self.path.resolve()}'"
            )
    if self.config.mksymlink and self.resolve and not self.path.exists():
        self.path.symlink_to(self.resolve)
        logger.info(f"Created symlink: {self.path} -> {self.resolve}")
    return self


def validate_exists(self) -> "PathModel":
    from loguru import logger

    if self.exists:
        if not self.path.exists():
            raise ValueError(f"Expected {self.path} to exist.")
    if self.config.mkdir and self.is_dir and not self.path.exists():
        self.path.mkdir(parents=True)
        logger.info(f"Created directory: {self.path}")
    return self
