A Minecraft Launcher in Python
---------------------------
[中文](readme.cn.md)
##Motivation
There are many minecraft servers today.  
Although maintaining a server is not hard, there are still some problems when concentrating the interaction with users.   

For instance, as a curious one, I would always be interested in finding some new mods, but distributing them to users is quite a huge problem; I have to notify everyone, moreover, I need to help them to load those mods, since they do not really have any idea of where they should put them in.

Thus, I decided to make a tool to accomplish the synchronization of mods between clients and server automatically.

Accomplished synchonizing part, I found that it's unacceptable for me to launch game and to synchonize mods separately. You can image what a disaster it is, calling a launcher after updated mods.

Thus! I ! DECIDED! TO! WRITE! A! INDEPENDENT! LAUNCHER! IN! PYTHON!

Life is short, use Python!!!

##Environment
You should install:  
[Python3](https://python.org/)  
[Java 7](https://java.com/en/download/manual_java7.jsp)

##Documentation

Edit `config.json` first.  

If the value of key `gameDir` is `'.'`,  this script will help you to download the game automatically from server. 
 
Here's some [instructions](FAQ/config_instruction.md) of it.  

####Start Game:

Run  `python3 start.py` or `python start.py` if your os is Windows.  

**Please ENSURE that you are using Python3**  

If it doesn't work, check if you have installed Python first, then check if the path of Python has been added to `PATH`.  

[How to add Python to `PATH`](https://docs.python.org/3.4/using/windows.html)


##Contributor
Ray Zhang