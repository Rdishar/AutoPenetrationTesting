import subprocess
import re
import os

def geturls(domain):
    subprocess.run(f"cp ./{domain}/subdomains/live_{domain}.txt .", shell=True)
    subprocess.run(f'cat live_{domain}.txt | waybackurls | tee allurls.txt', shell=True)
    subprocess.run(f"mv allurls.txt {domain}/urls", shell=True)
