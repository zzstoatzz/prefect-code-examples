import asyncio
import httpx
from pathlib import Path
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

def validate_readme():
    readme_markdown = (Path(__file__).parent.parent / "README.md").read_text()

    title = readme_markdown.split("\n")[0].strip("# ")
    
    categories = [
        {
            "name": category.split("\n", 1)[0],
            "examples": [
                {
                    "description": line.split("](")[0].lstrip("- ["),
                    "relative_path": line.split("](")[1].rstrip(")")
                }
                for line in category.split("\n")[1:] if line.startswith("- [")
            ]
        }
        for category in readme_markdown.split("### ")[1:]
    ]

    return Readme.model_validate(dict(title=title, categories=categories))


async def validate_links(readme: Readme):
    base_url = "https://raw.githubusercontent.com/zzstoatzz/prefect-code-examples"
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[
            client.get(f"{base_url}/main/{example.relative_path}")
            for category in readme.categories for example in category.examples
        ])
    
    assert all(response.status_code == 200 for response in responses), "One or more examples are not accessible"

if __name__ == "__main__":
    readme = validate_readme()
    asyncio.run(validate_links(readme))
    (Path(__file__).parent.parent / "views/README.json").write_text(readme.model_dump_json(indent=2))