"""Read published case-study files at a pinned commit; disclose schema only.

No experiment, launcher, reset or remote worker command is executed. Third-party
files remain local research inputs because a redistribution license is unverified.
The file selection is all three paper case studies, before numeric inspection.
"""
from pathlib import Path
import csv, hashlib, io, json, urllib.parse, urllib.request

HERE=Path(__file__).resolve().parent
OUT=HERE/'external-ordersage-inputs'
COMMIT='aed526a5a86432834b881bf0166a34f6ffe57623'
FILES=[
 ('memcached_tests.csv','20211012_21:02:01_results/20211012_21:02:01_all_exp_results.csv','5b34f027b43cc1b93b8d30b16aa9ee6bb969e31d'),
 ('memcached_runs.csv','20211012_21:02:01_results/20211012_21:02:01_all_run_results.csv','e9680d9fdc3f42d356cf9f3dd8da5fc5b6148026'),
 ('npbench_tests.csv','20221005_12:13:03_results/20221005_12:13:03_all_test_results.csv','ae5f843c57f661663b45a41eea05ce628e1e80de'),
 ('npbench_runs.csv','20221005_12:13:03_results/20221005_12:13:03_all_run_results.csv','48458063026d239b6c076869cee8a915bf373fdf'),
 ('ufs_tests.csv','20221012_19:59:50_results/20221012_19:59:50_all_test_results.csv','e4a4b497872c19341fd8d2f452aa7870f3b85c18'),
 ('ufs_runs.csv','20221012_19:59:50_results/20221012_19:59:50_all_run_results.csv','3b43f5b969955d590ffe42dacdb3ebca8d2582e4'),
]

def main():
    assert not OUT.exists()
    OUT.mkdir()
    manifest={'repository':'ordersage/paper-artifact','commit':COMMIT,
      'license_status':'not located; raw files are not authorized for redistribution by us',
      'scope':'published data read locally only; all three paper case studies selected before numeric inspection',
      'files':[]}
    schemas={}
    for alias,path,blob in FILES:
        url='https://raw.githubusercontent.com/ordersage/paper-artifact/'+COMMIT+'/'+urllib.parse.quote(path,safe='/')
        raw=urllib.request.urlopen(url,timeout=35).read()
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        assert actual==blob,(alias,actual)
        (OUT/alias).write_bytes(raw)
        reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
        rows=list(reader)
        schemas[alias]={'columns':reader.fieldnames,'rows':len(rows)}
        manifest['files'].append({'alias':alias,'original_path':path,'url':url,
          'git_blob_sha':blob,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'SCHEMAS_ONLY.json').write_text(json.dumps(schemas,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(schemas,indent=2))

if __name__=='__main__':main()
