# src/path_model/cli.py


from pathlib import Path

import typer
from pydantic import ValidationError

from directory_model.utils import from_yaml

app = typer.Typer()


@app.command()
def validate_directory(
    directory_schema_yaml_path: str = typer.Argument("paths.yml")
):
    """
    Command-line tool to validate the directory tree based on a YAML file.

    Args:
        directory_schema_yaml_path (str): Path to the YAML file to be validated.
    """
    #TODO confirm proper use of typer.Argument

    try:
        project_structure = from_yaml(Path(directory_schema_yaml_path))

        project_structure.print_tree()

        typer.echo("Validation successful! All directories are in place.")

    except ValidationError as e:
        typer.echo(f"Validation Error: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
