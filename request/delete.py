import requests
from os import environ

# url = "https://discord.com/api/v8/applications/469072242865602561/commands"
url = "https://discord.com/api/v8/applications/469072242865602561/guilds/430139146028187658/commands/862433458802262016" #guild specified


# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI"
}

# or a client credentials token for your app with the applications.commands.update scope
# headers = {
#     "Authorization": "Bearer <my_credentials_token>"
# }

r = requests.delete(url, headers=headers)

print(r)