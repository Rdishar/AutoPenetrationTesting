from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def xss(domain):
    subprocess.run(f"cp ./{domain}/urls/allurls.txt .", shell=True)
    subprocess.run(
        f"cat allurls.txt | grep '=' | egrep -iv '.(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt|js)' | tee filtered.txt",
        shell=True)
    subprocess.run(
        f"cat filtered.txt | kxss | tee kxssoutput.txt | sed 's/=.*/=/' | sed 's/URL: //' | dalfox pipe --waf-evasion | tee volnerable.txt",
        shell=True)
    subprocess.run(f'mkdir ./{domain}/xss', shell=True)
    subprocess.run(f'mv volnerable.txt ./{domain}/xss', shell=True)
    subprocess.run(f'mv filtered.txt ./{domain}/xss', shell=True)
    subprocess.run(f'mv kxssoutput.txt ./{domain}/xss', shell=True)
    subprocess.run(f'rm live_{domain}.txt', shell=True)
xss()
