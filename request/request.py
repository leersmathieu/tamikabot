import requests
from os import environ

url = "https://discord.com/api/v8/applications/469072242865602561/guilds/430139146028187658/commands" #guild specified

json = {
    "name": "joke",
    "description": "Send a random funny joke",
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI"
}

r = requests.post(url, headers=headers, json=json)

print(r)