from os import walk
filenames = next(walk('files/'), (None, None, []))[2]  # [] if no file
print(len(filenames))