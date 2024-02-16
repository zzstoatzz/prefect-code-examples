import asyncio
from prefect import flow

async def some_async_function():
    await asyncio.sleep(1)
    return "I'm an async function"

@flow(log_prints=True) # send `print` statements as INFO logs
async def my_async_workflow():
    print("I can call any python code here, including prefect tasks or flows")
    await some_async_function()

if __name__ == "__main__":
    asyncio.run(my_async_workflow()) # run it like a normal async python function
    
    # or serve it as a long-lived process
    # my_async_workflow.serve("my-deployment-name")