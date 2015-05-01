import os

def getFile(path, context):
    path = os.path.join(os.path.split(context)[0], path)
    return path

def getFileContent(path, context):
    content = ''
    message = ''
    path = getFile(path, context)
    try:
        with open(path, 'r') as f:
            content = f.read()
    except IOError as e:
        return None, "I/O error({0}): {1}".format(e.errno, e.strerror)
    return content, message
