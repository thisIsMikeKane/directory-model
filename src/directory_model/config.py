from pydantic import BaseModel

class ConfigModel(BaseModel):
    """
    Configuration settings for validation.
    """

    mkdir: bool = True
    mksymlink: bool = True
    strict: bool = False