# !/usr/bin/python3
from optparse import OptionParser
import subprocess
import re
import os
import json
import requests
from urllib import request


def getipblock(domain):  
    domainip = subprocess.run(f"ping {domain} -c 1 | grep '64 bytes'", shell=True, capture_output=True, text=True)
    result = re.search(r'\d*\.\d*\.\d*\.\d*', str(domainip))
    if result:
        ip = str(result.group(0))
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
        dirsearch_screeenshots(domain)
def filecominer():
        path = os.getcwd()
        os.chdir(path)
        finallist = []

        def convert_json_to_text():
            def read_json_file(file_path):
                f = open(file_path)
                data = json.load(f)
                for i in data:
                    with open("knockpy.txt", 'a') as f:
                        if i != '_meta':
                            f.write(i + '\n')
                        f.close()

            for file in os.listdir():
               
                if file.endswith(".json"):
                    file_path = f"{path}/{file}"
                    read_json_file(file_path)

        def combiner():
           
            def read_text_file(file_path):
                with open(file_path, 'r') as f:
                    return f.read()

            # it will write by reciving value from read_text_file() function.
            def write():
                with open('final.txt', 'a') as f:
                    f.write(read_text_file(file_path))
                    f.close()

            # iterate through all file
            for file in os.listdir():
                # Check whether file is in text format or not
                if file.endswith(".txt"):
                    file_path = f"{path}/{file}"

                    # call read text file function
                    read_text_file(file_path)
                    write()

            # will remove the duplicat value form final.txt file.
            def removeduplicate():
                with open(path + r'/final.txt', 'r') as f:
                    data = f.read().split('\n')
                    for i in data:
                        finallist.append(i)
                    setfinal = set(finallist)
                    listfinal = list(setfinal)
                    with open('without_duplicat.txt', 'a') as f:
                        for line in listfinal:
                            if line != "":
                                f.write(line + '\n')
                        f.close()

            removeduplicate()
            # will remove the final file which is useless.
            os.remove(path + r'/final.txt')
            # os.remove(path + r'\knockpy.txt')

        convert_json_to_text()
        combiner()
def report(domain):
        subprocess.run(f'wc ./{domain}/subdomains/without_duplicat.txt | anew {domain}/reports.txt', shell=True)
        subprocess.run(f'wc ./{domain}/subdomains/live_{domain}.txt | anew {domain}/reports.txt', shell=True)
        subprocess.run(f'wc ./{domain}/domains/amass{domain}.txt | anew {domain}/reports.txt', shell=True)
        subprocess.run(f'wc ./{domain}/subdomains/dirsearch/dURL.txt | anew {domain}/reports.txt', shell=True)
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
def geturls(domain):
    subprocess.run(f"cp ./{domain}/subdomains/live_{domain}.txt .", shell=True)
    subprocess.run(f'cat live_{domain}.txt | waybackurls | tee allurls.txt', shell=True)
    subprocess.run(f"mv allurls.txt {domain}/urls", shell=True)
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
def filterurl():
    dork2 = [
        '=/',
        '?next=',
        '?target=',
        '?url=',
        '?rurl=',
        '/dest=',
        '/destination=',
        '?redir=',
        '?redirect_uri=',
        '?return=',
        '?return_path',
        '/cgi-bin/redirect.cgi?',
        '?checkout_url=',
        '?image_url=',
        '/out?',
        '?continue=',
        '?view=',
        '/redirect/',
        '?go=',
        '?redirect=',
        '?externallink=',
        '?nextURL='
        '?dest=',
        '?destination=',
        '?redirect_url=',
        '/redirect/',
        '/cgi-bin/redirect.cgi?',
        '/out/',
        '/out?',
        '/login?to=',
        '?returnTo=',
        '?return_to=',
        '?ret',
        'Lmage_url=',
        'Open=',
        'callback=',
        'cgi-bin/redirect.cgi',
        'cgi-bin/redirect.cgi?',
        'checkout=',
        'checkout_url=',
        'continue=',
        'data=',
        'dest=',
        'destination=',
        'dir=',
        'domain=',
        'feed=',
        'file=',
        'file_name=',
        'file_url=',
        'folder=',
        'folder_url=',
        'forward=',
        'from_url=',
        'go=',
        'goto=',
        'host=',
        'html=',
        'image_url=',
        'img_url=',
        'load_file=',
        'load_url=',
        'login?to=',
        'login_url=',
        'logout=',
        'navigation=',
        'next=',
        'next_page=',
        'out=',
        'page=',
        'page_url=',
        'path=',
        'port=',
        'redir=',
        'redirect=',
        'redirect_to=',
        'redirect_uri=',
        'redirect_url=',
        'reference=',
        'return=',
        'returnTo=',
        'return_path=',
        'return_to=',
        'return_url=',
        'rt=',
        'rurl=',
        'show=',
        'site=',
        'target=',
        'to=',
        'uri=',
        'url=',
        'val=',
        'validate=',
        'view=',
        'window=',
        'r=',
        '=http',
        '=/'
        'redirecturi=',
        'redirect_uri=',
        'redirecturl=',
        'redirect_uri=',
        'return=',
        'returnurl=',
        'relaystate=',
        'forward=',
        'forwardurl=',
        'forward_url=',
        'dest=',
        'destination=',
        'next=',
        '=http'

    ]
    url = []
    with open('allurls.txt', 'r') as f:
        file = f.read().split('\n')
        for line in file:
            # linee = unquote(line)
            for dor in dork2:
                if dor in line:
                    if line.endswith('///'):
                        line = line[:-3]
                        if line not in url:
                            url.append(line)
                    elif line.endswith('//'):
                        line = line[:-2]
                        if line not in url:
                            url.append(line)
                    elif line.endswith('/'):
                        line = line[:-1]
                        if line not in url:
                            url.append(line)
                    else:
                        url.append(line)
                    break
            continue
    with open('opurl.txt', 'w') as f:
        for line in url:
            f.write(line + '\n')
        f.close()
