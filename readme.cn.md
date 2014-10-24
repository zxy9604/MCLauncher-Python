Minecraft 启动器 (Python)
------------------------
[English](readme.md)
##动机
虽然说维护一个服务器不是什么麻烦的事情, 但是和用户老爷们打交道的时候还是有不少蛋疼的事儿.

比如说, 经常好奇心发作, 一时兴起, 给服务器突然装几个mods. 这就得挨个通知大家, 挨个给他们发去文件, 还得帮他们copy到指定的文件夹里(他们要都能找的到mods该放哪我就不会傻逼写这个玩意儿了!)

那么问题来了!

所以我写了一个小工具, 自动同步服务端和本地的mods.

写完同步的这部分以后, 我陷入了深深的沉思. 作为一个处女座, 同步完以后再调用一个奇怪的launcher, 再让用户点来点去, 换你你受得了么!

所以! 我! 一口气! 用Python! 撸了个! 独立的! 启动器!

生命苦短! 快用Python!  (.

##环境配置
只需要安装:  
[Python3](https://python.org/)  
[Java 7](https://java.com/en/download/manual_java7.jsp)

##文档

使用前修改`config.json` 
 
若`gameDir`的键值为`'.'`, 该脚本会自动从服务器下载选定版本的游戏.  
这里是关于此配置文件的[介绍](FAQ/config_instruction.md)

####启动游戏:

如果在*nix下, ``python3 start.py`  

如果在Windows下, 双击`start.py`或者cmd下`python start.py`.  

**一定确保 Python的版本为3.x**  

如果这个不正常工作的话, 先检查一下是否安装了Python, 再检查一下Python是否在`PATH`里.

[如何将Python添加到 `PATH`](https://docs.python.org/3.4/using/windows.html)


##码农
Ray Zhang