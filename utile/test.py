import os
from os import stat

print(os.listdir("/home/tests/docker-dvwa/aws"))
statinfo = stat(filename)
statinfo