import asyncio
from pathlib import Path
import httpx

from models import Readme

async def validate_links(readme: Readme):
    base_url = "https://raw.githubusercontent.com/zzstoatzz/prefect-code-examples"
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[
            client.head(f"{base_url}/main/{example.relative_path}")
            for category in readme.categories for example in category.examples
        ])
    
    assert all(response.status_code == 200 for response in responses), "One or more examples are not accessible"
    
    print("All links are valid")

if __name__ == "__main__":
    asyncio.run(
        validate_links(
            Readme.model_validate_json(
                (Path(__file__).parent.parent / "views/README.json").read_text()
            )
        )
    )