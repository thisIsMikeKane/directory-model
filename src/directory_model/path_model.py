# src/path_model/models.py

from pathlib import Path
from typing import List, Union, Annotated

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from rich.style import Style
from rich.tree import Tree

from directory_model.utils import NodeBoolModel

from directory_model.config import ConfigModel
from .validators import validate_children, validate_is_dir, validate_symlinks, validate_exists

class PathModel(BaseModel):
    """
    A Pydantic model to model and validate a path, and its children if specified,
    against what is found on the filesystem.

    Attributes:
        name (str): The name of the directory or file.
        is_dir (bool): Specifies if this is a directory. Validated against `Path.is_dir`.
        description (Optional[str]): Description of the directory or file.
        exists (Union[bool, NodeBoolModel]): The directory/file must exist for validation to succeed.
        resolve (Optional[str]): Path to which this directory resolves (used for symlinks). Validated against `Path.resolve`.
        children (List["PathModel"]): Subdirectories or files within this directory.
        path (Optional[Path]): Resolved full path. Computed if None. Validated if provided.
        config (ConfigModel): Configuration settings for validation.

    Methods:
        build_tree(tree: rich.tree.Tree) -> None: Recursively add nodes to the tree for each directory and its children.
    """

    name: Annotated[str, Field(
        ..., # Required
        description="The name of the directory or file.")]
    
    is_dir: Annotated[bool, Field(
        default=False,
        description="Specifies if this is a directory. Validated against `Path.is_dir`.")]
    
    description: Annotated[Optional[str], Field(
        default=None,
        description="Description of the directory or file.")]

    exists: Annotated[Union[bool, NodeBoolModel], Field(
        default=False,
        description="The directory/file must exist for validation to succeed.")]
    
    resolve: Annotated[Optional[str], Field(
        default=None,
        description="Path to which this directory resolves (used for symlinks). Validated against `Path.resolve`.")]
    
    children: Annotated[List["PathModel"], Field(
        default=[],
        description="Subdirectories or files within this directory.")]
    
    path: Annotated[Optional[Path], Field(
        default=None,
        description="Resolved full path. Computed if None. Validated if provided.")]
    
    config: Annotated[ConfigModel, Field(
        default_factory=ConfigModel,
        description="Configuration settings for validation"
    )]

    model_config = dict(arbitrary_types_allowed=True)

    # Assign validators
    @field_validator("exists", mode="before")
    @classmethod
    def validate_node_bool(cls, v: Union[bool, NodeBoolModel]) -> NodeBoolModel:
        """
        Validate the `exists` attribute to ensure it is compatible with `NodeBoolModel`.

        Args:
            v (Union[bool, NodeBoolModel]): The value to be validated.

        Returns:
            NodeBoolModel: An instance of `NodeBoolModel` representing the validated value.
        """
        return NodeBoolModel(v)

    @model_validator(mode="before")
    def validate_path(self) -> "PathModel":
        """
        Validate and set the `path` attribute to ensure it is absolute and consistent with `name`.

        Returns:
            PathModel: The validated instance of `PathModel`.
        """
        if not self.path:
            self.path = Path(self.name).absolute()
        else:
            if not self.path.is_absolute():
                raise ValueError(f"Expected '{self.path}' to be absolute")
            if Path(self.name).exists() and not Path(self.name).samefile(self.path):
                raise ValueError(f"Expected {self.name} to be the same path as {self.path}")
        return self

    validate_children = model_validator(mode="after")(validate_children)
    validate_is_dir = model_validator(mode="after")(validate_is_dir)
    validate_symlinks = model_validator(mode="after")(validate_symlinks)
    validate_exists = model_validator(mode="after")(validate_exists)

    def build_tree(self, tree: Tree) -> None:
        """
        Recursively add nodes to the tree for each directory and its children.
        """
        if self.is_dir:
            label = f"[bold blue]{self.name}/[/bold blue]"
        else:
            label = f"[blue]{self.name}[/blue]"

        if self.description:
            label += f": {self.description}"

        style = Style(dim=True) if not self.path.exists() else Style()
        node = tree.add(label, style=style)

        if self.children:
            for child in self.children:
                child.build_tree(node)

PathModel.model_rebuild()
