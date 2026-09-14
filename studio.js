'use strict';
const $=id=>document.getElementById(id),C=$('preview'),ctx=C.getContext('2d'),L='#c3ff55',FG='#e9edf2',M='#83909d',R='#f27b83';
const defaults={error_code:'CS1002',message:'; expected',filename:'Player.cs',before:['void Start()','{','    Debug.Log("Hello")','}'],after:['void Start()','{','    Debug.Log("Hello");','}'],bug:'../assets/CS1002.png'};
let bugData=STUDIO_ASSETS.CS1002,bug,hosts=[],time=4.4,playing=false,last=0,model,ready=false,activeJob=false,localStudio=false;
const font=(n,mono=false)=>{ctx.font=`${n}px ${mono?'ArchiveMono':'ArchiveSans'}`;};
const width=(s,n,mono=true)=>{font(n,mono);return ctx.measureText(s).width;};
function tx(s,x,cy,n=32,color=FG,mono=false,align='left'){font(n,mono);ctx.fillStyle=color;ctx.textAlign=align;ctx.textBaseline='alphabetic';const m=ctx.measureText(s);ctx.fillText(s,x,cy+(m.actualBoundingBoxAscent-m.actualBoundingBoxDescent)/2);}
function rr(x,y,w,h,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke();}}
function line(points,color,w=1){ctx.beginPath();ctx.moveTo(...points[0]);for(const p of points.slice(1))ctx.lineTo(...p);ctx.strokeStyle=color;ctx.lineWidth=w;ctx.stroke();}
function circle(x,y,r,color,stroke){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);if(color){ctx.fillStyle=color;ctx.fill();}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1;ctx.stroke();}}
function glow(x,y,r=70){const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,'#b7ff5535');g.addColorStop(1,'#b7ff5500');ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);}
const ease=p=>{p=Math.max(0,Math.min(1,p));return p*p*(3-2*p);};
const bez=(a,b,c,d,p)=>[0,1].map(i=>(1-p)**3*a[i]+3*(1-p)**2*p*b[i]+3*(1-p)*p*p*c[i]+p**3*d[i]);
function loadImage(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error('Could not load image.'));im.src=src;});}
function message(s,x,y,maxsize,maxw,align='left',color=FG){let lines=[],size=maxsize;for(;size>=23;size--){lines=[];let str='';for(const word of s.split(/\s+/)){const z=(str+' '+word).trim();if(width(z,size)<=maxw)str=z;else{if(str)lines.push(str);str=word;}}if(str)lines.push(str);if(lines.length<=2&&lines.every(z=>width(z,size)<=maxw))break;}if(size<23)throw Error('Compiler message is too long for the two-line area.');lines.forEach((z,i)=>tx(z,x,y+(i-(lines.length-1)/2)*(size+7),size,color,true,align));}
function cfg(){const out={error_code:$('errorcode').value.trim(),filename:$('filename').value.trim()||'Player.cs',message:$('message').value,before:$('before').value.replace(/\t/g,'    ').split('\n'),after:$('after').value.replace(/\t/g,'    ').split('\n'),bug:'embedded.png',bug_data_url:bugData};if($('focus').value)out.focus_line=Number($('focus').value);out.music=musicChoice||'none';return out;}
function build(){const q=cfg();if(!/^CS\d{4}$/.test(q.error_code))throw Error('Use an error code such as CS1002.');if(!q.message.trim()||q.message.includes('\n'))throw Error('Enter a compiler message.');const count=Math.max(q.before.length,q.after.length);if(count>200)throw Error('Up to 200 source lines are supported.');let changes=[];for(let row=0;row<count;row++){const a=q.before[row]||'',b=q.after[row]||'';if(a===b)continue;let p=0;while(p<Math.min(a.length,b.length)&&a[p]===b[p])p++;let ae=a.length,be=b.length;while(ae>p&&be>p&&a[ae-1]===b[be-1]){ae--;be--;}changes.push({row,start:p,oldend:ae,end:be});}if(!changes.length)throw Error('Before and After must contain a correction.');const focus=changes.find(c=>c.row===q.focus_line-1)||changes[0],visible=Math.min(count,28),start=Math.max(0,Math.min(count-visible,focus.row-Math.floor(visible/2))),end=start+visible;let size=40;for(;size>=26;size--){if([...q.before.slice(start,end),...q.after.slice(start,end)].every(s=>width(s,size)<=704))break;}if(size<26)throw Error('A visible code line is too wide. Shorten that line.');size=Math.min(size,Math.floor(980/visible)-5);const step=Math.min(58,size+9),bottom=Math.max(690,350+(visible-1)*step+54);const target=[Math.min(922,220+width((q.after[focus.row]||'').slice(0,focus.start),size)+Math.max(width((q.after[focus.row]||'').slice(focus.start,focus.end),size),12)/2),350+(focus.row-start)*step];return {...q,count,changes,focus,visible,start,end,size,step,bottom,diag:bottom+54,bar:bottom+106,target};}
function background(){const g=ctx.createRadialGradient(540,850,30,540,850,1300);g.addColorStop(0,'#181e25');g.addColorStop(1,'#0e1217');ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);for(let x=120;x<=960;x+=60)for(let y=90;y<=1900;y+=60){ctx.fillStyle='#303942';ctx.fillRect(x,y,1,1);}for(const x of [80,1000])line([[x,80],[x,1900]],'#283039');for(const y of [80,1900]){line([[80,y],[110,y]],'#4c5862',2);line([[970,y],[1000,y]],'#4c5862',2);}tx('BUG ARCHIVE',120,109,23,M,true);line([[120,143],[960,143]],'#333e48');}
const keywords=new Set('void int float double string bool public private class return new if else null true false static var using'.split(' '));
function codeLine(s,x,baseline,size){font(size,true);ctx.textBaseline='alphabetic';ctx.textAlign='left';const re=/("(?:\\.|[^"\\])*"|\/\/.*|\b\d+(?:\.\d+)?\b|\b[A-Za-z_]\w*\b|.)/g;let m;while((m=re.exec(s))){let c=FG,t=m[0];if(t.startsWith('"'))c='#dcaf92';else if(t.startsWith('//'))c='#839582';else if(keywords.has(t))c='#c3a6e8';else if(/^\d/.test(t))c='#b6cca4';else if(['Debug','Console'].includes(t))c='#87d9e7';else if(/^[A-Za-z_]/.test(t)&&s.slice(re.lastIndex).trimStart().startsWith('('))c='#d9d4a9';ctx.fillStyle=c;ctx.fillText(t,x,baseline);x+=ctx.measureText(t).width;}}
/* An episode with no bug PNG loads with no bug at all. Carrying the previous episode's image
   over made it look ready to render when it was not, and the render would have committed the
   wrong PNG under this episode's error code. */
