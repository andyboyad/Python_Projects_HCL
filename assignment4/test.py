import os.path
import time
import os

with os.scandir() as dir_entries:
    for entry in dir_entries:
        print('File         :', entry)
        print('Access time  :', time.ctime(os.path.getatime(entry)))
        print('Modified time:', time.ctime(os.path.getmtime(entry)))
        print('Change time  :', time.ctime(os.path.getctime(entry)))
        print('Size         :', os.path.getsize(entry))

print(open('upload_dir.txt', 'r').read()[0])
