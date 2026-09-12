from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np, math, subprocess, wave, json, argparse, shutil, sys, re, difflib, base64, io
from pathlib import Path
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description="Render the fixed Bug Archive quiz format from JSON and a bug PNG.")
parser.add_argument("config",nargs="?",default=str(ROOT/"episodes/CS1002.json"))
parser.add_argument("--bug",help="Override bug PNG (transparent RGBA required)")
parser.add_argument("--output",help="Output MP4 path")
parser.add_argument("--output-dir",default=str(ROOT/"output"))
parser.add_argument("--preview",action="store_true",help="Generate keyframes and layout.json only")
parser.add_argument("--batch",help="Render every *.json in a folder, in filename order")
args=parser.parse_args()
if args.batch:
    configs=[c for c in sorted(Path(args.batch).resolve().glob("*.json")) if c.name!="index.json"]
    if not configs:parser.error("Batch folder contains no JSON files.")
    codes=[json.loads(c.read_text(encoding='utf-8-sig'))['error_code'] for c in configs]
    if len(codes)!=len(set(codes)):parser.error('Each batch episode must have a unique error_code.')
    for config in configs:
        cmd=[sys.executable,str(Path(__file__).resolve()),str(config),"--output-dir",args.output_dir]
        if args.preview:cmd.append("--preview")
        subprocess.run(cmd,check=True)
    sys.exit(0)
configpath=Path(args.config).resolve()
try:cfg=json.loads(configpath.read_text(encoding="utf-8-sig"))
except Exception as e:parser.error(str(e))
for key in ("error_code","message","before","after"):
    if key not in cfg:parser.error(f"Missing field: {key}")
CODE=cfg["error_code"];MESSAGE=cfg["message"]
if not re.fullmatch(r"CS\d{4}",CODE):parser.error("error_code must look like CS1002.")
if not isinstance(MESSAGE,str) or not MESSAGE or "\n" in MESSAGE:parser.error("message must be one nonempty English line.")
before=cfg["before"];after=cfg["after"]
if not isinstance(before,list) or not isinstance(after,list) or not all(isinstance(s,str) and "\n" not in s for s in before+after):parser.error("before/after must be arrays of code lines.")
if not 1<=max(len(before),len(after))<=200 or not before or not after:parser.error("Use 1–200 code lines.")
if before==after:parser.error("before and after are identical; no repair to show.")
before=[s.replace("\t","    ") for s in before];after=[s.replace("\t","    ") for s in after]
bugpath=Path(args.bug).resolve() if args.bug else (configpath.parent/cfg.get('bug','../assets/CS1002.png')).resolve()
OUTPUT=Path(args.output).resolve() if args.output else Path(args.output_dir).resolve()/f"{CODE}-bug-archive.mp4"
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
P=OUTPUT.parent/(OUTPUT.stem+"-preview");P.mkdir(parents=True,exist_ok=True)
W,H=1080,1920;FPS=30;DUR=12
L='#C3FF55';RED='#F27B83';FG='#E9EDF2';MUTED='#83909D';LINE='#333E48'
mono=str(ROOT/'fonts/DejaVuSansMono.ttf');sans=str(ROOT/'fonts/DejaVuSans.ttf')
fontcache={}
def font(n,m=False):
 k=(n,m)
 if k not in fontcache:fontcache[k]=ImageFont.truetype(mono if m else sans,n)
 return fontcache[k]
def text(d,x,y,s,n=32,c=FG,m=False,a='lt'):d.text((x,y),s,font=font(n,m),fill=c,anchor=a)
def ease(p):p=max(0,min(1,p));return p*p*(3-2*p)
def bez(a,b,c,d,p):return tuple((1-p)**3*a[i]+3*(1-p)**2*p*b[i]+3*(1-p)*p*p*c[i]+p**3*d[i] for i in [0,1])
def mix(a,b,p):return tuple(a[i]+(b[i]-a[i])*p for i in [0,1])
Y,X=np.mgrid[:H,:W];v=np.clip(1-((X-540)/1100)**2-((Y-820)/1600)**2,0,1)
arr=np.zeros((H,W,3),np.uint8)
for i,(a,b) in enumerate([(14,10),(18,12),(23,14)]):arr[:,:,i]=a+b*v
back=Image.fromarray(arr).convert('RGBA');d=ImageDraw.Draw(back)
for x in range(120,961,60):
 for y in range(90,1901,60):d.ellipse((x,y,x+1,y+1),fill='#303942')
