import json
import time
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact
from pydantic import BaseModel, Field

class Data(BaseModel):
    key: str
    value: dict = Field(default_factory=dict)

@task
def fetch_data_for_key(key: str) -> Data:
    """A task that simulates fetching data from some source"""
    return Data(key=key, value={"data": "some data"})

@task
def process_data(data: Data) -> Data:
    """A task that simulates processing data"""
    print(f"Processing {data!r} (I swear)")
    time.sleep(3)
    return data

@flow
def work_i_need_to_do_sometimes(keys: list[str]):
    """Work you might need to do ever so often"""
    
    keys_repr = "-".join(sorted(keys))
    
    raw_data_futures = fetch_data_for_key.map(keys)

    futures = process_data.map(raw_data_futures)
    
    create_markdown_artifact(
        markdown=(
            "![image](https://t.ly/xsf5J)\n"
            f"## processed data for {keys_repr}\n\n```json\n"
            f"{json.dumps([f.result().model_dump() for f in futures], indent=2)}\n```"
        ),
        key=keys_repr,
    )

if __name__ == "__main__":
    work_i_need_to_do_sometimes.serve(
        name="sporradic-deployment",
        parameters={"keys": ["foo", "bar", "baz"]},
    )