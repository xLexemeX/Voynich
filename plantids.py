"""Extract tentative plant identifications per folio from voynich.nu quire pages (data/ext_vnu)."""
import re, html, glob, json
out={}
for p in sorted(glob.glob('data/ext_vnu/q*.html')):
    s=open(p,encoding='utf-8',errors='replace').read()
    for m in re.finditer(r'ID="(f\d+[rv]\d?)"(.*?)(?=ID="f\d+[rv]\d?"|$)',s,re.S):
        b=re.search(r'Tentative identifications</H4>\s*<P>(.*?)</P>',m.group(2),re.S)
        if b:
            t=html.unescape(re.sub(r'<[^>]+>',' ',b.group(1))); t=re.sub(r'\s+',' ',t).strip()
            t=re.sub(r'^Possible plant identifications?:?\s*','',t)
            if t: out[m.group(1)]=t
json.dump(out,open('data/plantids.json','w'),indent=0,ensure_ascii=False)
print(len(out))
for k,v in out.items(): print(k,'|',v[:120])
