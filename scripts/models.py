from pydantic import BaseModel

class Example(BaseModel):
    description: str
    relative_path: str

class ExampleCategory(BaseModel):
    name: str
    examples: list[Example]

class Readme(BaseModel):
    title: str
    categories: list[ExampleCategory]