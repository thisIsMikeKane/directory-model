# src/path_model/__main__.py

from directory_model.cli import validate_directory
import typer

def main(directory_schema_yaml_path: str = typer.Argument("paths.yml")):
    """
    Main function to validate the directory tree based on a schema YAML file.

    Args:
        directory_schema_yaml_path (str): Path to the YAML file containing the directory schema. Defaults to "paths.yml".

    Returns:
        None

    Example CLI usage:
        python -m path_model /path/to/your/schema.yml
    """
    #TODO confirm proper use of typer.Argument
    validate_directory(directory_schema_yaml_path)

if __name__ == "__main__":
    typer.run(main)
