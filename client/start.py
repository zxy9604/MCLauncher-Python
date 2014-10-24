#A simple minecraft launcher
#By Ray Zhang
#Oct 23. 2014

import json
import os
import urllib.request
import platform

minecraftArguments = {}

#load configs
def loadConfigs():
    f = open("config.json")
    config = json.loads(f.read())
    f.close()
    if not "gameDir" in config:
        print("It seems there is no game.")
    elif not os.path.exists(config['gameDir']):
        print("Path does not exists! Please correct it!")
    os.chdir(config["gameDir"])                     #mark: change dir to 'gameDir'
    return config

#Sync mods

def fetchVersionList(server):
    print("Fetching version list from server...")
    return json.loads(urllib.request.urlopen(server).read().decode())

def fetchModList(server, version):
    os.chdir("versions/" + version)
    if not os.path.exists('mods'):
        os.mkdir('mods')
    os.chdir('mods')                                #mark: change dir to 'mods'
    print("Fetching mods list from server...")
    return json.loads(urllib.request.urlopen(server+'?version='+version).read().decode())

# def callback(blockNum, blockSize, totalSize):
#     w = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')), ' ', ETA(), ' ', FileTransferSpeed()]
#     pbar = ProgressBar(widgets=w, maxval=100).start()
#     amount = 100.0 * blockNum * blockSize / totalSize
#     if amount < 100:
#         pbar.update(int(amount))
#     else:
#         pbar.update(int(amount))
#         pbar.finish()

def downloadMods(config):
    versionList = fetchVersionList(config['server']+'version.php')
    serverPath = versionList[config['version']]['server_path']
    modlist = fetchModList(config['server']+'mods.php', config['version'])
    print("Start downloading mods from server...")
    for f in modlist:
        if not os.path.exists(f):
            print("Find:", f)
            url = config['server'] + serverPath[2:] + '/mods/'
            url += f[2:]
            url = url.replace(' ', '%20')
            print("Download from",url)
            dirpath = f[:len(f)-f[::-1].find('/')]
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            try:
                urllib.request.urlretrieve(url, f)
            except UnicodeEncodeError:
                print("Ignore it")
            except:
                print("The server is down right now. Please try again later!")
    print("Complete! Starting game...")


#launch game

def launchMinecraft(args):
    os.chdir('..')
    os.system(args)

def prepareArgs(config):
    global minecraftArguments
    minecraftArguments = {"username" : config["username"],
                          "version": config["version"],
                          "gameDir": config["gameDir"],
                          "assetsDir" : config["assetsDir"],
                          "assetIndex" : "1.7.10",      #所以这到底是啥
                          "accessToken" : '{}',         #待补全X1
                          "uuid" : '{}',                #待补全X2
                          "userProperties" : '{}',      #233
                          "userType" : "legacy",        #or mojang
                          "tweakClass" : "cpw.mods.fml.common.launcher.FMLTweaker",
                          "mainClass" : "wtf"
                          }
    if config['authenticate'] == True:
        if (not 'username' in config) or (not 'password' in config):
            print("It seems there is no valid username/password, please change `authenticate` to false or add your own profile here.")
            print("Now entering illegal version...")
        else:
            try:
                auth = authenticate(config['username'], config['password'], twitch = config['twitch'])
                minecraftArguments['username'] = auth['name']
                minecraftArguments['uuid'] = auth['uuid']
                minecraftArguments['accessToken'] = auth['accessToken']
                minecraftArguments['userProperties'] = auth['twitchToken']
            except:
                print("Invalid combination of username and password. Please verify it again.")
                print("Now entering illegal version...")

def parsePreparedArgs(args):
    return "{config[mainClass]} --username {config[username]} --version {config[version]} --gameDir {config[gameDir]}/versions/{config[version]} --assetsDir {config[assetsDir]} --uuid {config[uuid]} --accessToken {config[accessToken]} --userProperties {config[userProperties]} --userType {config[userType]} --tweakClass {config[tweakClass]}".format(config = args)

def parseArgs(config):
    args = ''
    prepareArgs(config)
    javaPath = config["javaPath"]
    if javaPath == '':
        javaPath = 'java'                           #if it's not exists, use PATH
    args += javaPath + ' '                          #add java path to
    args += '-Xmx' + config["maxMem"] + ' '         #add -Xmx part
    args += '-Dfml.ignoreInvalidMinecraftCertificates=true '
    if getSystemType() == 'windows' :               #interesting
        args += '-Djava.library.path=".minecraft\\natives" '
    else:
        args += '-Djava.library.path=".minecraft/natives" '
    args += '-cp '
    args += parseLibs(config['gameDir'], readjson(config['version']), config['arch'], config['version']) + ' '
    args += parsePreparedArgs(minecraftArguments)
    return args

