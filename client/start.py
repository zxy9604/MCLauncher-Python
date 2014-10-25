#A simple minecraft launcher
#By Ray Zhang
#Oct 23. 2014

import json
import os
import urllib.request
import platform
import zipfile
import sys

minecraftArguments = {}

#load configs
def loadConfigs():
    with open("config.json", 'r') as f:
        config = json.loads(f.read())
    if not "gameDir" in config:
        print("It seems there is no game.")
        config["gameDir"] = "."
    elif not os.path.exists(config['gameDir']):
        print("Path does not exists! Please correct it!")
        config["gameDir"] = "."
    else:
        os.chdir(config["gameDir"])                     #mark: change dir to 'gameDir'
    return config

#Sync mods

def fetchVersionList(server):
    print("Fetching version list from server...")
    return json.loads(urllib.request.urlopen(server + 'version.php').read().decode())

def fetchModList(server, version, source):
    if not os.path.exists("versions/" + version):
        downloadVersion(server, version)
    os.chdir("versions/" + version)
    if not os.path.exists('mods'):
        os.mkdir('mods')
    os.chdir('mods')                                #mark: change dir to 'mods'
    print("Fetching mods list from server...")
    return json.loads(urllib.request.urlopen(server+'mods.php'+'?version='+version+'&source='+source).read().decode())

def downloadMods(config):
    cwd = os.getcwd()
    versionList = fetchVersionList(config['server'])
    serverPath = versionList[config['version']]['server_path']
    modlist = fetchModList(config['server'], config['version'], 'server')
    print("Start downloading mods from server...")
    for f in modlist:
        if not os.path.exists(f):
            print("Find:", f)
            url = config['server'] + serverPath[2:] + '/mods/'
            url += f[2:]
            url = url.replace(' ', '%20')           #fix some coding problems in http
            print("Download from",url)
            dirpath = f[:len(f)-f[::-1].find('/')]
            if not os.path.exists(dirpath):         #to check whether such a dir exists, if not, make it.
                os.makedirs(dirpath)
            try:
                urllib.request.urlretrieve(url, f)
            except UnicodeEncodeError:              #fucking encode problem. Never mind.
                print("Ignore it")
            except:
                print("The server is down right now. Please try again later!")
    serverPath = versionList[config['version']]['client_path']
    #copy above codes here, but really tired to give it a elegent implementation.
    os.chdir(cwd)
    modlist = fetchModList(config['server'], config['version'], 'client')
    for f in modlist:
        if not os.path.exists(f):
            print("Find:", f)
            url = config['server'] + serverPath[2:] + '/mods/'
            url += f[2:]
            url = url.replace(' ', '%20')           #fix some coding problems in http
            print("Download from",url)
            dirpath = f[:len(f)-f[::-1].find('/')]
            if not os.path.exists(dirpath):         #to check whether such a dir exists, if not, make it.
                os.makedirs(dirpath)
            try:
                urllib.request.urlretrieve(url, f)
            except UnicodeEncodeError:              #fucking encode problem. Never mind.
                print("Ignore it")
            except:
                print("The server is down right now. Please try again later!")
    print("Complete! Starting game...")

# urlretrieve - callback
def filesizeformat(bytes):
    """
    Formats the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc).
    """
    try:
        bytes = float(bytes)
    except (TypeError,ValueError,UnicodeDecodeError):
        return "%(size)d byte" % {'size': 0}

    filesize_number_format = lambda value: round(value, 1)

    return "%s MB" % filesize_number_format(bytes / (1024 * 1024))


def callback(count, blockSize, totalSize):
    width = 32
    percentage = 100 * (count * blockSize)/totalSize
    currentWidth = width*percentage/100
    sys.stdout.write('% 3d%% [%s%s] %s remaining    \r' % (percentage, '=' * int(currentWidth), ' ' * int(width - currentWidth), filesizeformat(totalSize - count * blockSize)))
#download game



def downloadGame(config):
    if not os.path.exists('.minecraft'):
        os.mkdir('.minecraft')
        print("Didn't find '.minecraft', make it..")
    os.chdir('.minecraft')
    downloadDependence(config)
    while True:
        switch = input("Do you want to download resource files right now? y/n: ")
        if switch == 'y' or switch == 'Y':
            downloadAssets(config)
            break
        if switch == 'n' or switch == 'N':
            break
    downloadVersion(config['server'], config['version'])

def downloadDependence(config):
    urllib.request.urlretrieve(config['server']+ '/client/dependence.zip', 'dependence.zip', callback)
    print("\n Extracting...")
    unzip('dependence.zip', '.')
    os.remove('dependence.zip')
    with open('../config.json','w') as f:
        config['gameDir'] = '.minecraft'
        f.write(json.dumps(config, ensure_ascii=False, indent=4, separators = (', \r\n', ': ')))



