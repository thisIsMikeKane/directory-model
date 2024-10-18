
from typing import List, Optional

from pydantic import BaseModel, Field
from rich.tree import Tree
from rich.console import Console

from directory_model.config import ConfigModel
from directory_model.path_model import PathModel


class DirectoryModel(BaseModel):
    """
    Define a model for the overall directory tree.
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
