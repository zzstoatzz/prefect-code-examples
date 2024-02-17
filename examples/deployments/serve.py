import time
from prefect import flow, task
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
    
    raw_data_futures = fetch_data_for_key.map(keys)

    process_data.map(raw_data_futures)

if __name__ == "__main__":
    work_i_need_to_do_sometimes.serve(
        name="sporradic-deployment",
        parameters={"keys": ["foo", "bar", "baz"]},
    )