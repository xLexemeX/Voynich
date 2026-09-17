"""Parse an IVTFF transliteration file into clean tokens with metadata.
Output: data/corpus.tsv  (folio, line, locus_type, quire, page_lang, hand, section, text)
Bracketed alternatives [a:b] -> first reading. Removes <...> inline tags, {..} comments.
"""
import re, sys, json
src = sys.argv[1] if len(sys.argv)>1 else 'data/ZL3b-n.txt'
pagemeta = {}
rows = []
cur = None
sect_names = {'H':'herbal','A':'astro','Z':'zodiac','B':'bio','C':'cosmo','P':'pharma','S':'stars','T':'text'}
for raw in open(src, encoding='utf-8', errors='replace'):
    line = raw.rstrip('\n')
    if line.startswith('#'): continue
    m = re.match(r'^<(f\w+)>\s*<!(.*?)>', line)
    if m:
        cur = m.group(1)
        vars_ = dict(re.findall(r'\$(\w)=(\w+)', m.group(2)))
        pagemeta[cur] = vars_
        continue
    m = re.match(r'^<(f\w+)\.(\w+),([@+=*~])(\w+)>\s*(.*)$', line)
    if not m: continue
    folio, lnum, prefix, ltype, text = m.groups()
    # strip inline markers
    t = text
    t = re.sub(r'<!.*?>', '', t)          # comments
    t = re.sub(r'<->', '.', t)            # inline drawing gap = word break
    t = re.sub(r'<~>', '', t)
    t = re.sub(r'<%>|<\$>', '', t)
    t = re.sub(r'<[^>]*>', '', t)         # anything else
    t = re.sub(r'\{[^}]*\}', '', t)
    t = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', t)  # alternatives -> first
    t = t.replace('@', '')
    t = re.sub(r'[!%]', '', t)
    t = t.replace(',', '.')               # uncertain space -> space
    t = re.sub(r'\.+', '.', t).strip('.')
    t = t.replace('?', '')
    pm = pagemeta.get(folio, {})
    rows.append(dict(folio=folio, line=lnum, ltype=ltype, quire=pm.get('Q',''),
                     lang=pm.get('L',''), hand=pm.get('H',''),
                     section=sect_names.get(pm.get('I',''), pm.get('I','')),
                     text=t))
with open('data/corpus.tsv','w') as f:
    f.write('folio\tline\tltype\tquire\tlang\thand\tsection\ttext\n')
    for r in rows:
        f.write('\t'.join(r[k] for k in ['folio','line','ltype','quire','lang','hand','section','text'])+'\n')
json.dump(pagemeta, open('data/pagemeta.json','w'), indent=1)
print(len(rows),'lines;', len(pagemeta),'pages')
