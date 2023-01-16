from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def getipblock(domain):  # it will grip all subnet associated to the given domain base on ASN number
    # first it will get target ip, then will curl the ip-api.com website, to find ASN number, then filter all ips form that packet.
    """domainip = subprocess.run(f"ping {domain} -c 1 | grep '64 bytes'", shell=True, capture_output=True, text=True)
    result = re.search(r'\d*\.\d*\.\d*\.\d*', str(domainip))
    if result:
        ip = str(result.group(0))"""
    with open('asnfile.json', 'w') as f:
        subprocess.run(f"curl -s http://ip-api.com/json/{domain}", shell=True, stdout=f, text=True)
    ASNnumber = subprocess.run("cat asnfile.json | jq -r .as | cut -d' ' -f1", shell=True, capture_output=True,
                               text=True)
    ASNnumber = ASNnumber.stdout
    print(ASNnumber)
    with open('ipbp.txt', 'w') as f:
        subprocess.run(f"whois -h whois.radb.net -i origin {ASNnumber}) ", shell=True, stdout=f, text=True)
    subprocess.run("cat ipbp.txt | grep -Eo '([0-9.]+{4}/[0-9]+)' | uniq | tee ipblock.txt", shell=True)
    subprocess.run(f'mv ipblock.txt ./{domain}/domains/ips', shell=True)
    subprocess.run('rm ipbp.txt', shell=True)
    subprocess.run('rm asnfile.json', shell=True)
 getipblock()
