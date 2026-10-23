"""Lossless deterministic gzip streams with compressed and expanded SHA256."""
from pathlib import Path
import argparse,gzip,hashlib,json
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--attempt',type=Path,required=True);a=p.parse_args();result={}
 for n in ['CORE_CYCLES.csv','REFERENCE_RLE.csv']:
  src=a.attempt/n;dst=a.attempt/(n+'.gz');h=hashlib.sha256();size=0
  with src.open('rb') as f,dst.open('wb') as g,gzip.GzipFile(fileobj=g,mode='wb',mtime=0) as z:
   for b in iter(lambda:f.read(1048576),b''):z.write(b);h.update(b);size+=len(b)
  check=hashlib.sha256()
  with gzip.open(dst,'rb') as f:
   for b in iter(lambda:f.read(1048576),b''):check.update(b)
  assert h.hexdigest()==check.hexdigest()==sha(src)
  result[n]={'expanded_bytes':size,'expanded_sha256':h.hexdigest(),'gzip_bytes':dst.stat().st_size,'gzip_sha256':sha(dst),'lossless_readback_verified':True,'raw_retained_locally':True}
 (a.attempt/'STREAM_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
