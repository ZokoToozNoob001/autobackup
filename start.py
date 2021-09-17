import os
from dotenv import load_dotenv
import requests
import time
import subprocess

load_dotenv()

if not "accounts" in os.listdir():
  res = requests.get(os.environ["accounts_zip_url"])
  if res.status_code == 200:
    with open('accounts.zip', 'wb') as f:
      f.truncate(0)
      f.write(res.content)
    subprocess.run(["unzip", "-q", "-o", "accounts.zip"])
    os.remove("accounts.zip")
    print("Service accounts downloaded")
  else:
    raise KeyError
  
drives = os.environ["drive_ids"]

drives_list = drives.split(",")

f = open("process.sh","w")

for drives in drives_list:
  drive1 = drives.split(" ")[0]
  drive2 = drives.split(" ")[1]
  text_to_write = "python3 process.py -s {}  -d {}  -sp / -dp / -b 1 -e 600\n".format(drive1, drive2)
  f.write(text_to_write)

f.close()
time.sleep(3)

seconds_to_wait = int(os.environ["rest_seconds"])

while(True):
  subprocess.call(['sh', './process.sh'])
  time.sleep(seconds_to_wait) 