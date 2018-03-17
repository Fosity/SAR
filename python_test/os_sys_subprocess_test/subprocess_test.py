# -*- coding: utf-8 -*-
""""""
"""
我们经常需要通过Python去执行一条系统命令或脚本，
系统的shell命令是独立于你的python进程之外的，
每执行一条命令，就是发起一个新进程，通过python调用系统命令或脚本的模块在python2有os.system，



三种执行命令的方法
subprocess.run(*popenargs, input=None, timeout=None, check=False, **kwargs) #官方推荐
subprocess.call(*popenargs, timeout=None, **kwargs) #跟上面实现的内容差不多，另一种写法
subprocess.Popen() #上面各种方法的底层封装

run()
标准写法
subprocess.run(['df','-h'],stderr=subprocess.PIPE,stdout=subprocess.PIPE,check=True)
涉及到管道|的命令需要这样写
subprocess.run('df -h|grep disk1',shell=True) #shell=True的意思是这条命令直接交给系统去执行，不需要python负责解

call()
#执行命令，返回命令执行状态 ， 0 or 非0
>>> retcode = subprocess.call(["ls", "-l"])
#执行命令，如果命令结果为0，就正常返回，否则抛异常
>>> subprocess.check_call(["ls", "-l"])
0
#接收字符串格式命令，返回元组形式，第1个元素是执行状态，第2个是命令结果 
>>> subprocess.getstatusoutput('ls /bin/ls')
(0, '/bin/ls')
#接收字符串格式命令，并返回结果
>>> subprocess.getoutput('ls /bin/ls')
'/bin/ls'
#执行命令，并返回结果，注意是返回结果，不是打印，下例结果返回给res
>>> res=subprocess.check_output(['ls','-l'])
>>> res
b'total 0\ndrwxr-xr-x 12 alex staff 408 Nov 2 11:05 OldBoyCRM\n'

Popen()方法
常用参数：
args：shell命令，可以是字符串或者序列类型（如：list，元组）
stdin, stdout, stderr：分别表示程序的标准输入、输出、错误句柄
preexec_fn：只在Unix平台下有效，用于指定一个可执行对象（callable object），它将在子进程运行之前被调用
shell：同上
cwd：用于设置子进程的当前目录
env：用于指定子进程的环境变量。如果env = None，子进程的环境变量将从父进程中继承。

区别是Popen会在发起命令后立刻返回，而不等命令执行结果。这样的好处是什么呢？
如果你调用的命令或脚本 需要执行10分钟，你的主程序不需卡在这里等10分钟，可以继续往下走，
干别的事情，每过一会，通过一个什么方法来检测一下命令是否执行完成就好了。
Popen调用后会返回一个对象，可以通过这个对象拿到命令执行结果或状态等，该对象有以下方法

poll()
Check if child process has terminated. Returns returncode

wait()
Wait for child process to terminate. Returns returncode attribute.

terminate()终止所启动的进程Terminate the process with SIGTERM
kill() 杀死所启动的进程 Kill the process with SIGKILL
communicate()与启动的进程交互，发送数据到stdin,并从stdout接收输出，然后等待任务结束
"""