const BLANK_PNG='data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
function clearBug(){bugData=null;bug=null;$('bugthumb').src=BLANK_PNG;markBugState();}
function markBugState(){const missing=!bugData;
for(const id of ['render','thumbnail'])$(id).disabled=missing||activeJob;
$('bugthumb').classList.toggle('empty',missing);$('bugthumb').alt=missing?'':'Selected bug';
$('bugmissing').hidden=!missing;}
function drawBug(x,y,height=80,gray=false,angle=0){if(!bug)return;ctx.save();ctx.translate(x,y);ctx.rotate(angle);if(gray)ctx.filter='grayscale(1)';const scale=height/bug.height;ctx.drawImage(bug,-bug.width*scale/2,-height/2,bug.width*scale,height);ctx.restore();}
const CODEX_LIFT=330;/* the codex sits high so a Shorts sticker can take the lower half */
function archive(t,forceLocked=false){const locked=forceLocked||t<=10.45;ctx.save();ctx.translate(0,-CODEX_LIFT);rr(160,570,760,780,26,'#1b242a',locked?'#78828a':L);for(const [x,y,sx,sy]of[[183,593,1,1],[897,593,-1,1],[183,1327,1,-1],[897,1327,-1,-1]])line([[x,y+22*sy],[x,y],[x+22*sx,y]],locked?M:L,3);tx(locked?'LOCKED':'UNLOCKED',540,637,27,locked?M:L,true,'center');circle(540,905,180,null,locked?'#3c4348':'#354337');circle(540,905,162,null,locked?'#30383f':'#29372f');if(!locked)glow(540,905,200);drawBug(540,905,260,locked,locked?0:Math.sin((t-10.45)*4)*.035);line([[215,1110],[865,1110]],'#333e48');tx(model.error_code,540,1184,78,FG,true,'center');message(model.message,540,1272,32,650,'center',locked?M:L);ctx.restore();}
function draw(t=time,thumbnail=false){if(!ready||!model)return;ctx.clearRect(0,0,1080,1920);background();if(t>=10||thumbnail){archive(t,thumbnail);}else{const q=model,fix=t>=6;tx('Find the error in the code.',120,205,48);rr(120,266,840,q.bottom-266,18,'#1d242c','#3b4650');rr(120,266,840,60,18,'#252e37');ctx.fillStyle='#252e37';ctx.fillRect(121,306,838,20);tx(q.filename,150,296,25,M,true);tx('C#',930,296,23,M,true,'right');if(q.count>q.visible)tx(`L${q.start+1}–${q.end} / ${q.count}`,780,296,20,M,true,'right');line([[121,326],[959,326]],'#333e48');font(q.size,true);let metrics=ctx.measureText('0123456789Ag'),offset=(metrics.actualBoundingBoxAscent-metrics.actualBoundingBoxDescent)/2;const lines=fix?q.after:q.before;for(let row=q.start;row<Math.min(q.end,lines.length);row++){const y=350+(row-q.start)*q.step,b=y+offset,s=lines[row];if(fix)for(const ch of q.changes.filter(c=>c.row===row)){let x=220+width(s.slice(0,ch.start),q.size),w=Math.max(12,width(s.slice(ch.start,ch.end),q.size));rr(x-2,y-q.size*.62,w+4,q.size*1.24,6,'#354928');}font(q.size,true);ctx.fillStyle='#697987';ctx.textBaseline='alphabetic';ctx.textAlign='right';ctx.fillText(String(row+1),177,b);codeLine(s,220,b,q.size);if(fix)for(const ch of q.changes.filter(c=>c.row===row)){font(q.size,true);ctx.fillStyle=L;ctx.fillText(s.slice(ch.start,ch.end),220+width(s.slice(0,ch.start),q.size),b);}}if(!fix){const f=q.focus,a=q.before[f.row]||'',w=Math.max(24,width(a.slice(f.start,f.oldend),q.size));const x=Math.min(220+width(a.slice(0,f.start),q.size),920-w),y=q.target[1]+q.size*.6,pts=[];for(let k=0;k<=w;k+=6)pts.push([x+k,y+(Math.floor(k/6)%2?3:0)]);line(pts,R,2);}circle(128,q.diag,8,fix?'#52604d':R);tx(q.error_code,155,q.diag,29,fix?M:R,true);const div=155+width(q.error_code,29)+28;line([[div,q.diag-14],[div,q.diag+14]],'#333e48',2);message(q.message,div+28,q.diag,29,960-div-28,'left',fix?M:FG);rr(120,q.bar-3,756,6,3,'#35414d');rr(120,q.bar-3,Math.max(1,756*Math.min(t/6,1)),6,3,fix?L:'#96a6b7');if(t>=3&&t<6)tx(String(3-Math.floor(t-3)),932,q.bar,37,FG,true,'center');else if(fix)line([[917,q.bar-1],[927,q.bar+9],[947,q.bar-11]],L,3);
const pose=t<4?0:t<5?1:t<6?2:t<8.35?3:4;ctx.save();ctx.translate(660,1694+Math.sin(t*2.6)*3);if(t<6)ctx.rotate(2.5*Math.sin(t*2)*Math.PI/180);if(pose===3)ctx.scale(-1,1);ctx.drawImage(hosts[pose],-210,-210,420,420);ctx.restore();if(t>=3&&t<6)for(let j=0;j<3;j++)circle(390+j*19,1595,j>Math.floor(t*2%3)?3:5,M);if(t>=6&&t<7.9){const f=[781,1631],p=ease((t-6)/.32),a=f.map((v,i)=>v+(q.target[i]-v)*p);line([f,a],'#6f9241',2);circle(...a,5,L);}if(t>=7.5&&t<8.6){let p=ease((t-7.5)/1.1),a=bez(q.target,[340,Math.max(900,q.target[1]+60)],[275,1590],[552,1660],p);glow(...a,60);drawBug(...a,12+68*Math.min(1,(t-7.5)/.25),false,Math.sin(p*12)*.2);}else if(t>=8.6&&t<8.88){glow(552,1660);drawBug(552,1660,60);}else if(t>=8.88&&t<9.48){const p=ease((t-8.88)/.6),a=bez([552,1660],[580,1760],[780,1720],[698,1844],p);glow(...a);drawBug(...a,60*(1-p)+8);}if(t>=9.3&&t<10)glow(698,1844,95*(1-(t-9.3)/.7));}
if($('guides').checked&&!thumbnail){ctx.fillStyle='#00000065';ctx.fillRect(930,850,150,1070);ctx.fillRect(0,1720,1080,200);tx('UI OVERLAY',970,1190,19,'#ffffff88',true,'center');tx('CHANNEL / CAPTION',540,1790,25,'#ffffff88',true,'center');} }
function status(s,error=false){$('status').textContent=s;$('status').classList.toggle('error',error);}
function update(){try{model=build();draw();refreshMusic();$('lineinfo').textContent=`${model.count} lines · ${model.visible} visible · ${model.size}px`;status(model.count>28?`Showing lines ${model.start+1}–${model.end} around the repair.`:'Ready.');try{localStorage.setItem('bugarchive-v2',JSON.stringify(cfg()));}catch{}}catch(e){status(e.message,true);model=null;}}
async function setConfig(q){for(const k of ['error_code','message','before','after'])if(!(k in q))throw Error(`Missing ${k}`);$('errorcode').value=q.error_code;$('filename').value=q.filename||'Player.cs';$('message').value=q.message;$('before').value=q.before.join('\n');$('after').value=q.after.join('\n');$('focus').value=q.focus_line||'';musicChoice=q.music==='none'?'':(q.music||'random');refreshMusic();if(q.bug_data_url)await setBug(q.bug_data_url);else if(!q.bug||q.bug.includes('CS1002'))await setBug(STUDIO_ASSETS.CS1002);else clearBug();update();}
async function setBug(src){const im=await loadImage(src),temp=document.createElement('canvas');temp.width=im.width;temp.height=im.height;const d=temp.getContext('2d');d.drawImage(im,0,0);const data=d.getImageData(0,0,im.width,im.height).data;let x0=im.width,y0=im.height,x1=-1,y1=-1,transparent=false;for(let y=0;y<im.height;y++)for(let x=0;x<im.width;x++){const a=data[(y*im.width+x)*4+3];if(a<255)transparent=true;if(a>0){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);}}if(!transparent)throw Error('Choose a PNG with a genuinely transparent background.');if(x1<0)throw Error('The PNG is empty.');let w=x1-x0+1,h=y1-y0+1;const bw=w,bh=Math.max(h,Math.ceil(w/1.5));
/* The renderer never draws the bug taller than about 760px, so anything bigger is repository
   weight only: it lands in every GitHub Pages build artifact. Cap it here, at the one place
   every bug image passes through. */
