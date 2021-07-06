from os import environ

class Config:

    def __init__(self):

        # Discord authentication
        self.TOKEN = environ.get('DISCORD_TOKEN')
        self.APP_ID = environ.get('DISCORD_APP_ID')
        # MongoDB authentication
        # self.DB_HOST = environ.get('DB_HOST')
        # self.DB_PASSWORD = environ.get('DB_PASSWORD')

        # MS Bot Framework app
        # self.BOT_API = environ.get('BOT_API')
        # self.BOT_CALLBACK_PORT = int(environ.get('BOT_CALLBACK_PORT'))
        # self.BOT_CALLBACK_HOST = environ.get('BOT_CALLBACK_HOST')

        # Website URL
        self.MY_WEBSITE_URL = "https://leersmathieu.com"
