# -*- coding: utf-8 -*-
"""高级的 文件、文件夹、压缩包 处理模块"""
import shutil

shutil.copyfileobj(open('old.xml','r'),open('new.xml','w'))
# 将文件内容拷贝到另一个文件中

shutil.copyfile('f1.log','f2.log') #目标文件无需存在
# 拷贝文件

shutil.copymode('f1.log','f2.log') #目标文件必须存在
# 仅拷贝权限。内容、组、用户均不变

shutil.copystat('f1.log','f2.log') #目标文件必须存在
# 仅拷贝状态信息。包括：mode bits, atime, mtime, flags

shutil.copy('f1.log','f2.log') # 拷贝文件和权限
#

shutil.copy2('f1.log', 'f2.log')  #拷贝文件和状态信息

shutil.move('folder1', 'folder3') #递归的去移动文件，它类似mv命令，其实就是重命名。


# 压缩包种类，“zip”, “tar”, “bztar”，“gztar”
#将 /data 下的文件打包放置当前程序目录
import shutil
ret = shutil.make_archive("data_bak", 'gztar', root_dir='/data')

#将 /data下的文件打包放置 /tmp/目录
import shutil
ret = shutil.make_archive("/tmp/data_bak", 'gztar', root_dir='/data')

# shutil 对压缩包的处理是调用 ZipFile 和 TarFile 两个模块来进行的，详细：
# zipfile压缩&解压缩

import zipfile

# 压缩
z = zipfile.ZipFile('laxi.zip', 'w')
z.write('a.log')
z.write('data.data')
z.close()

# 解压
z = zipfile.ZipFile('laxi.zip', 'r')
z.extractall(path='.')
z.close()

# tarfile压缩&解压缩
import tarfile

# 压缩
t=tarfile.open('/tmp/egon.tar','w')
t.add('/test1/a.py',arcname='a.bak')
t.add('/test1/b.py',arcname='b.bak')
t.close()

# 解压
t=tarfile.open('/tmp/egon.tar','r')
t.extractall('/egon')
t.close()