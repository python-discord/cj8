import sys
import time

import requests

print(sys.argv)

for i in range(3):
    print(i)
    time.sleep(0.1)

requests.get('badurl')

for i in range(3):
    print(i)
    time.sleep(0.1)