# restrained lab architecture, deliberately outside code and face
for x in [80,1000]:d.line((x,80,x,1900),fill='#283039',width=1)
for y in [80,1900]:
 d.line((80,y,110,y),fill='#4C5862',width=2);d.line((970,y,1000,y),fill='#4C5862',width=2)
text(d,120,100,'BUG ARCHIVE',23,MUTED,True)
d.line((120,143,960,143),fill=LINE,width=1)
# Center glyph bounds exactly, including punctuation with different ascenders.
def centered(d,x,cy,s,n=32,c=FG,m=False,align="left"):
    ft=font(n,m);box=ft.getbbox(s,anchor="ls");baseline=cy-(box[1]+box[3])/2
    if align=="center":x-=ft.getlength(s)/2
    elif align=="right":x-=ft.getlength(s)
    d.text((x,baseline),s,font=ft,fill=c,anchor="ls")
def fit(s,maxsize,width,m=False,minsize=23):
    for size in range(maxsize,minsize-1,-1):
        if font(size,m).getlength(s)<=width:return size
    parser.error(f"Text is too long for safe layout: {s}")
def wrapped_message(d,x,cy,message,maxsize,width,align="left",color=FG):
    # Keep long compiler diagnostics readable in a centered two-line block.
    for size in range(maxsize,22,-1):
        lines=[];line=""
        for word in message.split():
            candidate=(line+" "+word).strip()
            if font(size,True).getlength(candidate)<=width:line=candidate
            else:
                if line:lines.append(line)
                line=word
        if line:lines.append(line)
        if len(lines)<=2 and all(font(size,True).getlength(z)<=width for z in lines):break
    else:parser.error("Compiler message is too long for the two-line diagnostic area.")
    gap=size+7
    for i,line in enumerate(lines):centered(d,x,cy+(i-(len(lines)-1)/2)*gap,line,size,color,True,align)