def openredirect(domain):
    subprocess.run(f"cp ./{domain}/subdomains/live_{domain}.txt .", shell=True)
    subprocess.run(f"cp {domain}/urls/allurls.txt .", shell=True)
    filterurl()
    with open(f'live_{domain}.txt', 'r') as f:
        subdomains = f.read().split('\n')
        for sub in subdomains:
            if sub:
                subprocess.run(f"cat /opt/openredscan/text/origionalpayloads.txt|sed 's/test.com/''{sub}''/' | tee /opt/openredscan/text/payloads.txt", shell=True)
                subprocess.run(f'cat opurl.txt |grep "{sub}"|  while read host do ; do python3 /opt/openredscan/openredacan.py -p /opt/openredscan/text/payloads.txt -u $host ; done |grep "http" | egrep -iv "404|400"| anew openredirectvulnerable.txt', shell=True)
    subprocess.run("cat openredirectvulnerable.txt | awk -F ' ' '{print $5}' | sed 's/^://' | tee pureurl.txt", shell=True)
    liveurls = []
    with open('pureurl.txt', 'r') as f:
        urls = f.read().split('\n')
        for i in urls:
            try:
                resp = request.urlopen(i)
                if resp.code == 200:
                    liveurls.append(i)
            except:
                pass
        f.close()
    with open('volnerable.txt', 'w') as f:
        for i in liveurls:
            f.write(i + '\n')
        f.close()
    subprocess.run(f'mkdir ./{domain}/OR', shell=True)
    subprocess.run(f'mv openredirectvulnerable.txt ./{domain}/OR', shell=True)
    subprocess.run(f'mv volnerable.txt ./{domain}/OR', shell=True)
    subprocess.run(f'rm pureurl.txt', shell=True)
    subprocess.run(f"rm live_{domain}.txt", shell=True)
    subprocess.run(f"rm allurls.txt", shell=True)
def recon(domain):
    if f'{domain}' not in os.listdir():
        subprocess.run(
            f"mkdir {domain} ./{domain}/subdomains ./{domain}/subdomains/dirsearch ./{domain}/subdomains/screenshots ./{domain}/subdomains/dirsearch/screenshots ./{domain}/domains ./{domain}/domains/ips ./{domain}/urls",
            shell=True)
    else:
        pass
    #getipblock(domain)
    getsubdomains(domain)
    dirsearch(domain)
    taking_screenshots(domain)
    geturls(domain)
    xss(domain)
    openredirect(domain)
def readdomain():
    if 'domains' not in os.listdir():
        subprocess.run('mkdir domains', shell=True)
        subprocess.run('cat newdomains.txt | anew domains.txt', shell=True)
        subprocess.run('mv *.txt domains', shell=True)
    with open('domains/domains.txt', 'r') as f:
        for line in f:
            if not line.isspace():
                recon(line.strip())
readdomain()

