def get():
    f = open('config/config.txt', 'r')
    info = {}
    
    for i in f.readlines():
        info[i.split('=')[0]] = i.replace('\n', '').split('=')[1]

    return info