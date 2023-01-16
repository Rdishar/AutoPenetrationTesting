from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request

def getsubdomains(domain):
        subprocess.run(f"assetfinder -subs-only {domain} | tee ./{domain}/subdomains/assetfinder{domain}.txt",
                       shell=True)

        subprocess.run(f"sublist3r.py -d {domain} -v -t 200 -o ./{domain}/subdomains/sublister{domain}.txt", shell=True)
        #subprocess.run(f"amass intel -d {domain} -whois | tee ./{domain}/domains/amass{domain}.txt", shell=True)
        subprocess.run(f"subfinder -d {domain}  -o ./{domain}/subdomains/subfinder{domain}.txt", shell=True) # it can accept a list
        subprocess.run(f"amass enum -passive -d {domain} -o ./{domain}/subdomains/amassenum{domain}.txt", shell=True)
        subprocess.run(f"knockpy.py {domain} -th 200 -o ./{domain}/subdomains/.", shell=True)
        def getcrtsh_subdomains(domain):
            subdomains = set()
            wildcardsubdomains = set()
            BASE_URL = f"https://crt.sh/?q={domain}&output=json"
            try:
                response = requests.get(BASE_URL.format(domain))
                if response.ok:
                    content = response.content.decode('UTF-8')
                    jsondata = json.loads(content)
                    for i in range(len(jsondata)):
                        name_value = jsondata[i]['name_value']
                        if name_value.find('\n'):
                            subname_value = name_value.split('\n')
                            for subname_value in subname_value:
                                if subname_value.find('*'):
                                    if subname_value not in subdomains:
                                        subdomains.add(subname_value)
                                else:
                                    if subname_value not in wildcardsubdomains:
                                        wildcardsubdomains.add(subname_value)
            except:
                pass

            for subdomain in subdomains:
                with open('crtsh_subdomain.txt', 'a') as f:
                    f.write(subdomain + '\n')
                    f.close()
            subprocess.run(f"mv crtsh_subdomain.txt ./{domain}/subdomains", shell=True)  ##
        getcrtsh_subdomains(domain)
        def getsecurity_tril_subdomain(domain):  # it is the function to get all subdomains from getsecurityTrial website
            url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
            querystring = {"apikey": "RaTQUD5falorL9Qm4OGJAzyUqSiP1Tc1"}
            response = requests.request("GET", url, params=querystring)
            # creating json file from url
            with open('response.json', 'w') as f:
                f.write(response.text)
                f.close()

            def read_json_file():
                listall = []
                f = open('response.json')
                data = json.load(f)
                value = data['meta']['limit_reached']
                if value == False:
                    for i in data['subdomains']:
                        if i != listall:
                            listall.append(f'{i}.domain.com')
                    with open('securitytrails.txt', 'w') as f:
                        for i in listall:
                            if 'domain.com' not in i:
                                f.write(i + '\n')
                        f.close()
                else:
                    # use defrent API
                    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
                    querystring = {"apikey": "GSNrmfRIHKeLGrrCzApkttafZEUrxIMi"}
                    response = requests.request("GET", url, params=querystring)
                    # creating json file from url
                    with open('response.json', 'w') as f:
                        f.write(response.text)
                        f.close()

                    def read_json_file():
                        print("from second API")
                        listall = []
                        f = open('response.json')
                        data = json.load(f)
                        value = data['meta']['limit_reached']
                        if value == False:
                            for i in data['subdomains']:
                                if i != listall:
                                    listall.append(f'{i}.domain.com')
                            with open('securitytrails.txt', 'w') as f:
                                for i in listall:
                                    if 'domain.com' not in i:
                                        f.write(i + '\n')
                                f.close()
                        else:
                            print(" you reached 100 search for two api key:"
                                  "https://api.securitytrails.com")

                    read_json_file()

            read_json_file()
            os.remove('response.json')
            subprocess.run(f"mv securitytrails.txt ./{domain}/subdomains", shell=True)  ##
        getsecurity_tril_subdomain(domain)
        subprocess.run(f'cp {domain}/subdomains/* .', shell=True)
        input(f"IT IS TIME TO ADD THE SUBDOMAIN FROM PORJECTDISCOVERY for {domain}: ")
        filecominer()
        input("ADD outofscope.txt FILE: ")
        oofs = []
        inscop = []
        if 'outofscope.txt' in os.listdir():
            try:
                with open('outofscope.txt', 'r') as f:
                    outofscop = f.read().split('\n')
                    for i in outofscop:
                        oofs.append(i)
                    f.close()
                os.remove(path + r'/outofscope.txt')
                with open('without_duplicat.txt', 'r') as f:
                    ins = f.read().split('\n')
                    for i in ins:
                        if i not in oofs:
                            inscop.append(i)
                    f.close()
                os.remove(path + r'/without_duplicat.txt')
                with open('without_duplicat.txt', 'w') as f:
                    for i in inscop:
                        f.write(i + '\n')
                    f.close()
            except:
                pass
        subprocess.run(
            f'cat without_duplicat.txt| httprobe --prefer-https | sed "s/www.//"| anew livesubdomain.txt',
            shell=True)
        subprocess.run("cat livesubdomain.txt | awk -F'//' '{print $2}' | tee livesubdomain2.txt", shell=True)
        subprocess.run(f"cat livesubdomain2.txt | anew ./{domain}/subdomains/live_{domain}.txt", shell=True)
        subprocess.run('rm livesubdomain2.txt',shell=True)
        subprocess.run('rm livesubdomain.txt', shell=True)
        subprocess.run('rm without_duplicat.txt', shell= True)
        subprocess.run(f'rm *.json', shell=True)
        subprocess.run(f'rm *.txt', shell=True)
        subprocess.run('mv domains/newdomains.txt .', shell=True)
