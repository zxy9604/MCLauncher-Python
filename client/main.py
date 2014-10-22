import json
import os
import urllib.request

def launchMinecraft(conf):
    pass

def loadConfig():
    with open("updator.conf") as f:
        config = json.loads(f.read())

    if not "path" in config:
        print("The path of game is not defined. Please add it in updator.conf")
    elif not os.path.exists(config['path']):
        print("Path does not exists! Please correct it!")
    os.chdir(config["path"])
    return config

#Sync mods

def fetchModList(server):
    return json.loads(urllib.request.urlopen(server).read().decode())




if __name__ == "__main__":
    config = loadConfig()
    modlist = fetchModList(config['server']+'version.php')
    for f in modlist:
        if not os.path.exists(f):
            print("Find:", f)
            url = config['server'] + config['version'] + '/' +'mods' + '/'
            url += f[2:]
            print("Download from",url)
            try:
                urllib.request.urlretrieve(url, f)
            except:
                print("The server is down right now. Please try again later!")
    print("Complete! Press ANYKEY to continue...")
    launchMinecraft(config['launcher'])
    input()




