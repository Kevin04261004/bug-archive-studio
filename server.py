"""Loopback-only desktop bridge for index.html and the Python MP4 renderer."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,re,subprocess,sys,uuid,threading,webbrowser,argparse,base64
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8765);ap.add_argument('--no-browser',action='store_true');ap.add_argument('--index',action='store_true',help='Only refresh episodes/index.json and exit');args=ap.parse_args()
jobs={};pool=ThreadPoolExecutor(max_workers=1);lock=threading.Lock()
def render(job,config):
    folder=ROOT/'output'/'jobs'/job;folder.mkdir(parents=True,exist_ok=True)
    path=folder/'episode.json';path.write_text(json.dumps(config),encoding='utf-8')
    output=folder/(config['error_code']+'-bug-archive.mp4')
    try:
        with lock:jobs[job]={'status':'running','progress':'Archiving the episode…'}
        saved=archive(config)
        with lock:jobs[job]={'status':'running','progress':'Rendering 1080 × 1920 MP4…'}
        p=subprocess.Popen([sys.executable,str(ROOT/'render.py'),str(path),'--output',str(output)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log=[]
        for line in p.stdout:
            log.append(line)
            if line.startswith('frame '):
                with lock:jobs[job]['progress']=f'Rendering… {min(99,int(int(line.split()[1])/360*100))}%'
        if p.wait()!=0:raise RuntimeError(''.join(log)[-1600:])
        with lock:jobs[job]={'status':'done','video':'/'+output.relative_to(ROOT).as_posix(),'thumbnail':'/'+output.with_name(output.stem+'-locked.png').relative_to(ROOT).as_posix(),'archive':saved[0],'bug':saved[1]}
    except Exception as e:
        with lock:jobs[job]={'status':'failed','error':str(e)}
def render_batch(job,codes):
    """Render several episodes straight from episodes/, one after another.

    The single-episode job renders whatever is in the editor. A batch renders what is
    already saved, so picking thirty episodes does not mean loading each one first.
    One failure is recorded and the run carries on, matching the GitHub Action."""
    folder=ROOT/'output'/'jobs'/job;folder.mkdir(parents=True,exist_ok=True)
    done,failed=[],[]
    for i,code in enumerate(codes,1):
        with lock:jobs[job]={'status':'running','progress':f'Rendering {code}… ({i}/{len(codes)})','done':list(done),'failed':list(failed)}
        output=folder/f'ERROR.{code}.mp4'
        try:
            p=subprocess.run([sys.executable,str(ROOT/'render.py'),str(ROOT/'episodes'/f'{code}.json'),'--output',str(output)],
                             cwd=ROOT,capture_output=True,text=True)
            if p.returncode!=0:raise RuntimeError((p.stdout+p.stderr)[-600:])
            done.append({'code':code,
                         'video':'/'+output.relative_to(ROOT).as_posix(),
                         'thumbnail':'/'+output.with_name(output.stem+'-locked.png').relative_to(ROOT).as_posix()})
        except Exception as e:
            failed.append({'code':code,'error':str(e)})
    with lock:jobs[job]={'status':'done','batch':True,'done':done,'failed':failed}
INDEX=ROOT/'episodes'/'index.json'
MUSIC_DIR=ROOT/'music'
MUSIC_INDEX=MUSIC_DIR/'index.json'
MUSIC_TYPES={'.mp3':'audio/mpeg','.wav':'audio/wav','.ogg':'audio/ogg','.m4a':'audio/mp4','.opus':'audio/ogg','.flac':'audio/flac'}
def tracks():
    """Background music the renderer can use. Paths are relative to index.html, like the episode list."""
    out=[]
    for path in sorted(MUSIC_DIR.glob('*')):
        if path.suffix.lower() not in MUSIC_TYPES:continue
        out.append({'file':path.name,'path':'music/'+path.name,'size':path.stat().st_size})
    return out
def write_music_index():
    data={'tracks':tracks()}
    try:
        MUSIC_DIR.mkdir(exist_ok=True)
        MUSIC_INDEX.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except OSError:pass
    return data
def safe_track(name):
    name=Path(str(name)).name
    if not name or name.startswith('.') or Path(name).suffix.lower() not in MUSIC_TYPES:raise ValueError('Use an audio file such as .mp3 or .wav.')
    return MUSIC_DIR/name
CHECKLIST=ROOT/'cs-error-series-checklist.md'
def checklist_order():
    """Map CS code -> (number, tier) from the checklist so the load list matches the plan, not the filenames."""
    order={};tier=0
    try:text=CHECKLIST.read_text(encoding='utf-8')
    except OSError:return order
    for line in text.split('\n'):
        head=re.match(r'^##\s*(\d+)티어',line)
        if head:tier=int(head.group(1));continue
        item=re.match(r'^- \[[ x]\]\s*(\d+)\.\s*\*\*(CS\d+)\*\*',line)
        if item:order.setdefault(item.group(2),(int(item.group(1)),tier))
    return order
def episodes():
    """List episodes/*.json with the bug PNG each one points at, when that file is inside the studio.

    Paths are relative to index.html so the same payload works from the local server and from GitHub Pages."""
    out=[];order=checklist_order()
    for path in sorted((ROOT/'episodes').glob('*.json')):
        if path==INDEX:continue
        try:c=json.loads(path.read_text(encoding='utf-8'))
        except Exception:continue
        if not isinstance(c,dict):continue
        bug=c.get('bug') if isinstance(c.get('bug'),str) else None
        target=(path.parent/bug).resolve() if bug else None
        inside=bool(target) and target.is_file() and ROOT in target.parents
        out.append({'file':path.name,'path':'episodes/'+path.name,'error_code':str(c.get('error_code','')),
                    'message':str(c.get('message','')),'filename':str(c.get('filename','Player.cs')),
                    'lines':max(len(c.get('before') or []),len(c.get('after') or [])),
                    'bug':target.relative_to(ROOT).as_posix() if inside else None,
                    'missing':bug if bug and not inside else None})
        n,tier=order.get(str(c.get('error_code','')),(0,0))
        out[-1]['order']=n;out[-1]['tier']=tier
    out.sort(key=lambda e:(e['order'] or 10**6,e['file']))
    return out
def write_index():
    """Keep episodes/index.json in step with the folder. GitHub Pages has no API, so it reads this file."""
    write_music_index()
    data={'episodes':episodes()}
    try:INDEX.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except OSError:pass
    return data
def archive(config):
    """Store the rendered episode as episodes/<CODE>.json plus assets/<CODE>.png so it can be loaded again."""
    code=config['error_code'];png=ROOT/'assets'/f'{code}.png'
    png.write_bytes(base64.b64decode(config['bug_data_url'].split(',',1)[1],validate=True))
    kept={k:config[k] for k in ('error_code','message','filename','before','after') if k in config}
    if 'focus_line' in config:kept['focus_line']=config['focus_line']
    if config.get('music'):kept['music']=config['music']
    kept['bug']=f'../assets/{code}.png'
    (ROOT/'episodes'/f'{code}.json').write_text(json.dumps(kept,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_index()
    return f'episodes/{code}.json',f'assets/{code}.png'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
    def local(self):return self.headers.get('Host') in {f'127.0.0.1:{args.port}',f'localhost:{args.port}'}
    def send_json(self,data,status=200):
        b=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if not self.local():return self.send_json({'error':'Local access only.'},403)
        if self.path.startswith('/api/job/'):
            with lock:data=jobs.get(self.path.split('/')[-1])
            return self.send_json(data or {'error':'Unknown job.'},200 if data else 404)
        if self.path=='/api/health':return self.send_json({'ready':True})
        if self.path=='/api/episodes':return self.send_json(write_index())
        if self.path=='/api/music':return self.send_json(write_music_index())
        super().do_GET()
    def do_music(self):
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<40*1024*1024:raise ValueError('Use an audio file under 40 MB.')
            body=json.loads(self.rfile.read(length))
            path=safe_track(body.get('name'))
            if self.path.endswith('/delete'):
                path.unlink(missing_ok=True)
            else:
                data=str(body.get('data_url') or '')
                if ',' not in data or not data.startswith('data:'):raise ValueError('Send the file as a data URL.')
                MUSIC_DIR.mkdir(exist_ok=True)
                path.write_bytes(base64.b64decode(data.split(',',1)[1],validate=True))
            return self.send_json(write_music_index())
        except Exception as e:return self.send_json({'error':str(e)},400)
    def do_batch(self):
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<64*1024:raise ValueError('Selection is too large.')
            codes=json.loads(self.rfile.read(length)).get('codes')
            if not isinstance(codes,list) or not codes:raise ValueError('Pick at least one episode.')
            if len(codes)>600:raise ValueError('Pick 600 episodes or fewer.')
            wanted,seen=[],set()
            for code in codes:
                if not isinstance(code,str) or not re.fullmatch(r'CS\d{4}',code):raise ValueError(f'Invalid error code: {code!r}.')
                if not (ROOT/'episodes'/f'{code}.json').is_file():raise ValueError(f'{code} is not an episode in the episodes folder.')
                if code not in seen:seen.add(code);wanted.append(code)
            job=uuid.uuid4().hex
            with lock:jobs[job]={'status':'queued','progress':f'{len(wanted)} episodes queued…','done':[],'failed':[]}
            pool.submit(render_batch,job,wanted);self.send_json({'job':job,'count':len(wanted)},202)
        except Exception as e:self.send_json({'error':str(e)},400)
    def do_POST(self):
        origin=self.headers.get('Origin')
        if not self.local() or origin not in {None,f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}'}:return self.send_json({'error':'Local origin required.'},403)
        if self.path in {'/api/music','/api/music/delete'}:return self.do_music()
        if self.path=='/api/render/batch':return self.do_batch()
        if self.path!='/api/render':return self.send_json({'error':'Unknown action.'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<12*1024*1024:raise ValueError('Project is too large.')
            if 'application/json' not in self.headers.get('Content-Type',''):raise ValueError('JSON required.')
            c=json.loads(self.rfile.read(length))
            import re
            if not re.fullmatch(r'CS\d{4}',c.get('error_code','')):raise ValueError('Invalid error code.')
            if not isinstance(c.get('bug_data_url'),str) or not c['bug_data_url'].startswith('data:image/png;base64,'):raise ValueError('Save an embedded PNG first.')
            c={k:v for k,v in c.items() if k in {'error_code','filename','message','before','after','focus_line','bug_data_url','music'}}
            job=uuid.uuid4().hex
            with lock:jobs[job]={'status':'queued','progress':'Queued for rendering…'}
            pool.submit(render,job,c);self.send_json({'job':job},202)
        except Exception as e:self.send_json({'error':str(e)},400)
if args.index:
    print('episodes/index.json refreshed with %d episodes.'%len(write_index()['episodes']));sys.exit()
write_index()
url=f'http://127.0.0.1:{args.port}/index.html'
try:server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
except OSError:sys.exit('Port is already in use. Close the old studio or use --port 8766.')
print('Bug Archive Studio: '+url,flush=True)
if not args.no_browser:threading.Timer(.5,lambda:webbrowser.open(url)).start()
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close();pool.shutdown(wait=False)
