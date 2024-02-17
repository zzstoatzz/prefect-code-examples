import time
from prefect import flow, task

# tasks inherit their `log_prints` setting from their parent flow
# but can optionally override it with their own setting
@task
def sleep(t: int):
    print(f"Going to sleep for {t} seconds...")
    time.sleep(t)
    print("...and I'm awake!")


@flow(log_prints=True)
def my_flow():
    """flows run submitted tasks concurrently by default"""
    sleep(3) # block the flow for 3 seconds (not concurrently)
    
    future = sleep.submit(2) # submit a task run to the task runner, doesn't block flow
    
    future.wait() # block the flow until the submitted task run is complete
    
    sleep.map([5] * 10) # submit 10 at once, each sleeps for 5 seconds, don't block
    
    # even though the flow is done, we won't exit until all the task runs are complete

if __name__ == "__main__":
    my_flow()