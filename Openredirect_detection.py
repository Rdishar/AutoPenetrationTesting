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
