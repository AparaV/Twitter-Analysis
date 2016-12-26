class Global:
    var = 'Hello'

if __name__ == "__main__":
    print Global.var
    Global.var = 5
    print Global.var