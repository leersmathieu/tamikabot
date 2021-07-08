import requests
from os import environ

url = "https://discord.com/api/v8/applications/469072242865602561/guilds/430139146028187658/commands" #guild specified

json = {
    "name": "google",
    "description": "testing bot",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot NDY5MDcyMjQyODY1NjAyNTYx.W08HkQ.ed6MoEIFeIJSVzW8UF7n5NgzhiI"
}

r = requests.post(url, headers=headers, json=json)

print(r)