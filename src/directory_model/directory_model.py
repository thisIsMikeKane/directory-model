
from typing import List, Optional

from pydantic import BaseModel, Field
from rich.tree import Tree
from rich.console import Console

from directory_model.config import ConfigModel
from directory_model.path_model import PathModel


class DirectoryModel(BaseModel):
    """
    DirectoryModel: A model representing the overall directory tree structure. This model includes
    a list of path objects and configuration settings for validation.
    
    Attributes:
        paths (List[PathModel]): A list of path objects representing each path in the base directory.
        config (ConfigModel): Configuration settings used for validation.
    
    Methods:
        validate_project_structure() -> DirectoryModel:
            Validates the project structure by ensuring each path object conforms to the given configuration.
        print_tree():
            Prints the directory tree structure to the console using a tree representation.
    """

    paths: List[PathModel] = Field(
        ...,
        description="List of each path object in the base directory."
    )

    config: ConfigModel = Field(
        default_factory=ConfigModel,
        description="Configuration settings for validation"
    )

    def validate_project_structure(self) -> "DirectoryModel":
        validated_paths = list(self.paths)
        for i, path in enumerate(validated_paths):
            validated_paths[i] = PathModel(**path.dict(), config=self.config)
        self.paths = validated_paths
        return self

    def print_tree(self):
        tree = Tree("Project Structure")
        for path in self.paths:
            path.build_tree(tree)
        console = Console()
        console.print(tree)
