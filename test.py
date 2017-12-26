import sys


for i in sys.stdin:
    a = i
    if "Simon says" in a:
        print(a.split("world",1)[1])
