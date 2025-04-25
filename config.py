import os
import sys

appname = 'subsync'


if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    datadir = sys._MEIPASS
else:
    datadir = os.path.dirname(__file__)

configdir = "/config"
shareddir = configdir
assetupd =  None

configpath = os.path.join(configdir, appname + '.json')
assetspath = os.path.join(configdir, 'assets.json')

assetdir   = os.path.join(shareddir, 'assets')
imgdir     = os.path.join(datadir, 'img')
localedir  = os.path.join(datadir, 'locale')
keypath    = os.path.join(datadir, 'key.pub')

assetsurl = 'https://github.com/sc0ty/subsync/releases/download/assets/assets.json'