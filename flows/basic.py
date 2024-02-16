from prefect import flow

@flow(log_prints=True) # send `print` statements as INFO logs
def my_workflow():
    print("I can call any python code here, including prefect tasks or flows")

if __name__ == "__main__":
    my_workflow() # call it like a normal python function
    
    # or serve it as a long-lived process
    # my_workflow.serve("my-deployment-name")