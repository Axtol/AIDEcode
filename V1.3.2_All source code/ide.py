def c():
    while True:
        cmd = input('>>> ')
        if cmd == "quit" or cmd == "quit()" or cmd == "exit" or cmd == "exit()":
            raise OSError("程序结束")
        last = cmd[-1]
        while last == ':' or last == '\\':
            temp = input('... ')
            cmd += temp
            last = cmd[-1]
        try:
            res = eval(cmd)
            print(res)
        except BaseException as e:
            try:
                exec(cmd)
            except BaseException as e:
                print(e)


def e():
    """
    打开交互模式
    """
    try:
        c()
    except IndexError:
        e()


if __name__ == "__main__":
    e()
