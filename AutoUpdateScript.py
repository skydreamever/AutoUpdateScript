#!/usr/local/anaconda3/envs/learning/bin/python3

import os

#地址需要转义
SUBSCRIBE_ADRESS = ""
CONF_FILE = "/Users/dream/Documents/Surge/Default.conf"
# #移除旧订阅
command = '/usr/local/anaconda3/bin/v2sub remove'
output = os.popen(command).read()
print(output)
#
# # 手动添加订阅
command = '/usr/local/anaconda3/bin/v2sub add ' + SUBSCRIBE_ADRESS
output = os.popen(command).read()
print(output)
#
# #更新
command = '/usr/local/anaconda3/bin/v2sub update'
output = os.popen(command).read()
print(output)

#读取list
command = '/usr/local/anaconda3/bin/v2sub list'
output = os.popen(command).read()

#处理list
string_lines = output.split('\n')
contents = string_lines[3:-1]

proxy_contents = "[Proxy]\n"
proxy_group = '[Proxy Group]\nProxy = select'
for content in contents:
    subcontent = content.split(']')
    index = subcontent[0][1:]
    name = subcontent[1].split('--')[0]
    #构造Proxy
    proxy_content = "%s%s%s%s" % (name, ' = external, exec = "/usr/local/anaconda3/bin/v2sub", args = "run", args = "--port", args = "9900", args = "', index, '", local-port = 9900')
    proxy_contents = "%s%s\n" % (proxy_contents, proxy_content)
    # 构造Proxy Group
    proxy_group = "%s, %s" % (proxy_group, name)

# 写入并添加到Default.conf中
# /Users/dream/Downloads/Default.conf
with open(CONF_FILE, 'r+') as conf_file:
    orign = conf_file.read()
    split_content = orign.split('[Rule]')
    static_content1 = '[Rule]' + split_content[1]
    split_content = split_content[0].split('[Proxy]')
    static_content0 = split_content[0]
    conf_content = "%s%s\n%s\n\n%s" % (static_content0, proxy_contents, proxy_group, static_content1)

    #重新写入文件
    conf_file.seek(0)
    conf_file.truncate()
    conf_file.write(conf_content)
    conf_file.flush()