def downloadAssets(config):
    urllib.request.urlretrieve(config['server']+ '/client/assets.zip', 'assets.zip', callback)
    print("\n Extracting...")
    unzip('assets.zip', '.')
    os.remove('assets.zip')
    with open('../config.json','w') as f:
        config['assetsDir'] = config['gameDir'] + '/assets'
        f.write(json.dumps(config, ensure_ascii=False, indent=4, separators = (', \r\n', ': ')))

def downloadVersion(server, version):
    versionList = fetchVersionList(server)
    if not version in versionList:
        print("The version you have chosen does not exists in Server! Please check it again!")
    else:
        serverPath = server + versionList[version]["client_path"][2:] + '/'
        if not os.path.exists('versions/' + version):
            os.mkdir('versions/' + version)
        print("Downloading " + 'versions/' + version + '/' + version + '.jar')
        urllib.request.urlretrieve(serverPath + version + '.jar', 'versions/' + version + '/' + version + '.jar',callback)
        print("Downloading " + 'versions/' + version + '/' + version + '.json')
        urllib.request.urlretrieve(serverPath + version + '.json', 'versions/' + version + '/' + version + '.json',callback)

def unzip(src, des):
    with zipfile.ZipFile(src) as zf:
        for member in zf.namelist():
            zf.extract(member, des)

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
                          "assetIndex" : "1.7.10",      #WTF it is
                          "accessToken" : '{}',         #to be filled later
                          "uuid" : '{}',                #to be filled later
                          "userProperties" : '{}',      #to be filled later
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
                auth = authenticate(config['username'], config['password'], twitch = config['twitch'])  #authenticate if legal
                minecraftArguments['username'] = auth['name']
                minecraftArguments['uuid'] = auth['uuid']
                minecraftArguments['accessToken'] = auth['accessToken']
                minecraftArguments['userProperties'] = auth['twitchToken']
            except:
                print("Invalid combination of username and password. Please check it again.")
                print("Now entering illegal version...")

def parsePreparedArgs(args):
    return "{config[mainClass]} --username {config[username]} --version {config[version]} --gameDir {config[gameDir]}/versions/{config[version]} --assetsDir {config[assetsDir]} --uuid {config[uuid]} --accessToken {config[accessToken]} --userProperties {config[userProperties]} --userType {config[userType]} --tweakClass {config[tweakClass]}".format(config = args)

def parseArgs(config):
    args = ''
    prepareArgs(config)
    javaPath = config["javaPath"]
    if javaPath == '':
        javaPath = 'java'                           #if it's not exists, use PATH
    if getSystemType() == "windows":
        javaPath = '"' + javaPath + '"'
    args += javaPath + ' '                          #add java path to
    args += '-Xmx' + config["maxMem"] + ' '         #add -Xmx part
    args += '-Dfml.ignoreInvalidMinecraftCertificates=true '
    if getSystemType() == 'windows' :               #interesting
        args += '-Djava.library.path=".minecraft\\natives" '
    else:
        args += '-Djava.library.path=".minecraft/natives" '
    args += '-cp '
    args += parseLibs(config['gameDir'], readjson(config['version']), config['arch'], config['version']) + ' '
    args += parsePreparedArgs(minecraftArguments)   #add other arguments
    if getSystemType() == 'windows' :
        args = '"' + args + '"'
    return args

def readjson(version):
    with open('versions/' + version + '/' + version +'.json', 'r') as f:
        argsList = json.loads(f.read())
    minecraftArguments['assetIndex'] = argsList['assets']
    minecraftArguments['mainClass'] = argsList['mainClass']
    libs = argsList['libraries']
    return libs

def parseLibs(path, libs, arch, version):
    result = '"'
    if getSystemType() == 'windows':                                    # wcnm
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
                result += name[index+1:].replace(':','-')               #At the same time, replace ':' by '-' then use it as the name of jar
            else:
                result = path
                result += '/libraries/'
                result += name[:index].replace('.','/') + '/'           #part of using dots as splitter
                result += name[index+1:].replace(':','/') + '/'         #part of using colon as splitter
                result += name[index+1:].replace(':','-')               #At the same time, replace ':' by '-' then use it as the name of jar
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
            result += name[index+1:].replace(':','-')               #At the same time, replace ':' by '-' then use it as the name of jar
        else:
            result = path
            result += '/libraries/'
            result += name[:index].replace('.','/') + '/'           #part of using dots as splitter
            result += name[index+1:].replace(':','/') + '/'         #part of using colon as splitter
            result += name[index+1:].replace(':','-')               #At the same time, replace ':' by '-' then use it as the name of jar
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
    if config['gameDir'] == ".":
        while True:
            switch = input("Do you want to download game right now? y/n: ")
            if switch == 'y' or switch == 'Y':
                downloadGame(config)
                break
            if switch == 'n' or switch == 'N':
                exit()
    os.chdir(cwd)
    config = loadConfigs()
    if config['sync'] == True:
        downloadMods(config)
    os.chdir(cwd + '/' + config['gameDir'])
    launchMinecraft(parseArgs(config))
