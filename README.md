# tamikabot

The TAMIKABOT is a little discord bot able to make few things like *saying joke, delete messages, playing music, translate sentences, etc*

## NodeJs Version :

https://github.com/leersmathieu/tamikabot/tree/nodejs


## Actual features ON :

- Art  
  - ascii :       Transform a given sentence by ascii art  
- Bank  
  - add_coins:    Add ( or remove if negative number ) a given amount of coins for the given user
  - bank:         See your bank account
- Google
  - google:       From a given entry return a simple search from google
- Joke
  - joke:         The bot say a random joke
  - joke_tts:     The bot say a random joke with text to speech active
- Messages
  - del_messages:Delete X messages from the current channel
  - say:          The bot say a given message to a given channel
  - translate:    Translate a given text to a given language
- Stream
  - leave:        Disconnect the bot from the current voice channel
  - pause:        Pause the audio
  - play:         Download one song from a given url and play it on your current channel
  - reset:        Reset the bot by stopping and removing mp3 file and leaving the channel
  - resume:       Resume the audio
  - stop:         Stop the audio
- No Category
  - help:         Shows this message

## DEV

Pour le lancer avec docker il faut entrer le DISCORD_TOKEN en variable d'environement

Exemple : 

docker run -e DISCORD_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  46tr4b6tr