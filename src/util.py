import os

def SaveFile(filename, content) :
    f = open(filename, 'w', encoding='utf-8',)
    f.write(content)
    f.close()   

def createFolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: CreateFolder' + path)
