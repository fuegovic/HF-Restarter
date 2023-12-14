# Import the HfApi class from the huggingface_hub library
from huggingface_hub import HfApi

# Create an instance of the HfApi class
api = HfApi()

# Get your Hugging Face username and token
# You can find your username on your profile page
# You can generate a token from your settings page
# Use a token with write access
USERNAME = ""
TOKEN = ""

# Get the owner and the name of the Space you want to restart
# For example, if the Space is https://huggingface.co/spaces/USER/SPACENAME
# Then the owner is "USER" and the name is "SPACENAME"
OWNER = ""
NAME = ""

# Use the restart_space() method of the HfApi class to restart the Space
# You need to provide the repo_id argument as "{owner}/{name}"
# And the username and token arguments as your Hugging Face credentials
api.restart_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN)

# Use the factory_rebuild_space() method when an update is needed
# api.factory_rebuild_space(repo_id=f"{OWNER}/{NAME}", token=TOKEN)
