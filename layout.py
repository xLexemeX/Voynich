"""Measure physical line extents (left and right ink edges) on text-only Quire 20 pages and align with the transcription."""
import sys, csv, numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
def measure(folio, fn, star_zone=0.11, thr=150, min_pitch=45, show=False):
    im=Image.open('beinecke/'+fn).convert('L'); a=np.asarray(im); h,w=a.shape
    ink=a<thr
    x0=int(star_zone*w); x1=int(0.97*w)
    proj=ink[:,x0:x1].sum(1).astype(float)
    sm=uniform_filter1d(proj, 15)
    peaks,_=find_peaks(sm, distance=min_pitch, prominence=np.percentile(sm,60)*0.5)
    tr=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['folio']==folio and r['ltype'].startswith('P')]
    return peaks, sm, tr, ink, w, h, x0, x1
if __name__=='__main__':
    folio, fn = sys.argv[1], sys.argv[2]
    peaks, sm, tr, ink, w, h, x0, x1 = measure(folio, fn)
    print(folio, 'peaks', len(peaks), 'transcription lines', len(tr))
    # if counts match, measure edges in a band of +/-18px around each peak
    if len(peaks)==len(tr):
        for p,r in zip(peaks,tr):
            band=ink[max(0,p-18):p+18, :]; cols=band.sum(0)
            xs=np.where(cols[x0:x1]>=2)[0]
            left=x0+xs[0] if len(xs) else -1; right=x0+xs[-1] if len(xs) else -1
            print(f'  y={p:4d} left={left:4d} right={right:4d}  {r["pstart"]}{r["pend"]} {r["text"][:24]:24s} ... {r["text"].split(".")[-1]}')
