"""Extract Sherwood's folio identifications (Latin genus in parentheses) from archived plant_list pages in data/ext_sher."""
import re, html, glob, json
out={}
for p in sorted(glob.glob('data/ext_sher/*.html')):
    t=html.unescape(re.sub(r'<[^>]+>','',open(p,encoding='utf-8',errors='replace').read()))
    for m in re.finditer(r'olio (\d+[rv]\d?)\.?,?\s*[^(]{0,80}?\(([A-Z][a-z]+)\s*[a-z]*',t):
        out.setdefault('f'+m.group(1),m.group(2))
json.dump(out,open('data/plantids_sherwood.json','w'),indent=0); print(len(out),out)
