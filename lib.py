from resources.iio import *
from resources.console import Console
import json, datetime
import os

ROOT_PATH = os.getcwd()
LOGS_PATH = os.path.join(ROOT_PATH, 'logs')

RESOURCES_PATH = os.path.join(ROOT_PATH, 'resources')
DATA_PATH = os.path.join(RESOURCES_PATH, 'data')

# Resources, needed for the bot to function, always go unchanged | borrowed
RESOURCES = {
    'motd': JSONData(path=RESOURCES_PATH, file='motd.json'),
    'name': JSONData(path=RESOURCES_PATH, file='name.json'),
}
# Data storage, changes frequently | borrowed
DATABASE = {
    'users': JSONData(path=DATA_PATH, file='user.json'), # User data
    'guilds': JSONData(path=DATA_PATH, file='guild.json'), # Guild data
    'eco': PickleData(path=DATA_PATH, file='eco.pickle'), # Economy data
    'marriage': JSONData(path=DATA_PATH, file='marriage.json'), # Marriage data
} 

# Borrowed clark assets, thank you jaden
now = datetime.datetime.now()
SETTINGS = {
    'title': f'bot-{now.year}-{now.month}-{now.day}_{now.hour}-{now.minute}-{now.second}.log',
    'limit': 10,
    'folder': LOGS_PATH,
    'compress': True,
    'zipfile': f'bot-logs-{now.month}-{now.year}.zip',
    'debug': False,
    'layout': '[%(asctime)s] [%(levelname)s] %(message)s',
}

console = Console()
console.configure(**SETTINGS)

for obj in RESOURCES.values():
    obj.load() # Load all resources

for obj in DATABASE.values():
    obj.load() # Load all data


#owners
botowners = {
  "Aiire" : 262417442209398784,
  "Derrick" : 164061868741099520
}
# Blacklist
blacklist = {}

#Horny jail
hornijail = {}

#servers
testServerId = 937841015648292934
InsaneAsylum = 880866540906508289

maintainance = False