const k=Math.min(1,800/Math.max(bw,bh)),out=document.createElement('canvas');
out.width=Math.max(1,Math.round(bw*k));out.height=Math.max(1,Math.round(bh*k));
const g=out.getContext('2d');g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high';
g.drawImage(im,x0,y0,w,h,0,Math.round((out.height-h*k)/2),Math.round(w*k),Math.round(h*k));
bugData=out.toDataURL('image/png');bug=await loadImage(bugData);$('bugthumb').src=bugData;markBugState();}
function download(blob,name){const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),10000);}
function save(){try{build();download(new Blob([JSON.stringify(cfg(),null,2)],{type:'application/json'}),`${cfg().error_code}.json`);status('Project saved with its bug image.');}catch(e){status(e.message,true);}}
/* Rendered files live on releases, made by render.py inside the GitHub Action. */
function repoSlug(){const m=/^([\w-]+)\.github\.io$/i.exec(location.hostname);if(!m)return null;
const first=location.pathname.split('/').filter(Boolean)[0];return {owner:m[1],repo:first||`${m[1]}.github.io`};}
function releaseLine(box,text,...nodes){box.replaceChildren(document.createTextNode(text),...nodes);}
function link(text,href){const a=document.createElement('a');a.textContent=text;a.href=href;a.target='_blank';a.rel='noopener';return a;}
async function showRelease(){const box=$('releasebox'),code=($('errorcode').value.trim()||'CS1002').toUpperCase(),slug=repoSlug();
box.classList.remove('error');
if(!slug)return releaseLine(box,'Open this editor from its GitHub Pages address to see the rendered files here.');
const repo=`https://github.com/${slug.owner}/${slug.repo}`,actions=link('Action runs',`${repo}/actions/workflows/render.yml`);
box.textContent=`Looking for a rendered ${code}…`;
try{const r=await fetch(`https://api.github.com/repos/${slug.owner}/${slug.repo}/releases/tags/episode-${code}`);
if(r.status===404)return releaseLine(box,`${code} has not been rendered yet. Commit episodes/${code}.json and the action takes it from there. `,actions);
if(!r.ok)throw Error(`GitHub answered ${r.status}.`);
const z=await r.json(),when=new Date(z.published_at||z.created_at).toLocaleString();
const assets=(z.assets||[]).map(a=>link(a.name.endsWith('.mp4')?'Download MP4':'Download thumbnail',a.browser_download_url));
releaseLine(box,`${code} rendered ${when}. `,...assets,actions);}
catch(e){box.classList.add('error');releaseLine(box,e.message+' ',actions);}}
$('recheck').onclick=showRelease;
/* One button on a published page: commit the episode, run the action, bring the MP4 back. */
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let gh={slug:null,token:''};
async function api(path,init={},tries=3){let r,body;
for(let attempt=1;;attempt++){
r=await fetch(`https://api.github.com/repos/${gh.slug.owner}/${gh.slug.repo}${path}`,
{...init,headers:{Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28',Authorization:'Bearer '+gh.token,...(init.headers||{})}});
body=null;if(r.status!==204){try{body=await r.json();}catch{}}
if(r.status<500||attempt>=tries)break;/* 5xx here is GitHub's own hiccup, not the token. Back off, do not hammer. */
await sleep(attempt*attempt*5000);}
if(r.ok)return body;
const why=body&&body.message?` GitHub says: ${body.message}`:'',where=path||'the repository';
if(r.status>=500)throw Error(`GitHub itself failed on ${where} (${r.status}), so this is not your token or your settings.${why} Saving the episode already committed it, and that commit starts the render on its own — open the Actions tab to watch it, then press Render MP4 again in a few minutes to pick up the MP4.`);
if(r.status===401)throw Error(`GitHub did not accept the token itself (401 on ${where}). Paste the whole github_pat_ string again, and check it has not expired.${why}`);
if(r.status===403)throw Error(`The token is missing a permission (403 on ${where}). In the token settings give this repository Contents: read and write, and Actions: read and write.${why}`);
if(r.status===404)throw Error(`GitHub could not find ${where} (404). A fine-grained token that does not list this repository answers 404 as well, so check Repository access is Only select repositories with bug-archive-studio picked.${why}`);
throw Error(`GitHub answered ${r.status} on ${where}.${why}`);}
function episodeFile(code){const q=cfg();delete q.bug_data_url;q.bug=`../assets/${code}.png`;
const order=['error_code','message','filename','before','after','focus_line','music','bug'],out={};
for(const k of order)if(k in q)out[k]=q[k];return JSON.stringify(out,null,2)+'\n';}
/* One commit for a set of files. Each entry adds or replaces a path, or removes it with drop:true. */
async function commitFiles(message,files){const ref=await api('/git/ref/heads/main'),base=ref.object.sha,head=await api('/git/commits/'+base),tree=[];
for(const f of files){
if(f.drop){tree.push({path:f.path,mode:'100644',type:'blob',sha:null});continue;}
const blob=await api('/git/blobs',{method:'POST',body:JSON.stringify({content:f.content,encoding:f.encoding||'utf-8'})});
tree.push({path:f.path,mode:'100644',type:'blob',sha:blob.sha});}
const built=await api('/git/trees',{method:'POST',body:JSON.stringify({base_tree:head.tree.sha,tree})});
if(built.sha===head.tree.sha)return null;
const made=await api('/git/commits',{method:'POST',body:JSON.stringify({message,tree:built.sha,parents:[base]})});
await api('/git/refs/heads/main',{method:'PATCH',body:JSON.stringify({sha:made.sha})});
return made.sha;}
/* No [skip ci] here on purpose: episodes/*.json and assets/*.png are in the workflow's push
   trigger, so this commit is what starts the render. No dispatch call needed. */
const commitEpisode=code=>commitFiles(`${code} 에피소드 저장`,[
{path:`episodes/${code}.json`,content:episodeFile(code)},
{path:`assets/${code}.png`,content:bugData.split(',')[1],encoding:'base64'}]);
async function findRun(match,tries=20){for(let i=0;i<tries;i++){await sleep(3000);
const z=await api('/actions/workflows/render.yml/runs?branch=main&per_page=10');
const run=(z.workflow_runs||[]).find(match);if(run)return run;}
return null;}
async function watchRun(run,code,since){for(let i=0;i<150;i++){const z=await api('/actions/runs/'+run.id);
if(z.status==='completed'){if(z.conclusion!=='success')throw Error(`The action finished as ${z.conclusion}. Open the run to see why.`);return z;}
step(`Rendering ${code} on GitHub… ${Math.round((Date.now()-since)/1000)}s`);await sleep(4000);}
throw Error('The action is taking too long. Check the run on GitHub.');}
async function runAction(code,since,sha){
/* The commit above already started the workflow. Watch that run. Only a commit that changed
   nothing leaves no run to watch, and that is the one case worth dispatching by hand. */
let run=sha?await findRun(r=>r.head_sha===sha):null;
if(!run){await api('/actions/workflows/render.yml/dispatches',{method:'POST',body:JSON.stringify({ref:'main',inputs:{episode:code}})});
run=await findRun(r=>r.event==='workflow_dispatch'&&new Date(r.created_at)>=since);}
if(!run)throw Error('The action did not start. Check that Actions are enabled for this repository.');
return watchRun(run,code,since);}
async function existingRelease(code){try{const z=await api('/releases/tags/episode-'+code);
return (z.assets||[]).some(a=>a.name.endsWith('.mp4'))?z:null;}catch{return null;}}
async function fetchRelease(code){for(let i=0;i<10;i++){try{const z=await api('/releases/tags/episode-'+code);
if((z.assets||[]).some(a=>a.name.endsWith('.mp4')))return z;}catch{}await sleep(3000);}
throw Error('The render finished but the release has no MP4 yet.');}
const openRender=()=>{if(!$('offline').open)$('offline').showModal();};
/* Progress and failures belong in the dialog: it stays open and covers the status line behind it. */
function step(text,error=false){const box=$('releasebox');box.classList.toggle('error',error);box.textContent=text;status(text,error);}
async function renderOnActions(){const slug=repoSlug();
openRender();
if(!slug)return step('This editor is not on its GitHub Pages address, so it cannot reach the repository. Save the project and commit it, or render on your own PC.',true);
const token=($('ghtoken').value||'').trim();
if(!token){$('ghtoken').focus();return step('Paste a GitHub token in the box above, then press Render MP4 again.',true);}
if(!bugData)return step(`${($('errorcode').value||'This episode').trim()} has no bug PNG. Generate one or choose a file first.`,true);
gh={slug,token};try{sessionStorage.setItem('bugarchive-ghtoken',token);}catch{}
activeJob=true;$('render').disabled=true;$('startrender').disabled=true;$('downloads').replaceChildren();
try{model=build();const code=model.error_code;
step(`Checking the token on ${slug.owner}/${slug.repo}…`);
const repo=await api('');
if(!repo.permissions||!repo.permissions.push)throw Error(`This token can read ${slug.owner}/${slug.repo} but cannot write to it. Open the token settings, set Repository access to this repository, and set Contents to read and write.`);
step(`Saving ${code} to ${slug.owner}/${slug.repo}…`);
const since=new Date(Date.now()-20000),sha=await commitEpisode(code);
let release=sha?null:await existingRelease(code);
if(release)step(`${code} is unchanged since its last render. Fetching that MP4…`);
else{step(sha?'Saved. That commit starts render.py on GitHub…':`${code} was already saved. Starting render.py on GitHub…`);
await runAction(code,since,sha);
step('Render finished. Fetching the MP4…');
release=await fetchRelease(code);}
const video=release.assets.find(a=>a.name.endsWith('.mp4'));
try{const r=await fetch(video.browser_download_url);if(!r.ok)throw Error('no cors');download(await r.blob(),video.name);}
catch{link('',video.browser_download_url).click();}
$('downloads').replaceChildren(...release.assets.map(a=>{const l=link(a.name.endsWith('.mp4')?'Download MP4 again':'Download thumbnail',a.browser_download_url);l.download='';return l;}));
const done=`${code} rendered by render.py and downloaded.${sha?' The episode and its bug PNG are committed too.':''} `;
$('releasebox').classList.remove('error');
releaseLine($('releasebox'),done,...release.assets.map(a=>link(a.name.endsWith('.mp4')?'Download MP4 again':'Download thumbnail',a.browser_download_url)));
status(done);}
catch(e){step(e.message,true);}
finally{activeJob=false;$('startrender').disabled=false;markBugState();}}
$('startrender').onclick=()=>renderOnActions().catch(e=>step(e.message,true));
$('save').onclick=save;$('offlineSave').onclick=save;$('closeDialog').onclick=()=>$('offline').close();$('open').onclick=()=>$('projectfile').click();$('projectfile').onchange=async e=>{try{if(e.target.files[0])await setConfig(JSON.parse(await e.target.files[0].text()));}catch(e){status(e.message,true);}};
$('choosebug').onclick=()=>$('bugfile').click();$('bugfile').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>8*1024*1024)throw Error('Use a PNG smaller than 8 MB.');const reader=new FileReader();reader.onload=async()=>{try{await setBug(reader.result);update();}catch(e){status(e.message,true);}};reader.readAsDataURL(f);}catch(e){status(e.message,true);}};
for(const id of ['before','after','errorcode','message','filename','focus'])$(id).oninput=update;
$('time').oninput=()=>{playing=false;bgmStop();$('play').textContent='Play';time=Number($('time').value);$('clock').textContent=`${time.toFixed(2)} / 12s`;draw();};$('guides').onchange=()=>draw();document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{$('time').value=b.dataset.time;$('time').oninput();});
/* Background music: a list you keep in the music folder, chosen per episode or left to chance. */
let musicChoice='random',tracks=[],bgm=null,bgmSrc='';
const MUSIC_GAIN=.22;
const mstatus=(s,error=false)=>{$('musicstatus').textContent=s;$('musicstatus').classList.toggle('error',error);};
const trackByName=n=>tracks.find(t=>t.file===n)||null;
function fnv1a(text){let h=0x811C9DC5;for(const b of new TextEncoder().encode(text)){h^=b;h=Math.imul(h,0x01000193)>>>0;}return h>>>0;}
/* Every error code keeps its track for good: the score depends on the code and that one file name,
   so adding or removing other tracks never moves an episode to a different song. render.py matches. */
