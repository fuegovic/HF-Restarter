# pylint: skip-file

import os
import time
import datetime
import schedule
from dotenv import load_dotenv
from huggingface_hub import HfApi

# Create an instance of the HfApi class
api = HfApi()

# Load the environment variables from the .env file
load_dotenv()

# Get the environment variables
USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")
OWNER = os.getenv("OWNER")
NAME = os.getenv("NAME")
RESTART_DELAY = int(os.getenv("RESTART_DELAY"))
REBUILD_DELAY = int(os.getenv("REBUILD_DELAY"))

next_restart = datetime.datetime.now() + datetime.timedelta(minutes=RESTART_DELAY)
next_rebuild = datetime.datetime.now() + datetime.timedelta(minutes=REBUILD_DELAY)

def print_next_job_time():
    now = datetime.datetime.now()
    print(f"Current time: {now}")

    # Update next restart/rebuild times if they are in the past
    global next_restart, next_rebuild

    if now > next_restart:
        next_restart = now + datetime.timedelta(minutes=RESTART_DELAY)
    if now > next_rebuild:
        next_rebuild = now + datetime.timedelta(minutes=REBUILD_DELAY)

    # Calculate the time until the next restart
    total_seconds_until_restart = (next_restart - now).total_seconds()

    # Calculate the time until the next rebuild
    total_seconds_until_rebuild = (next_rebuild - now).total_seconds()

    # Create a dynamic display for the time
    def create_time_display(total_seconds):
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        # adapted display based on the length of the time
        if days > 0:
            return f"{int(days)} day(s) and {int(hours)} hour(s)"
        if hours > 0:
            return f"{int(hours)} hour(s) and {int(minutes)} minute(s)"
        return f"{int(minutes)} minute(s) and {int(seconds)} second(s)"
    
    # Print the time until the next restart and rebuild in a user-friendly format
    print(f"Next restart in {create_time_display(total_seconds_until_restart)}")
    print(f"Next rebuild in {create_time_display(total_seconds_until_rebuild)}")

def restart_space():
    global next_restart, next_rebuild
    now = datetime.datetime.now()
    seconds_until_rebuild = (next_rebuild - now).total_seconds()
    minutes_until_rebuild = seconds_until_rebuild // 60

    if now > next_restart:
        if -5 < minutes_until_rebuild  <=5:
            print("Restart skipped due to upcoming rebuild")
        else:
            print("Restarting...")
            api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN)
        next_restart = now + datetime.timedelta(minutes=RESTART_DELAY)

def rebuild_space():
    global next_rebuild
    now= datetime.datetime.now()
    if now > next_rebuild:
        print("Factory Rebooting the space now...")
        api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN, factory_reboot=True)
        next_rebuild = now + datetime.timedelta(minutes=REBUILD_DELAY)

print("Scheduler Started")
print_next_job_time()

# Schedule the print_next_job_time function to run every minute
schedule.every(1).minutes.do(print_next_job_time)

# Schedule the restart_space function to run every RESTART_DELAY minutes
schedule.every(RESTART_DELAY).minutes.do(restart_space)

# Schedule the rebuild_space function to run every REBUILD_DELAY hours
schedule.every(REBUILD_DELAY).minutes.do(rebuild_space)

while True:
    schedule.run_pending()
    time.sleep(1)