def readjson(version):
    f = open('versions/' + version + '/' + version +'.json')
    argsList = json.loads(f.read())
    f.close()
    minecraftArguments['assetIndex'] = argsList['assets']
    minecraftArguments['mainClass'] = argsList['mainClass']
    libs = argsList['libraries']
    return libs

def parseLibs(path, libs, arch, version):
    result = '"'
    if getSystemType() == 'windows':                # wcnm
        result += ";".join((parseSingleLib(path, lib, arch) for lib in libs))
        result += ';'+ path + '\\versions\\' + version + '\\' + version + '.jar'
    else:
        result += ":".join((parseSingleLib(path, lib, arch) for lib in libs))
        result += path + '/versions/' + version + '/' + version + '.jar'
    #split libs by ';' or ':'
    result += '"'
    return result

def parseSingleLib(path, lib, arch):
    result = ""
    name = lib['name']
    index = name.find(':')
    if 'natives' in lib :
        if getSystemType() in lib['natives']:                           #parse the 'natives' part
            if getSystemType() == 'windows':                            #...
                result = path
                result += '\\libraries\\'
                result += name[:index].replace('.','\\') + '\\'         #part of using dots as splitter
                result += name[index+1:].replace(':','\\') + '\\'       #part of using colon as splitter
                result += name[index+1:].replace(':','-')               #At the same time, as the name of jar
            else:
                result = path
                result += '/libraries/'
                result += name[:index].replace('.','/') + '/'           #part of using dots as splitter
                result += name[index+1:].replace(':','/') + '/'         #part of using colon as splitter
                result += name[index+1:].replace(':','-')               #At the same time, as the name of jar
            nativePart = lib['natives'][getSystemType()]
            if nativePart.find("${arch}"):                              #if ${arch} exists, replace it by the argument.
                nativePart = nativePart.replace("${arch}", arch)
            result += '-' + nativePart + '.jar'
    else:
        if getSystemType() == 'windows':                            #F U C K
            result = path
            result += '\\libraries\\'
            result += name[:index].replace('.','\\') + '\\'         #part of using dots as splitter
            result += name[index+1:].replace(':','\\') + '\\'       #part of using colon as splitter
            result += name[index+1:].replace(':','-')               #At the same time, as the name of jar
        else:
            result = path
            result += '/libraries/'
            result += name[:index].replace('.','/') + '/'           #part of using dots as splitter
            result += name[index+1:].replace(':','/') + '/'         #part of using colon as splitter
            result += name[index+1:].replace(':','-')               #At the same time, as the name of jar
        result += '.jar'
    return result


def getSystemType():
    sysstr = platform.system()
    if sysstr == 'Windows' :
        return 'windows'
    elif sysstr == 'Linux' :
        return 'linux'
    elif sysstr == 'Darwin' :
        return 'osx'

def authenticate(username, password, clientToken = "", twitch = False):
    url = 'https://authserver.mojang.com/authenticate'
    params = json.dumps({
              "agent": {
                        "name": "Minecraft",
                        "version": 1
                       },
              "username": username,
              "password": password,
              "clientToken": clientToken,
              "requestUser": twitch
            }).encode()
    header = {'Content-type': 'application/json'}
    req = urllib.request.Request(
        url=url,
        data=params,
        headers=header
    )
    res = json.loads(urllib.request.urlopen(req).read().decode())
    try:
        twitchToken = '''"{"twitch_access_token": ["%s"]}"''' % res["user"]["properties"][0]["value"]
    except:
        twitchToken = "{}"
    return {"accessToken" : res["accessToken"],
            "clientToken" :res["clientToken"],
            "uuid" : res["selectedProfile"]["id"],
            "name" : res["selectedProfile"]["name"],
            "twitchToken" : twitchToken
            }

if __name__ == "__main__":
    cwd = os.getcwd()
    config = loadConfigs()
    if config['sync'] == True:
        downloadMods(config)
    os.chdir(cwd + '/' + config['gameDir'])
    launchMinecraft(parseArgs(config))





