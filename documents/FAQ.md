1. Windows下 在`config.json`里添加路径的时候, 记住用`\\`而不是`\` 因为***要转义! 邪恶的反斜杠wcnm啊!

1. 如果出现:
	
		[main/ERROR] [LaunchWrapper]: Unable to launch java.util.ConcurrentModificationException
	
	
	这样的错误
	
	恭喜你 赶快逃离Java8的魔爪 换回Java7吧233


2. 如果报错`EncodeError`  
	如! 果! 用! 中! 文!  
	要! 用! 也! 用! Unicode!  
	天灭GBK!

3. 其实你完全没必要把`config.json`里的`gameDir`和`assetsDir`改成绝对路径. 
	相对路径是完全可以而且推荐的.
	[什么是绝对路径与相对路径](http://libai.math.ncu.edu.tw/bcc16/4/unix/13.shtml)

4. 没事儿干别乱改`config.json`. 如果改出来什么错务必告诉我, 我尽可能的补上.   
   当然像是在config里边不按照正常的语法规则乱写, 这样报错我是不会去修正的..  
   这不是bug这是feature不谢...