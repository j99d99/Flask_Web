#1.配置salt-master
#参考
vim /etc/salt/master
interface:  $serverip
auto_accept:    True
file_roots:
   base:
      - /usr/local/src/salt

#修改cache目录
cachedir: /usr/local/src/salt
#文件复制模块cp.push需要开启此项
file_recv: True

#2.叫需要用到的脚本文件等均放在fitle_roots定义的目录里面
#3.从minion复制的文件均存放在cachedir目录里
