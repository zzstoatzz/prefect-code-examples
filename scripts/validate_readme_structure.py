from pathlib import Path

from models import Readme

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

if __name__ == "__main__":
    readme = validate_readme()
    (Path(__file__).parent.parent / "views/README.json").write_text(readme.model_dump_json(indent=2))