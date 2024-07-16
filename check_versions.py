# check_versions.py
import pandas as pd
import discord
import art
import googletrans
import requests
import nacl
import youtube_dl

print("pandas version:", pd.__version__)
print("discord.py version:", discord.__version__)
print("art version:", art.__version__)
print("googletrans version:", googletrans.__version__)
print("requests version:", requests.__version__)
print("PyNaCl version:", nacl.__version__)
print("youtube_dl version:", youtube_dl.version.__version__)
