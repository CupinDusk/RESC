"""Acquire only public upstream bytes; no firmware generation or DUT execution."""
from pathlib import Path
import hashlib,json,urllib.request,winreg,re
HERE=Path(__file__).resolve().parent
def main():
    out=HERE/'upstream';out.mkdir(exist_ok=True)
    proxies={}
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as k:
        if winreg.QueryValueEx(k,'ProxyEnable')[0]:
            endpoint=winreg.QueryValueEx(k,'ProxyServer')[0]
            if '=' not in endpoint:proxies={'http':'http://'+endpoint,'https':'http://'+endpoint}
            else:
                for pair in endpoint.split(';'):
                    scheme,value=pair.split('=',1)
                    proxies[scheme]=value if '://' in value else 'http://'+value
    opener=urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    def fetch(url):
        errors=[]
        for attempt in range(3):
            try:
                with opener.open(urllib.request.Request(url,headers={'User-Agent':'bounded-research-source-pin'}),timeout=90) as r:return r.read()
            except Exception as e:
                errors.append({'url':url,'attempt':attempt+1,'error_type':type(e).__name__,'message':str(e)})
                (HERE/'ACQUISITION_FAILURES.json').write_text(json.dumps(errors,indent=2)+'\n',encoding='utf-8')
        raise RuntimeError('Public-source download failed; see ACQUISITION_FAILURES.json')
    api=fetch('https://github.com/YosysHQ/picorv32')
    commit=re.search(rb'"currentOid":"([a-f0-9]{40})"',api).group(1).decode();assert len(commit)==40
    # API response can contain personal public author fields; retain only source metadata.
    binding={'repository':'https://github.com/YosysHQ/picorv32','commit':commit,'github_page_sha256':hashlib.sha256(api).hexdigest(),'pin_method':'GitHub repository page currentOid; API attempt returned HTTP403 rate limit and no bytes downloaded','files':{}}
    for n in ['picorv32.v','README.md','COPYING']:
        b=fetch(f'https://raw.githubusercontent.com/YosysHQ/picorv32/{commit}/{n}')
        (out/n).write_bytes(b);binding['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':f'https://raw.githubusercontent.com/YosysHQ/picorv32/{commit}/{n}'}
    (HERE/'UPSTREAM_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(binding,indent=2))
if __name__=='__main__':main()
