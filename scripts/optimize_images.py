"""Create web assets without altering originals. Requires Pillow and ImageMagick."""
from pathlib import Path
from PIL import Image, ImageOps
import subprocess, tempfile, json, hashlib, re, base64
ROOT=Path(__file__).resolve().parents[1]
NAMES=['presentation-smart-yiriba','remise-attestations-formation','reunion-travail','espace-formation-smart-yiriba','groupe-participants-atelier','salle-formation','atelier-participatif','formation-en-ligne','participants-formation','session-formation-groupe','atelier-numerique','formateur-presentation','groupe-apprenants','rencontre-en-ligne','participants-smart-yiriba','atelier-entrepreneuriat','apprentissage-informatique','rencontre-exterieure','atelier-femmes','remise-attestations-groupe','rencontre-evenement','participation-evenement','publication-couverture','publication-presentation','participant-evenement','espace-accueil','salle-reunion','espace-travail','locaux-formation','session-atelier','participantes-evenement','entree-locaux','atelier-informatique','presentation-formation','formation-collective','equipement-salle','espace-numerique','materiel-formation','entree-smart-yiriba','support-pedagogique','atelier-groupe','session-groupe','presentation-atelier','formation-femmes-informatique','accompagnement-numerique','atelier-ordinateur','atelier-ordinateur','participants-locaux','rencontre-professionnelle','formation-jeunes-femmes','presentation-participante','participante-ordinateur','salle-smart-yiriba','salle-equipee','apprentissage-ordinateur','formation-pratique-informatique','accompagnement-apprenants','exercice-informatique']
def main():
 files=sorted(p for p in (ROOT/'images').iterdir() if p.suffix.lower() in ['.jpg','.heic','.heif'])
 assert len(files)==len(NAMES), 'Update descriptive names when changing source inventory.'
 dest=ROOT/'images/web';dest.mkdir(exist_ok=True);entries=[];seen={}
 for i,(p,name) in enumerate(zip(files,NAMES)):
  with tempfile.TemporaryDirectory() as tmp:
   converted=Path(tmp)/'photo.png'
   subprocess.run(['magick',str(p)+'[0]','-auto-orient',str(converted)],check=True,capture_output=True)
   with Image.open(converted) as source:
    im=source.convert('RGB'); digest=hashlib.sha256(im.tobytes()+str(im.size).encode()).hexdigest()
    if digest in seen:
     entries.append({'source':p.name,'duplicate_of':seen[digest]['source'],'variants':seen[digest]['variants']});continue
    variants=[]
    for width in (640,1280,1920):
     if width>im.width and variants:continue
     copy=im.copy();copy.thumbnail((width,10000));out=dest/f'{name}-{i+1:02}-{copy.width}w.webp'
     if i == 50 and copy.width == 640: out = dest/'Abou-hassane-cisse-640w.webp'
     copy.save(out,'WEBP',quality=80,method=6)
     variants.append({'path':str(out.relative_to(ROOT)),'width':copy.width,'height':copy.height,'bytes':out.stat().st_size})
    entry={'source':p.name,'name':f'{name}-{i+1:02}','original_bytes':p.stat().st_size,'variants':variants};entries.append(entry);seen[digest]=entry
 # Extract the supplied official mark from the previous page (or saved original).
 old=ROOT/'docs/archive/index-original.html'
 if not old.exists():old=ROOT/'index.html'
 match=re.search(r'data:image/jpeg;base64,([^\"\s]+)',old.read_text())
 if match:
  import io
  with Image.open(io.BytesIO(base64.b64decode(match.group(1)))) as logo:
   logo.thumbnail((240,240));logo.save(dest/'logo-smart-yiriba.webp','WEBP',quality=90)
 (dest/'manifest.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
 rows=['# Inventaire des images web','', 'Les originaux sont conservés. Les noms décrivent le contenu visible sans attribuer de date, de lieu ou d’identité non vérifiés. Les doublons exacts partagent les mêmes fichiers optimisés.','', '| Source | Versions web |','|---|---|']
 for e in entries:rows.append('| '+e['source']+' | '+', '.join('['+Path(v['path']).name+'](../'+v['path']+')' for v in e['variants'])+' |')
 (ROOT/'docs/Smart_YIRIBA_Image_Inventory.md').write_text('\n'.join(rows)+'\n')
 print(f'{len(entries)} sources, {len(seen)} images uniques, {sum(len(e["variants"]) for e in seen.values())} versions WebP')
 print(f'Originaux : {sum(p.stat().st_size for p in files)/1048576:.1f} Mo ; versions web : {sum(p.stat().st_size for p in dest.glob("*.webp"))/1048576:.1f} Mo')
if __name__=='__main__':main()