count=max(len(before),len(after));cx=220
changes=[]
for i in range(count):
    a=before[i] if i<len(before) else "";b=after[i] if i<len(after) else ""
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!="equal":changes.append((i,i1,i2,j1,j2))
chosen=next((v for v in changes if v[0]==cfg.get("focus_line",changes[0][0]+1)-1),changes[0])
row,i1,i2,j1,j2=chosen
visible=min(count,28)
window_start=max(0,min(count-visible,row-visible//2))
window_end=window_start+visible
cs=min(fit(line,40,704,True,26) for line in before[window_start:window_end]+after[window_start:window_end])
cs=min(cs,int(980/visible)-5)
step=min(58,cs+9)
card_bottom=max(690,350+(visible-1)*step+54)
diag_y=card_bottom+54;bar_y=card_bottom+106
centers=[350+(i-window_start)*step for i in range(count)]
refbox=font(cs,True).getbbox("0123456789Ag",anchor="ls")
ys=[cy-(refbox[1]+refbox[3])/2 for cy in centers]
ex=cx+font(cs,True).getlength((after[row] if row<len(after) else "")[:j1])
repair_x=min(922,ex+max(font(cs,True).getlength((after[row] if row<len(after) else "")[j1:j2]),12)/2)
repair_y=centers[row]
pattern=re.compile(r'("(?:\\.|[^"\\])*"|//.*|\b\d+(?:\.\d+)?\b|\b[A-Za-z_]\w*\b|.)')
keywords={"void","int","float","double","string","bool","public","private","class","return","new","if","else","null","true","false","static","var","using"}
def draw_code(d,line,baseline):
    x=cx
    for match in pattern.finditer(line):
        tok=match.group();c=FG
        if tok.startswith('"'):c='#DCAF92'
        elif tok.startswith('//'):c='#839582'
        elif tok in keywords:c='#C3A6E8'
        elif tok.isdigit():c='#B6CCA4'
        elif tok in {'Debug','Console'}:c='#87D9E7'
        elif re.match(r'^[A-Za-z_]',tok) and line[match.end():].lstrip().startswith('('):c='#D9D4A9'
        d.text((x,baseline),tok,font=font(cs,True),fill=c,anchor='ls');x+=font(cs,True).getlength(tok)
def panel(lines,fixed):
    im=back.copy();d=ImageDraw.Draw(im)
    text(d,120,182,'Find the error in the code.',48)
    d.rounded_rectangle((120,266,960,card_bottom),18,fill='#1D242C',outline='#3B4650',width=2)
    d.rounded_rectangle((120,266,960,326),18,fill='#252E37')
    d.rectangle((121,306,959,326),fill='#252E37')
    name=cfg.get('filename','Player.cs')
    centered(d,150,296,name,fit(name,25,640,True),MUTED,True)
    centered(d,930,296,'C#',23,MUTED,True,'right')
    d.line((121,326,959,326),fill=LINE,width=1)
    if count>visible:centered(d,780,296,f'L{window_start+1}–{window_end} / {count}',20,MUTED,True,'right')
    for idx in range(window_start,min(window_end,len(lines))):
        line=lines[idx]
        if fixed:
            for rr,aa,bb,cc,dd in changes:
                if rr==idx:
                    left=cx+font(cs,True).getlength(line[:cc]);right=cx+font(cs,True).getlength(line[:dd])
                    d.rounded_rectangle((left-2,centers[idx]-cs*.62,min(942,max(left+12,right)+2),centers[idx]+cs*.62),6,fill='#354928')
        d.text((177,ys[idx]),str(idx+1),font=font(cs,True),fill='#697987',anchor='rs')
        draw_code(d,line,ys[idx])
        if fixed:
            for rr,aa,bb,cc,dd in changes:
                if rr==idx and cc!=dd:
                    d.text((cx+font(cs,True).getlength(line[:cc]),ys[idx]),line[cc:dd],font=font(cs,True),fill=L,anchor='ls')
    if not fixed:
        source=before[row] if row<len(before) else ''
        ux=cx+font(cs,True).getlength(source[:i1]);uw=max(24,font(cs,True).getlength(source[i1:i2]))
        # Missing-token markers remain inside the card.
        ux=min(ux,920-uw);uy=centers[row]+cs*.6
        points=[(ux+k,uy+(3 if (k//6)%2 else 0)) for k in range(0,int(uw)+1,6)]
        d.line(points,fill=RED,width=2)
    return im
static=panel(before,False);solved=panel(after,True)
sprites=[]
for i in range(5):
    q=Image.open(ROOT/f'assets/host-{i}.png').convert('RGBA').resize((420,420),Image.Resampling.LANCZOS)
    if i==3:q=ImageOps.mirror(q)
    sprites.append(q)
if cfg.get('bug_data_url') and not args.bug:
    data=cfg['bug_data_url']
    if not data.startswith('data:image/png;base64,'):parser.error('Embedded bug must be PNG.')
    bug=Image.open(io.BytesIO(base64.b64decode(data.split(',',1)[1],validate=True))).convert('RGBA')
else:bug=Image.open(bugpath).convert('RGBA')
if bug.getchannel('A').getextrema()[0]==255:parser.error("Bug must have a transparent background (RGBA PNG), not a checkerboard.")
box=bug.getbbox()
if box is None:parser.error("Bug image is empty.")
bug=bug.crop(box)
# Fit tall AND wide new bugs into identical display regions.
if bug.width/bug.height>1.5:
    canvas=Image.new('RGBA',(bug.width,math.ceil(bug.width/1.5)))
    canvas.alpha_composite(bug,(0,(canvas.height-bug.height)//2));bug=canvas
def paste(im,asset,pos,scale=1,opacity=1,angle=0):
 a=asset
 if scale!=1:a=a.resize((max(1,round(a.width*scale)),max(1,round(a.height*scale))),Image.Resampling.LANCZOS)
 if angle:a=a.rotate(angle,Image.Resampling.BICUBIC,expand=False)
 if opacity<1:a=a.copy();a.putalpha(a.getchannel('A').point(lambda z:int(z*opacity)))
 im.alpha_composite(a,(round(pos[0]),round(pos[1])))
def glow(im,pt,r=70,opacity=.4):
 layer=Image.new('RGBA',(W,H));g=ImageDraw.Draw(layer)
 g.ellipse((pt[0]-r,pt[1]-r,pt[0]+r,pt[1]+r),fill=(169,255,48,int(150*opacity)))
 im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r*.48)))
def bugat(im,pt,h=95,angle=0,opacity=1):
 sc=h/bug.height;ww=bug.width*sc
 paste(im,bug,(pt[0]-ww/2,pt[1]-h/2),sc,opacity,angle)
def spark(im,pt,t,strength=1):
 d=ImageDraw.Draw(im)
 for j in range(10):
  a=j*math.tau/10;r=18+90*t;px=pt[0]+math.cos(a)*r;py=pt[1]+math.sin(a)*r
  k=max(1,int(5*(1-t)*strength));d.ellipse((px-k,py-k,px+k,py+k),fill=L)
def spaced(d,cx,baseline,s,n,c,gap):
 f=font(n,True);widths=[d.textlength(ch,font=f) for ch in s]
 total=sum(widths)+gap*(len(s)-1);x=cx-total/2
 for ch,w in zip(s,widths):d.text((x,baseline),ch,font=f,fill=c,anchor='ls');x+=w+gap
 return total
def bug_mask(box):
 """The bug's alpha, scaled into box and centred, on a full canvas."""
 cx,cy,bw,bh=box;sc=min(bw/bug.width,bh/bug.height)
 shape=bug.getchannel('A').resize((max(1,round(bug.width*sc)),max(1,round(bug.height*sc))),Image.LANCZOS)
 mask=Image.new('L',(W,H),0);mask.paste(shape,(round(cx-shape.width/2),round(cy-shape.height/2)))
 return mask
def locked_thumbnail():
 """The download thumbnail: silhouette, rim glow, error code. Its own layout, not a video frame."""
 y,x=np.mgrid[0:H,0:W]
 dist=np.clip(np.sqrt((x-540)**2+(y-900)**2)/1250,0,1)[...,None]
 inner=np.array([20,28,37]);outer=np.array([8,12,17])
 im=Image.fromarray((inner+(outer-inner)*dist).astype('uint8'),'RGB').convert('RGBA')
 d=ImageDraw.Draw(im)
 for gx in range(36,W,48):
  for gy in range(36,H,48):d.rectangle((gx,gy,gx+1,gy+1),fill='#222D39')
 for tx_,ty in [(64,74),(1016,74),(64,1846),(1016,1846)]:
  d.line((tx_-13,ty,tx_+13,ty),fill='#2C3844',width=2);d.line((tx_,ty-13,tx_,ty+13),fill='#2C3844',width=2)
 spaced(d,96+118,168,'BUG ARCHIVE',29,'#77858F',7)
 d.line((96,196,160,196),fill='#4D5B66',width=3)
 d.rounded_rectangle((88,250,992,1700),16,outline='#2B3742',width=2)
 for bx,by,sx,sy in [(120,282,1,1),(960,282,-1,1),(120,1668,1,-1),(960,1668,-1,-1)]:
  d.line((bx,by+58*sy,bx,by,bx+58*sx,by),fill='#CFDAE2',width=4)
 lw=spaced(d,540,378,'LOCKED',36,'#E9EFF3',13)
 d.line((540-lw/2-90,368,540-lw/2-26,368),fill='#63707B',width=2)
 d.line((540+lw/2+26,368,540+lw/2+90,368),fill='#63707B',width=2)
 mask=bug_mask((540,880,744,800))
 for blur,alpha in [(19,.52),(8,.92),(3,1.0)]:
  layer=Image.new('RGBA',(W,H),L)
  layer.putalpha(mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v:int(v*alpha)))
  im.alpha_composite(layer)
 solid=Image.new('RGBA',(W,H),'#07100A');solid.putalpha(mask);im.alpha_composite(solid)
 d=ImageDraw.Draw(im)
 spaced(d,540,1470,CODE,156,'#F4F1E8',10)
 d.line((480,1546,600,1546),fill='#55616C',width=3)
 return im.convert('RGB')
def scene(t):
 fixed=t>=6
 im=(solved if fixed else static).copy();d=ImageDraw.Draw(im)
 if 6<=t<6.5:
  rr=20+60*(t-6)/.5;d.ellipse((repair_x-rr,repair_y-rr,repair_x+rr,repair_y+rr),outline=L,width=2)
 # diagnostic row and progress track always occupy fixed positions
 # All diagnostic elements share visible-glyph center y=908.
 d.ellipse((120,diag_y-8,136,diag_y+8),fill=RED if not fixed else '#52604D')
 centered(d,155,diag_y,CODE,29,RED if not fixed else MUTED,True)
 divider=155+font(29,True).getlength(CODE)+28
 d.line((divider,diag_y-14,divider,diag_y+14),fill=LINE,width=2)
 wrapped_message(d,divider+28,diag_y,MESSAGE,29,960-divider-28,color=FG if not fixed else MUTED)
 d.rounded_rectangle((120,bar_y-3,876,bar_y+3),3,fill='#35414D')
 p=min(t/6,1)
 if p>0:d.rounded_rectangle((120,bar_y-3,120+756*p,bar_y+3),3,fill=L if fixed else '#96A6B7')
 # reserved numeric slot prevents any layout shift
 if 3<=t<6:centered(d,932,bar_y,str(3-int(t-3)),37,FG,True,'center')
 elif fixed:
  d.line((917,bar_y-1,927,bar_y+9,947,bar_y-11),fill=L,width=3)
 # fixed host zone, all above 1500
 pose=0 if t<4 else 1 if t<5 else 2 if t<6 else 3 if t<8.35 else 4
 bob=math.sin(t*2.6)*3
 ang=2.5*math.sin(t*2) if t<6 else 0
 px,py=450,1484+bob
 if pose==4:py+=4*math.sin((t-8.35)*5)
 paste(im,sprites[pose],(px,py),angle=ang)
 # quick expression crossfade at pose changes
 boundary={1:4,2:5,3:6,4:8.35}.get(pose)
 if boundary is not None and t-boundary<.12:
  paste(im,sprites[pose-1],(px,py),opacity=1-(t-boundary)/.12)
 d=ImageDraw.Draw(im)
 if 3<=t<6:
  # small thought marks, no extra language
  for j in range(3):
   r=3 if j>int((t*2)%3) else 5
   d.ellipse((390+j*19-r,1595-r,390+j*19+r,1595+r),fill=MUTED)
 if 6<=t<7.9:
  # bright scanning trace from the raised index to the repaired token
  finger=(781,1631);end=(repair_x,repair_y);p=ease((t-6)/.32)
  dest=mix(finger,end,p)
  d.line((finger,dest),fill='#6F9241',width=2)
  d.ellipse((dest[0]-5,dest[1]-5,dest[0]+5,dest[1]+5),fill=L)
 # actual bug appears from repaired semicolon then flies toward pinching hand
 if 7.5<=t<8.6:
  p=ease((t-7.5)/1.1)
  pt=bez((repair_x,repair_y),(340,max(900,repair_y+60)),(275,1590),(552,1660),p)
  h=12+68*min(1,(t-7.5)/.25)
  glow(im,pt,56,.28);bugat(im,pt,h,math.sin(p*12)*12)
  if t<7.8:spark(im,(repair_x,repair_y),(t-7.5)/.3)
 elif 8.6<=t<8.88:
  pt=(552,1660);glow(im,pt,65,.5);bugat(im,pt,60)
 elif 8.88<=t<9.48:
  p=ease((t-8.88)/.6);pt=bez((552,1660),(580,1760),(780,1720),(698,1844),p)
  glow(im,pt,50,.5);bugat(im,pt,60*(1-p)+8)
 if 9.3<=t<10:
  p=min(1,(t-9.3)/.7);glow(im,(698,1844),95,(1-p)*.7);spark(im,(698,1844),p)
 # clean, centered codex; underlying background stays identical
 if t>=10:
  im=back.copy();d=ImageDraw.Draw(im)
  p=ease((t-10)/.3)
  # card centered exactly at (540,960): x160..920, y570..1350
  card=Image.new('RGBA',(W,H));c=ImageDraw.Draw(card)
  c.rounded_rectangle((160,570,920,1350),26,fill='#1B242A',outline=L if t>10.45 else '#78828A',width=2)
  for x,y,sx,sy in [(183,593,1,1),(897,593,-1,1),(183,1327,1,-1),(897,1327,-1,-1)]:
   c.line((x,y+22*sy,x,y,x+22*sx,y),fill=L if t>10.45 else MUTED,width=3)
  text(c,540,627,'UNLOCKED' if t>10.45 else 'LOCKED',27,L if t>10.45 else MUTED,True,'mt')
  c.ellipse((360,725,720,1085),outline='#273C2E' if t<=10.45 else '#354337',width=1)
  c.ellipse((378,743,702,1067),outline='#213328' if t<=10.45 else '#29372F',width=1)
  if t<=10.45:
   silhouette=Image.new('RGBA',bug.size,'#1C3026');silhouette.putalpha(bug.getchannel('A').point(lambda a: int(a * .82)))
   sc=260/bug.height;paste(card,silhouette,(540-bug.width*sc/2,775),sc)
  else:
   pulse=max(0,1-(t-10.45)/.7);glow(card,(540,905),180,.25+.4*pulse)
   bugat(card,(540,905),260+15*pulse,math.sin((t-10.45)*4)*2)
   if t<11.1:spark(card,(540,905),(t-10.45)/.65)
  c=ImageDraw.Draw(card)
  c.line((215,1110,865,1110),fill=LINE,width=1)
  text(c,540,1154,CODE,78,FG,True,'mt')
  wrapped_message(c,540,1272,MESSAGE,32,650,'center',L if t>10.45 else MUTED)
  paste(im,card,(0,int((1-p)*45)),opacity=p)
 return im.convert('RGB')
layout={"canvas":[1080,1920],"host_bottom":1904,"content_edges":[120,960],"code_baselines":ys,"line_number_baselines":ys,"code_font_size":cs,"line_number_font_size":cs,"header_center_y":296,"diagnostic_center_y":diag_y,"progress_center_y":bar_y,"countdown_center_y":bar_y,"codex_center":[540,960],"repair_point":[repair_x,repair_y],"visible_lines":[window_start+1,window_end],"code_panel_bottom":card_bottom}
(P/'layout.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
locked_thumbnail().save(OUTPUT.with_name(OUTPUT.stem+'-locked.png'))
for tt in [1,4.4,6.6,8.7,9.2,10.2,11.2]:scene(tt).save(P/f'frame-{tt}.jpg')
if __name__=='__main__':
 import sys
 if args.preview:sys.exit()
 sr=48000;audio=np.zeros(sr*DUR)
 def tone(start,dur,freq,amp=.12,decay=9):
  q=np.arange(int(sr*dur))/sr;en=np.minimum(q/.006,1)*np.exp(-q*decay);z=amp*np.sin(math.tau*freq*q)*en
  k=int(start*sr);audio[k:k+len(z)]+=z
 for t in [3,4,5]:tone(t,.18,680)
 tone(6,.23,880);tone(6.1,.32,1174)
 tone(7.5,.18,1400,.07);tone(8.6,.1,1100,.14);tone(9.35,.35,520,.12)
 for start,freq in [(10.45,660),(10.55,880),(10.68,1320)]:tone(start,.6,freq,.12,6)
 # quiet synthetic flight whoosh, original audio
 rng=np.random.default_rng(21)
 for start,dur in [(7.55,.8),(8.9,.5)]:
  n=int(sr*dur);z=rng.normal(0,.016,n)*np.sin(np.linspace(0,np.pi,n))**2
  z=np.convolve(z,np.ones(11)/11,'same');k=int(start*sr);audio[k:k+n]+=z
 with wave.open(str(P/'sound.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype('<i2').tobytes())
 ffmpeg=shutil.which('ffmpeg')
 if not ffmpeg:
  try:
   import imageio_ffmpeg
   ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
  except ImportError:parser.error('Install dependencies: python -m pip install -r requirements.txt')
 cmd=[ffmpeg,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-i',str(P/'sound.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-shortest',str(OUTPUT)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(FPS*DUR):
  proc.stdin.write(scene(i/FPS).tobytes())
  if i%90==0:print('frame',i,flush=True)
 proc.stdin.close();assert proc.wait()==0
 print('complete',flush=True)
