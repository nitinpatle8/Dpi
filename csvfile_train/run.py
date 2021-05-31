import os
cwd = os.getcwd()
filenames = os.listdir(cwd)
for file in filenames:
    if 'streaming' in file:
        os.remove(file)
