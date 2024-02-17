import os
import platform

from prefect import flow, pause_flow_run, task
from prefect.context import EngineContext
from prefect.input import RunInput
from prefect.settings import PREFECT_UI_URL
from pydantic import BaseModel
import webbrowser

class ClockConfig(BaseModel):
    reminder: str = "Time to take a break!"
    prompt: str = "![👋](https://static.wikia.nocookie.net/duolingo/images/4/4a/Duo_waving.svg/revision/latest/scale-to-width-down/250?cb=20230113024808)\nSay the magic word (y/n):" # noqa E501
    require_approval: bool = True
    open_in_browser: bool = False

class Approval(RunInput):
    is_granted: bool = False

@task
def make_a_noise():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 1000)  # 1000 Hz, 1000 ms
    else:
        os.system('echo -n "\\a"')


@flow(log_prints=True) # then we patch `builtins.print`
def pomodoro_timer(config: ClockConfig = ClockConfig()):
    """A flow to remind you to take a break
    
    and wait for you to be ready to get back to work.
    """
    received_approval = False
        
    make_a_noise()
    
    print(config.reminder) # will be logged as INFO

    if config.open_in_browser:
        webbrowser.open_new_tab(
            f"{PREFECT_UI_URL.value()}/flow-runs/flow-run/{EngineContext.get().flow_run.id}"
        )

    while not received_approval:
        # this is cool thing Prefect does
        # pauses the flow run until a type gets hydrated
        # into an instance via some form (any form really)
        received_approval = pause_flow_run(
            wait_for_input=Approval.with_initial_data(
                description=config.prompt
            )
        ).is_granted
    
    make_a_noise()
    
    return "Now get back in there!"

if __name__ == "__main__":
    pomodoro_timer.serve(
        parameters={"config": {"open_in_browser": True}}, # patch default parameter values
        name="Pomodoro Timer", # name of the deployment
        cron="*/15 * * * *"    # on a schedule, run every 15 minutes
    )