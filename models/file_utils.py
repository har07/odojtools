import os

test_files_dir = 'test_files'

def read_file(file_name):
    f = open(test_files_dir+os.sep+file_name, 'r')
    text = f.read()
    #print(text)
    return text
