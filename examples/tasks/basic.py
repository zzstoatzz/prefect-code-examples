from prefect import flow, task

@task(task_run_name="Adding {x} and {y}") # you can template arguments into the task name!
def add(x: int, y: int) -> int:
    """just a python function with a fancy hat on!"""
    return x + y

@flow
def my_flow():
    """tasks must be called in the flow to be executed (at this time)"""
    first_result = add(1, 2) 
    second_result = add(first_result, first_result)
    return add(first_result, second_result)

if __name__ == "__main__":
    # run the flow
    my_flow()
    
    # you can run tasks' functions directly outside of a flow if you want
    # but it won't be tracked by prefect, it's just a normal function
    assert add.fn(1, 2) == 3

