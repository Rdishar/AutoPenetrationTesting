from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def dirsearch(domain):
    directorylist = "/root/Desktop/SecLists/Discovery/Web-Content/combined_directories.txt"
    wordlist = "/root/Desktop/SecLists/Discovery/Web-Content/combined_words.txt"
    subprocess.run(f"cp ./{domain}/subdomains/live_{domain}.txt .", shell=True)
    subprocess.run(f"dirsearch.py -l live_{domain}.txt -x 400-499,500-599 -o dirsearchFile.txt ", shell=True)
    subprocess.run("cat dirsearchFile.txt | grep 'htt' | awk '{print $3}' |tee dURL.txt", shell=True)
    subprocess.run(f'mv dirsearchFile.txt ./{domain}/subdomains/dirsearch ', shell=True)
    subprocess.run(f'mv dURL.txt ./{domain}/subdomains/dirsearch ', shell=True)
    subprocess.run(f'rm live_{domain}.txt', shell=True)
    subprocess.run(f'rm -rf reports', shell=True)
dirsearch()
