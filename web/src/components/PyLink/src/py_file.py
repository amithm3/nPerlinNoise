def fooPrint():
    print('console log from python')


def fooArgsNoReturn(*args, **kwargs):
    print("Args:")
    for arg in args: print(f"{arg} of {type(arg)}")
    print("Kwargs:")
    for key, val in kwargs.items(): print(f"{key} : {val} of {type(val)}")
