# src/path_model/utils.py

import os
from pathlib import Path
from typing import Optional

import jinja2
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from directory_model.path_model import DirectoryModel

load_dotenv()

class NodeBoolModel(BaseModel):
    """
    A Pydantic model for boolean properties of nodes in a tree that can be inherited
    or recursive.
    """

    value: Optional[bool] = Field(
        None, description="The computed value of the field (True, False, or None)."
    )
    value_init: Optional[bool] = Field(
        None, description="The value of the field when initialized"
    )
    recurse: Optional[bool] = Field(
        None, description="Whether the value should recurse to children."
    )
    inherit: Optional[bool] = Field(
        None, description="Whether the value should be inherited to children."
    )

    def __init__(
        self,
        value: Optional[bool] = None,
        *,
        recurse: Optional[bool] = None,
        inherit: Optional[bool] = None,
    ):
        super().__init__(
            value=value,
            value_init=value,
            recurse=recurse,
            inherit=inherit,
        )

    def __eq__(self, other):
        return self.value == other

    def __bool__(self):
        return self.value is True

def from_yaml(yaml_file: Path) -> DirectoryModel:
    """
    Load the YAML configuration file and replace environment variables using Jinja2.

    Args:
        yaml_file (Path): The path to the YAML configuration file.

    Returns:
        DirectoryModel: The validated project structure based on the YAML configuration.
    """
    with open(yaml_file, "r", encoding="utf-8") as file:
        yaml_content = file.read()

    # Use Jinja2 to replace environment variables in the YAML
    template = jinja2.Template(yaml_content)
    rendered_yaml = template.render(os.environ)

    # Parse the rendered YAML and load it into a Pydantic model
    yaml_data = yaml.safe_load(rendered_yaml)
    return DirectoryModel(**yaml_data)