function pickRandom(){if(!tracks.length)return null;const code=($('errorcode').value.trim()||'CS1002').toUpperCase();
return tracks.reduce((best,t)=>{const s=fnv1a(code+'|'+t.file);const b=fnv1a(code+'|'+best.file);
return s>b||(s===b&&t.file>best.file)?t:best;});}
function resolvedTrack(){if(musicChoice==='random')return pickRandom();return musicChoice?trackByName(musicChoice):null;}
function musicLabel(){if(!musicChoice)return'None';const t=resolvedTrack();
if(musicChoice==='random')return t?`Random · ${t.file}`:'Random · no tracks yet';
return t?t.file:`${musicChoice} · missing`;}
function refreshMusic(){$('musicnow').textContent=musicLabel();}
async function loadTracks(){if(location.protocol==='file:')return tracks;
const source=localStudio?'api/music':'music/index.json';
try{const r=await fetch(source,{cache:'no-store'});if(!r.ok)throw 0;tracks=(await r.json()).tracks||[];}catch{tracks=[];}
refreshMusic();return tracks;}
function trackRow(label,value,track){const b=document.createElement('button');b.className='trackrow'+(musicChoice===value?' on':'');
const dot=document.createElement('span');dot.className='dot';
const name=document.createElement('span');name.className='name';name.textContent=label;
b.append(dot,name);
if(track){const size=document.createElement('span');size.className='size';size.textContent=`${(track.size/1048576).toFixed(1)} MB`;
const drop=document.createElement('button');drop.className='trackdrop';drop.textContent='✕';drop.title=`Remove ${track.file}`;
drop.onclick=e=>{e.stopPropagation();removeTrack(track).catch(err=>mstatus(err.message,true));};
b.append(size,drop);}
b.onclick=()=>{musicChoice=value;refreshMusic();update();drawTracks();mstatus(value?`Using ${musicLabel()}.`:'The render keeps only the sound effects.');};
return b;}
function drawTracks(){const list=$('tracklist');
list.replaceChildren(trackRow('None · effects only','',null),trackRow('Random · picked from this list','random',null),
...tracks.map(t=>trackRow(t.file,t.file,t)));}
async function openMusic(){$('musicdlg').showModal();mstatus('Reading the music folder…');
await loadTracks();drawTracks();
mstatus(location.protocol==='file:'?'A page opened from a file cannot read the music folder. Use START_STUDIO.bat or the published site.'
:tracks.length?`${tracks.length} track${tracks.length>1?'s':''} in the music folder.`:'No tracks yet. Add one below.',location.protocol==='file:');}
async function saveTrack(name,dataUrl,bytes){
if(localStudio){const r=await fetch('api/music',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,data_url:dataUrl})});
const z=await r.json();if(!r.ok)throw Error(z.error||'Could not save the track.');tracks=z.tracks||[];return;}
const slug=repoSlug();if(!slug)throw Error('Open the published site to add tracks from the browser.');
const token=($('ghtoken').value||'').trim();if(!token)throw Error('Adding a track commits it to the repository. Paste a GitHub token in the Render MP4 window first.');
gh={slug,token};
const next=[...tracks.filter(t=>t.file!==name),{file:name,path:'music/'+name,size:bytes}].sort((a,b)=>a.file.localeCompare(b.file));
await commitFiles(`배경음 ${name} 추가 [skip ci]`,[{path:'music/'+name,content:dataUrl.split(',')[1],encoding:'base64'},
{path:'music/index.json',content:JSON.stringify({tracks:next},null,2)+'\n'}]);
tracks=next;}
async function removeTrack(track){if(!confirm(`Remove ${track.file} from the music folder?`))return;
mstatus(`Removing ${track.file}…`);
if(localStudio){const r=await fetch('api/music/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:track.file})});
const z=await r.json();if(!r.ok)throw Error(z.error||'Could not remove the track.');tracks=z.tracks||[];}
else{const slug=repoSlug();if(!slug)throw Error('Open the published site to manage tracks from the browser.');
const token=($('ghtoken').value||'').trim();if(!token)throw Error('Removing a track commits to the repository. Paste a GitHub token in the Render MP4 window first.');
gh={slug,token};const next=tracks.filter(t=>t.file!==track.file);
await commitFiles(`배경음 ${track.file} 삭제 [skip ci]`,[{path:'music/'+track.file,drop:true},
{path:'music/index.json',content:JSON.stringify({tracks:next},null,2)+'\n'}]);
tracks=next;}
if(musicChoice===track.file)musicChoice='';
drawTracks();refreshMusic();update();mstatus(`${track.file} removed.`);}
$('musiclist').onclick=()=>openMusic().catch(e=>mstatus(e.message,true));
$('closeMusic').onclick=()=>$('musicdlg').close();
$('addtrack').onclick=()=>$('musicfile').click();
$('musicfile').onchange=async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;
try{if(f.size>40*1024*1024)throw Error('Use a track under 40 MB.');
const name=f.name.replace(/[^\w.\- ]+/g,'_');
mstatus(`Adding ${name}…`);
const dataUrl=await blobDataUrl(f);
await saveTrack(name,dataUrl,f.size);
musicChoice=name;drawTracks();refreshMusic();update();mstatus(`${name} added and selected.`);}
catch(err){mstatus(err.message,true);}};
/* The preview plays the same track under the effects, at the gain the render uses. */
function bgmStart(){const t=resolvedTrack();if(!t||!$('sound').checked)return;
if(!bgm||bgmSrc!==t.path){bgm=new Audio(t.path);bgm.loop=true;bgmSrc=t.path;}
bgm.volume=MUSIC_GAIN;try{bgm.currentTime=time%(bgm.duration||12);}catch{}
bgm.play().catch(()=>{});}
function bgmStop(){if(bgm)bgm.pause();}
/* Preview sound. Same cues, times and shapes the rendered MP4 carries, rebuilt with Web Audio. */
const CUES=[[3,.18,680,.12,9],[4,.18,680,.12,9],[5,.18,680,.12,9],[6,.23,880,.12,9],[6.1,.32,1174,.12,9],[7.5,.18,1400,.07,9],[8.6,.1,1100,.14,9],[9.35,.35,520,.12,9],[10.45,.6,660,.12,6],[10.55,.6,880,.12,6],[10.68,.6,1320,.12,6]];
const WHOOSH=[[7.55,.8],[8.9,.5]];
let ac,master;
function audio(){if(!ac){const Ctx=window.AudioContext||window.webkitAudioContext;if(!Ctx)return null;ac=new Ctx();master=ac.createGain();master.gain.value=1;master.connect(ac.destination);}if(ac.state==='suspended')ac.resume();return ac;}
function tone(dur,freq,amp,decay){const c=audio();if(!c)return;const t=c.currentTime,o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=freq;
g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(amp,t+.006);g.gain.setTargetAtTime(0,t+.006,1/decay);
g.gain.setTargetAtTime(0,t+dur,.004);o.connect(g);g.connect(master);o.start(t);o.stop(t+dur+.04);}
function whoosh(dur){const c=audio();if(!c)return;const n=Math.floor(c.sampleRate*dur),b=c.createBuffer(1,n,c.sampleRate),d=b.getChannelData(0);
for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*.03*Math.sin(Math.PI*i/n)**2;
const s=c.createBufferSource(),lp=c.createBiquadFilter();s.buffer=b;lp.type='lowpass';lp.frequency.value=1900;
s.connect(lp);lp.connect(master);s.start();}
function playCues(from,to){if(!$('sound').checked||to<=from)return;
for(const [at,dur,freq,amp,decay]of CUES)if(at>from&&at<=to)tone(dur,freq,amp,decay);
for(const [at,dur]of WHOOSH)if(at>from&&at<=to)whoosh(dur);}
$('sound').onchange=()=>{try{localStorage.setItem('bugarchive-sound',$('sound').checked?'1':'0');}catch{}if($('sound').checked){audio();if(playing)bgmStart();}else bgmStop();};
$('play').onclick=()=>{playing=!playing;if(playing&&time>11.9)time=0;if(playing&&$('sound').checked)audio();if(playing)bgmStart();else bgmStop();$('play').textContent=playing?'Pause':'Play';last=performance.now();};function loop(now){if(playing&&ready){const from=time;time+=(now-last)/1000;if(time>=12){time=11.99;playing=false;$('play').textContent='Play';bgmStop();}playCues(from,time);$('time').value=time;$('clock').textContent=`${time.toFixed(2)} / 12s`;try{draw();}catch(e){playing=false;status(e.message,true);}}last=now;requestAnimationFrame(loop);}requestAnimationFrame(loop);
/* LOCKED thumbnail. Its own layout, not a video frame: silhouette, rim glow, big error code. */
function spaced(c,text,cx,baseline,size,color,gap){c.font=`${size}px ArchiveMono`;c.fillStyle=color;c.textAlign='left';c.textBaseline='alphabetic';
const chars=[...text],w=chars.map(ch=>c.measureText(ch).width),total=w.reduce((a,b)=>a+b,0)+gap*(chars.length-1);
let x=cx-total/2;chars.forEach((ch,i)=>{c.fillText(ch,x,baseline);x+=w[i]+gap;});return total;}
function bugMask(color,box){if(!bug)return null;const m=document.createElement('canvas');m.width=1080;m.height=1920;const d=m.getContext('2d');
const scale=Math.min(box.w/bug.width,box.h/bug.height),w=bug.width*scale,h=bug.height*scale;
d.drawImage(bug,box.cx-w/2,box.cy-h/2,w,h);d.globalCompositeOperation='source-in';d.fillStyle=color;d.fillRect(0,0,1080,1920);return m;}
function thumbnailCanvas(){const T=document.createElement('canvas');T.width=1080;T.height=1920;const c=T.getContext('2d'),code=model.error_code;
const g=c.createRadialGradient(540,900,60,540,900,1250);g.addColorStop(0,'#141c25');g.addColorStop(1,'#080c11');c.fillStyle=g;c.fillRect(0,0,1080,1920);
c.fillStyle='#222d39';for(let x=36;x<1080;x+=48)for(let y=36;y<1920;y+=48)c.fillRect(x,y,2,2);
c.strokeStyle='#2c3844';c.lineWidth=2;
for(const [x,y]of[[64,74],[1016,74],[64,1846],[1016,1846]]){c.beginPath();c.moveTo(x-13,y);c.lineTo(x+13,y);c.moveTo(x,y-13);c.lineTo(x,y+13);c.stroke();}
spaced(c,'BUG ARCHIVE',96+118,168,29,'#77858f',7);
c.strokeStyle='#4d5b66';c.lineWidth=3;c.beginPath();c.moveTo(96,196);c.lineTo(160,196);c.stroke();
c.beginPath();c.roundRect(88,250,904,1450,16);c.strokeStyle='#2b3742';c.lineWidth=2;c.stroke();
c.strokeStyle='#cfdae2';c.lineWidth=4;
for(const [x,y,sx,sy]of[[120,282,1,1],[960,282,-1,1],[120,1668,1,-1],[960,1668,-1,-1]]){c.beginPath();c.moveTo(x,y+58*sy);c.lineTo(x,y);c.lineTo(x+58*sx,y);c.stroke();}
const lw=spaced(c,'LOCKED',540,378,36,'#e9eff3',13);
c.strokeStyle='#63707b';c.lineWidth=2;c.beginPath();
c.moveTo(540-lw/2-90,368);c.lineTo(540-lw/2-26,368);c.moveTo(540+lw/2+26,368);c.lineTo(540+lw/2+90,368);c.stroke();
const box={cx:540,cy:880,w:744,h:800},glowMask=bugMask('#c3ff55',box),solid=bugMask('#07100a',box);
if(glowMask&&solid){c.save();for(const [blur,alpha]of[[38,.34],[16,.7],[6,1]]){c.filter=`blur(${blur}px)`;c.globalAlpha=alpha;c.drawImage(glowMask,0,0);}c.restore();
c.drawImage(solid,0,0);}
spaced(c,code,540,1470,156,'#f4f1e8',10);
c.strokeStyle='#55616c';c.lineWidth=3;c.beginPath();c.moveTo(480,1546);c.lineTo(600,1546);c.stroke();
return T;}
$('thumbnail').onclick=()=>{try{model=build();thumbnailCanvas().toBlob(b=>download(b,`${model.error_code}-locked.png`),'image/png');status('LOCKED thumbnail saved.');}catch(e){status(e.message,true);}};
$('longexample').onclick=()=>setConfig(longExample()).catch(e=>status(e.message,true));function longExample(){const a=['using UnityEngine;','','public class Counter : MonoBehaviour','{','    private int score = 0;','    private int bonus = 5;','','    void Start()','    {','        score = 10;','        score += bonus;','        PrintScore();','    }','','    void PrintScore()','    {','        Debug.Log("Score")','        Debug.Log(score);','    }','','    void ResetScore()','    { score = 0; }','','}'];const b=[...a];b[16]+=';';return {...defaults,before:a,after:b,bug_data_url:bugData};}
$('render').onclick=async()=>{if(activeJob)return;if(!localStudio)return renderOnActions().catch(e=>{activeJob=false;$('startrender').disabled=false;markBugState();step(e.message,true);});try{model=build();activeJob=true;$('render').disabled=true;status('Rendering MP4…');const r=await fetch('api/render',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(cfg())});const result=await r.json();if(!r.ok)throw Error(result.error||'Render failed.');const poll=async()=>{try{const q=await fetch('api/job/'+result.job),z=await q.json();if(z.status==='done'){status(z.archive?`MP4 ready. The episode was archived as ${z.archive} with ${z.bug}.`:'MP4 and thumbnail are ready.');$('downloads').replaceChildren();for(const [name,url]of[['Download MP4',z.video],['Download thumbnail',z.thumbnail]]){const a=document.createElement('a');a.textContent=name;a.href=url;a.download='';$('downloads').append(a);}activeJob=false;$('render').disabled=false;}else if(z.status==='failed')throw Error(z.error||'Render failed.');else{status(z.progress||'Rendering MP4…');setTimeout(poll,1000);}}catch(e){activeJob=false;$('render').disabled=false;status(e.message,true);}};poll();}catch(e){activeJob=false;$('render').disabled=false;status(e.message,true);}};
/* Episode browser for the episodes folder of the running studio. */
const epstatus=(s,error=false)=>{$('episodestatus').textContent=s;$('episodestatus').classList.toggle('error',error);};
function blobDataUrl(blob){return new Promise((resolve,reject)=>{const fr=new FileReader();fr.onload=()=>resolve(fr.result);fr.onerror=()=>reject(Error('Could not read the bug PNG.'));fr.readAsDataURL(blob);});}
async function listEpisodes(){if(location.protocol==='file:')throw Error('A page opened from a file cannot read the episodes folder. Use START_STUDIO.bat, the published site, or open a saved JSON.');
const source=localStudio?'api/episodes':'episodes/index.json';let r;
try{r=await fetch(source,{cache:'no-store'});}catch{throw Error('Could not reach the episode list. Check the connection, or restart START_STUDIO.bat.');}
const z=await r.json().catch(()=>({}));
if(!r.ok)throw Error(z.error||(localStudio?'Could not read the episodes folder.':'This site has no episodes/index.json yet. Run python server.py --index and publish it.'));
return z.episodes||[];}
async function loadEpisode(row){epstatus(`Loading ${row.file}…`);
const r=await fetch(row.path||'episodes/'+encodeURIComponent(row.file),{cache:'no-store'});if(!r.ok)throw Error(`Could not read ${row.file}.`);
const q=await r.json();
if(row.bug){const png=await fetch(row.bug);if(!png.ok)throw Error(`Could not read ${row.bug}.`);q.bug_data_url=await blobDataUrl(await png.blob());}
try{await setConfig(q);}catch(e){throw Error(`${row.file} is not a complete episode. ${e.message}.`);}$('episodes').close();
status(row.bug?`Loaded ${row.file} with its bug image.`:`Loaded ${row.file}. It has no bug PNG yet, so rendering is off until you add one.`);}
function episodeRow(row){const b=document.createElement('button');b.className='episoderow'+(row.bug?'':' nobug');
const code=document.createElement('b');code.textContent=row.error_code||row.file;
if(row.order){const n=document.createElement('i');n.className='epnum';n.textContent=row.order;b.append(n);}
const meta=document.createElement('span');meta.textContent=`${row.filename} · ${row.lines} lines`;
const msg=document.createElement('em');msg.textContent=row.message;
b.append(code,meta,msg);b.onclick=()=>loadEpisode(row).then(syncPosition).catch(e=>epstatus(e.message,true));return b;}
function episodeNodes(rows){/* Rows arrive in checklist order; break them into the same tiers the checklist uses. */
const out=[];let tier=null;
for(const row of rows){const t=row.tier||0;
if(t!==tier){tier=t;const h=document.createElement('p');h.className='tierhead';h.textContent=t?`TIER ${t}`:'NOT ON THE CHECKLIST';out.push(h);}
out.push(episodeRow(row));}
return out;}
$('loadepisode').onclick=async()=>{$('episodelist').replaceChildren();epstatus('Reading the episodes folder…');$('episodes').showModal();
try{const rows=episodeCache=await listEpisodes();$('episodelist').replaceChildren(...episodeNodes(rows));epstatus(rows.length?`${rows.length} episodes, in checklist order. Pick one to load it into the editor.`:'The episodes folder has no JSON yet.');}
catch(e){epstatus(e.message,true);}};
$('closeEpisodes').onclick=()=>$('episodes').close();
$('episodeopen').onclick=()=>{$('episodes').close();$('projectfile').click();};
/* Prev / Next walk the episode list in checklist order, so building a series in order does not
   mean reopening the picker for every single one. The list is fetched once and reused. */
