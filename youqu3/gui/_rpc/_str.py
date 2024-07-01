slaves_help = """\
附属的测试机，用例步骤中与其他机器进行交互
       ┌─ slave ${user}@${ip}:${password}
master ┼─ slave mikigo@192.168.8.11:admin123
       └─ slave ${user}@${ip}
如果${password}和前面配置项PASSWORD一样，可以不传：${user}@${ip}
多个机器之间用斜线分割：${user}@${ip}:${password}/${user}@${ip}
"""