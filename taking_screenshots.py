from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def taking_screenshots(domain):
        def dirsearch_screeenshots(domain):
            print('Tacking Screenshots: ')
            subprocess.run(f"cp ./{domain}/subdomains/dirsearch/dURL.txt /opt/EyeWitness/Python", shell=True)
            subprocess.run(
                'python3 /opt/EyeWitness/Python/EyeWitness.py -f /opt/EyeWitness/Python/dURL.txt -d /opt/EyeWitness/Python/report',
                shell=True)
            subprocess.run(f"mv /opt/EyeWitness/Python/report ./{domain}/subdomains/dirsearch/screenshots", shell=True)
            subprocess.run(f'rm /opt/EyeWitness/Python/dURL.txt', shell=True)
        def subdomain_screenshots(domain):
            print('Tacking Screenshots for subdomain: ')
            subprocess.run(f"cp ./{domain}/subdomains/live_{domain}.txt /opt/EyeWitness/Python", shell=True)
            subprocess.run(
                f'python3 /opt/EyeWitness/Python/EyeWitness.py -f /opt/EyeWitness/Python/live_{domain}.txt -d /opt/EyeWitness/Python/report',
                shell=True)
            subprocess.run(f"mv /opt/EyeWitness/Python/report ./{domain}/subdomains/screenshots", shell=True)
            subprocess.run(f'rm /opt/EyeWitness/Python/live_{domain}.txt', shell=True)

        subdomain_screenshots(domain)
        #dirsearch_screeenshots(domain)