let episodeCache=null;
async function orderedEpisodes(){if(!episodeCache)episodeCache=await listEpisodes();return episodeCache;}
function syncPosition(){if(!episodeCache)return;
const code=($('errorcode').value||'').trim().toUpperCase();
showPosition(episodeCache,episodeCache.findIndex(r=>(r.error_code||'').toUpperCase()===code));}
function showPosition(rows,index){const box=$('episodepos');
if(!rows||index<0){box.textContent='';box.title='';return;}
const row=rows[index];box.textContent=`${index+1} / ${rows.length}`;
box.title=`${row.error_code}${row.order?` · checklist #${row.order}`:''}`;}
async function stepEpisode(delta){const code=($('errorcode').value||'').trim().toUpperCase();
const rows=await orderedEpisodes();
if(!rows.length)throw Error('The episodes folder has no JSON yet.');
const at=rows.findIndex(r=>(r.error_code||'').toUpperCase()===code);
/* Unknown code in the editor: Next starts at the top, Prev at the end. */
const next=at<0?(delta>0?0:rows.length-1):at+delta;
if(next<0)throw Error(`${code} is the first episode on the checklist.`);
if(next>=rows.length)throw Error(`${code} is the last episode on the checklist.`);
await loadEpisode(rows[next]);showPosition(rows,next);}
const stepper=delta=>()=>{const b=[$('prevepisode'),$('nextepisode')];b.forEach(x=>x.disabled=true);
stepEpisode(delta).catch(e=>status(e.message,true)).finally(()=>b.forEach(x=>x.disabled=false));};
$('prevepisode').onclick=stepper(-1);
$('nextepisode').onclick=stepper(1);
/* AI bug generation. The concept stays the established Bug Archive family; only one slight variation changes. */
const MOTIFS={CS1002:'one tiny black semicolon-shaped mouth, exactly like the reference',CS1003:'holding one lime puzzle piece with an obviously missing matching slot',CS0103:'searching through one tiny magnifying glass',CS0246:'holding an empty name-tag frame with a small question symbol shape (no readable text)',CS1061:'trying one rounded key that visibly does not fit a tiny socket',CS0029:'holding two visibly mismatched rounded connector pieces',CS0161:'tossing one curved return-arrow boomerang',CS0165:'holding one empty translucent value capsule',CS0019:'holding two rounded puzzle pieces whose operator-shaped edges cannot meet',CS1503:'trying to place one round plug into a square socket',CS0201:'holding one unfinished dotted path that stops abruptly',CS0111:'holding two identical tiny toy blasters, one in each hand, clearly showing an accidental duplicate',CS0117:'checking one small empty name plate',CS0120:'reaching from a tiny pedestal toward an instance object below',CS1525:'surprised by one wrong puzzle token floating beside it',CS1729:'holding a constructor-shaped box with the wrong number of round slots',CS7036:'holding an empty required-argument socket with one missing plug'};
const VARIATIONS=[['auto','Auto (slight)'],['cheeks','Rounder cheeks'],['antennae','Shorter antennae'],['pose','Playful pose'],['accessory','Small accessory'],['none','No variation']];
const VARIATION_TEXT={cheeks:'slightly rounder cheeks',antennae:'slightly shorter antennae',pose:'a playful pose',accessory:'one small accessory',none:''};
const autoVariation=code=>['cheeks','antennae','pose','accessory'][[...code].reduce((a,c)=>a+c.charCodeAt(0),0)%4];
const aistatus=(s,error=false)=>{$('aistatus').textContent=s;$('aistatus').classList.toggle('error',error);};
function inferredMotif(message){const m=message.toLowerCase();if(/already defines|already contains|same parameter|duplicate/.test(m))return 'holding two identical tiny objects, one in each hand, to directly symbolize an accidental duplicate';if(/could not be found|does not exist|not found/.test(m))return 'searching through one tiny magnifying glass for a clearly missing object';if(/cannot convert|implicitly convert|argument/.test(m))return 'trying to join one round plug to one square socket';if(/inaccessible|protection level|private/.test(m))return 'standing behind one tiny rounded padlock';if(/ambiguous/.test(m))return 'looking between two equally sized direction arrows';if(/return/.test(m))return 'catching one curved return-arrow boomerang';if(/expected|unexpected|invalid token/.test(m))return 'holding one puzzle piece beside a visibly wrong or missing slot';if(/static|object reference/.test(m))return 'reaching from a small pedestal toward one separate instance object';return 'interacting with one simple lime-and-charcoal coding puzzle prop that directly symbolizes the error';}
function bugPrompt(){const code=($('errorcode').value.trim()||'CS1002').toUpperCase(),msg=$('message').value.trim(),concept=$('concept').value.trim()||`${code} — ${msg||'; expected'}`,motif=MOTIFS[code]||inferredMotif(msg);
return [`Create a new pose of the EXACT SAME Bug Archive mascot species shown in this public reference image: https://kevin04261004.github.io/bug-archive-studio/assets/CS1002.png . Inspect that reference before generating.`,`Identity lock: nearly perfect circular fluorescent yellow-lime head/body with no separate torso; two very long thin lime stalk antennae ending in oversized round bulbs; two huge vertical black oval eyes with one small white highlight each; tiny black dot nose; tiny black semicolon-shaped mouth; exactly four small lime oval feet/side nubs; thin dark plum outline; smooth 2D chibi vector/anime rendering; strong white glossy highlights at upper-left; subtle lime edge shading. Preserve these proportions, face placement, outline weight, palette and rendering so it is unmistakably the same mascot, not a redesigned insect.`,`Episode concept: ${concept}. Give it one clear visual joke: ${motif}. The prop or pose must make the error idea understandable at a glance, while the mascot anatomy and face stay unchanged.`,`Do not make a generic beetle, caterpillar, alien, robot, bee, or monster. No wings, shell, fur, extra limbs, clothing, realistic anatomy, gradients outside the character, or arbitrary decorative markings.`,`One centered full-body character, entirely visible with a clear margin, genuinely transparent PNG background. No words, letters, digits, error code, caption, card, floor, scenery, border, or cast shadow.`].join(' ');}
function refreshPrompt(){const code=($('errorcode').value.trim()||'CS1002').toUpperCase();$('concept').placeholder=`${code} — ${$('message').value.trim()||'; expected'}`;$('aiprompt').value=bugPrompt();}
function dataUrlBlob(url){const bin=atob(url.split(',')[1]),bytes=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);return new Blob([bytes],{type:'image/png'});}
async function apiFetch(url,init){try{return await fetch(url,init);}catch{throw Error('The image API could not be reached. Open START_STUDIO.bat and retry from http://127.0.0.1:8765, then check the key and the network.');}}
async function openaiBug(key,prompt,ref){let url='https://api.openai.com/v1/images/generations',init={method:'POST',headers:{Authorization:'Bearer '+key}};
if(ref){const form=new FormData();for(const [k,v]of[['model','gpt-image-1'],['prompt',prompt],['size','1024x1024'],['background','transparent'],['output_format','png'],['quality','high'],['n','1']])form.append(k,v);form.append('image[]',dataUrlBlob(ref),'CS1002.png');url='https://api.openai.com/v1/images/edits';init.body=form;}
else{init.headers['Content-Type']='application/json';init.body=JSON.stringify({model:'gpt-image-1',prompt,size:'1024x1024',background:'transparent',output_format:'png',quality:'high',n:1});}
const r=await apiFetch(url,init),z=await r.json().catch(()=>({}));if(!r.ok)throw Error(z.error?.message||`OpenAI request failed (${r.status}).`);const b64=z.data?.[0]?.b64_json;if(!b64)throw Error('OpenAI returned no image. Try again.');return b64;}
async function geminiBug(key,prompt,ref){const parts=[{text:prompt}];if(ref)parts.unshift({inline_data:{mime_type:'image/png',data:ref.split(',')[1]}});
const r=await apiFetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent',{method:'POST',headers:{'Content-Type':'application/json','x-goog-api-key':key},body:JSON.stringify({contents:[{parts}]})}),z=await r.json().catch(()=>({}));
if(!r.ok)throw Error(z.error?.message||`Gemini request failed (${r.status}).`);const part=(z.candidates?.[0]?.content?.parts||[]).find(p=>p.inlineData||p.inline_data),data=(part?.inlineData||part?.inline_data)?.data;if(!data)throw Error('Gemini returned no image. Try again.');return data;}
function pixels(im){const t=document.createElement('canvas');t.width=im.width;t.height=im.height;const d=t.getContext('2d',{willReadFrequently:true});d.drawImage(im,0,0);return {canvas:t,d,img:d.getImageData(0,0,im.width,im.height)};}
const opaque=im=>{const px=pixels(im).img.data;for(let i=3;i<px.length;i+=4)if(px[i]<255)return false;return true;};
function cutout(im){const {canvas,d,img}=pixels(im),w=im.width,h=im.height,px=img.data,tol=44;let r=0,g=0,b=0,n=0;
for(let x=0;x<w;x++)for(const y of[0,h-1]){const i=(y*w+x)*4;r+=px[i];g+=px[i+1];b+=px[i+2];n++;}
for(let y=0;y<h;y++)for(const x of[0,w-1]){const i=(y*w+x)*4;r+=px[i];g+=px[i+1];b+=px[i+2];n++;}
r/=n;g/=n;b/=n;const seen=new Uint8Array(w*h),alpha=new Float32Array(w*h).fill(1),stack=[];
for(let x=0;x<w;x++)stack.push(x,x+(h-1)*w);for(let y=0;y<h;y++)stack.push(y*w,y*w+w-1);
while(stack.length){const p=stack.pop();if(seen[p])continue;seen[p]=1;const i=p*4,dist=Math.max(Math.abs(px[i]-r),Math.abs(px[i+1]-g),Math.abs(px[i+2]-b));
if(dist>tol*2)continue;alpha[p]=dist<=tol?0:(dist-tol)/tol;const x=p%w,y=(p-x)/w;
if(x>0)stack.push(p-1);if(x<w-1)stack.push(p+1);if(y>0)stack.push(p-w);if(y<h-1)stack.push(p+w);}
let cleared=0;for(let p=0;p<w*h;p++)if(alpha[p]<1){px[p*4+3]=Math.round(px[p*4+3]*alpha[p]);cleared++;}
if(cleared<w*h*0.05)throw Error('The generated image has no transparent background and no flat background to remove. Ask for a transparent PNG and try again.');
d.putImageData(img,0,0);return canvas.toDataURL('image/png');}
$('aibug').onclick=()=>{refreshPrompt();aistatus('');$('aigen').showModal();};
$('closeAi').onclick=()=>$('aigen').close();
$('variation').replaceChildren(...VARIATIONS.map(([v,label])=>{const o=document.createElement('option');o.value=v;o.textContent=label;return o;}));
for(const id of ['concept','errorcode','message'])$(id).addEventListener('input',refreshPrompt);
for(const id of ['variation','useref'])$(id).addEventListener('change',refreshPrompt);
$('provider').onchange=()=>{$('apikey').placeholder=$('provider').value==='openai'?'sk-...':'AIza...';try{localStorage.setItem('bugarchive-provider',$('provider').value);}catch{}};
$('generate').onclick=async()=>{const key=$('apikey').value.trim();if(!key)return aistatus('Paste an image API key.',true);
$('generate').disabled=true;aistatus('Generating one bug. This usually takes 15–40 seconds.');
try{sessionStorage.setItem('bugarchive-imagekey',key);}catch{}
try{const ref=$('useref').checked?STUDIO_ASSETS.CS1002:null,b64=$('provider').value==='openai'?await openaiBug(key,$('aiprompt').value,ref):await geminiBug(key,$('aiprompt').value,ref);
let url='data:image/png;base64,'+b64,trimmed=false;const im=await loadImage(url);
if(opaque(im)){url=cutout(im);trimmed=true;}
await setBug(url);update();$('aithumb').src=bugData;$('aithumb').hidden=false;$('aisave').hidden=false;
aistatus(trimmed?'Bug applied. Its flat background was removed to get real transparency.':'Bug applied to the preview and to the episode.');status('AI bug generated and applied.');}
catch(e){aistatus(e.message,true);}finally{$('generate').disabled=false;}};
$('aisave').onclick=()=>download(dataUrlBlob(bugData),`${($('errorcode').value.trim()||'bug').toUpperCase()}.png`);
async function init(){try{await Promise.all([new FontFace('ArchiveMono',`url(${STUDIO_ASSETS.DejaVuSansMono})`).load(),new FontFace('ArchiveSans',`url(${STUDIO_ASSETS.DejaVuSans})`).load()].map(async p=>document.fonts.add(await p)));hosts=await Promise.all([0,1,2,3,4].map(i=>loadImage(STUDIO_ASSETS['host-'+i])));await setBug(STUDIO_ASSETS.CS1002);ready=true;let q=defaults;try{const saved=localStorage.getItem('bugarchive-v2');if(saved)q=JSON.parse(saved);}catch{}await setConfig(q);try{$('sound').checked=localStorage.getItem('bugarchive-sound')!=='0';const saved=localStorage.getItem('bugarchive-provider');if(saved)$('provider').value=saved;const key=sessionStorage.getItem('bugarchive-imagekey');if(key)$('apikey').value=key;const gt=sessionStorage.getItem('bugarchive-ghtoken');if(gt)$('ghtoken').value=gt;}catch{}$('provider').onchange();refreshPrompt();try{localStudio=['127.0.0.1','localhost'].includes(location.hostname)&&(await fetch('api/health',{cache:'no-store'})).ok;}catch{localStudio=false;}
$('mode').textContent=localStudio?'LOCAL RENDER STUDIO':location.protocol==='file:'?'OFFLINE EDITOR':'WEB EDITOR';await loadTracks();if(document.modelContext?.registerTool)document.modelContext.registerTool({name:'inspect_episode',description:'Read the current episode and preview layout.',inputSchema:{type:'object',properties:{}},annotations:{readOnlyHint:true},execute:()=>({error_code:model?.error_code,lines:model?.count,visible:model?.visible,time})});}catch(e){status(e.message,true);}}init();
