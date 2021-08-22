def myfunc(formal_param='\n'):
    print("hello", end='')
    print(formal_param, end='')
    print("world", end='')


myfunc()
myfunc(formal_param=' ')
