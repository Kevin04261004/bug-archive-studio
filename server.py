"""Loopback-only desktop bridge for index.html and the Python MP4 renderer."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,uuid,threading,webbrowser,argparse
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8765);ap.add_argument('--no-browser',action='store_true');args=ap.parse_args()
jobs={};pool=ThreadPoolExecutor(max_workers=1);lock=threading.Lock()
def render(job,config):
    folder=ROOT/'output'/'jobs'/job;folder.mkdir(parents=True,exist_ok=True)
    path=folder/'episode.json';path.write_text(json.dumps(config),encoding='utf-8')
    output=folder/(config['error_code']+'-bug-archive.mp4')
    try:
        with lock:jobs[job]={'status':'running','progress':'Rendering 1080 × 1920 MP4…'}
        p=subprocess.Popen([sys.executable,str(ROOT/'render.py'),str(path),'--output',str(output)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log=[]
        for line in p.stdout:
            log.append(line)
            if line.startswith('frame '):
                with lock:jobs[job]['progress']=f'Rendering… {min(99,int(int(line.split()[1])/360*100))}%'
        if p.wait()!=0:raise RuntimeError(''.join(log)[-1600:])
        with lock:jobs[job]={'status':'done','video':'/'+output.relative_to(ROOT).as_posix(),'thumbnail':'/'+output.with_name(output.stem+'-locked.png').relative_to(ROOT).as_posix()}
    except Exception as e:
        with lock:jobs[job]={'status':'failed','error':str(e)}
def episodes():
    """List episodes/*.json with the bug PNG each one points at, when that file is inside the studio."""
    out=[]
    for path in sorted((ROOT/'episodes').glob('*.json')):
        try:c=json.loads(path.read_text(encoding='utf-8'))
        except Exception:continue
        if not isinstance(c,dict):continue
        bug=c.get('bug') if isinstance(c.get('bug'),str) else None
        target=(path.parent/bug).resolve() if bug else None
        inside=bool(target) and target.is_file() and ROOT in target.parents
        out.append({'file':path.name,'error_code':str(c.get('error_code','')),'message':str(c.get('message','')),
                    'filename':str(c.get('filename','Player.cs')),
                    'lines':max(len(c.get('before') or []),len(c.get('after') or [])),
                    'bug':'/'+target.relative_to(ROOT).as_posix() if inside else None,
                    'missing':bug if bug and not inside else None})
    return out
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
        if self.path=='/api/episodes':return self.send_json({'episodes':episodes()})
        super().do_GET()
    def do_POST(self):
        origin=self.headers.get('Origin')
        if not self.local() or origin not in {None,f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}'}:return self.send_json({'error':'Local origin required.'},403)
        if self.path!='/api/render':return self.send_json({'error':'Unknown action.'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<12*1024*1024:raise ValueError('Project is too large.')
            if 'application/json' not in self.headers.get('Content-Type',''):raise ValueError('JSON required.')
            c=json.loads(self.rfile.read(length))
            import re
            if not re.fullmatch(r'CS\d{4}',c.get('error_code','')):raise ValueError('Invalid error code.')
            if not isinstance(c.get('bug_data_url'),str) or not c['bug_data_url'].startswith('data:image/png;base64,'):raise ValueError('Save an embedded PNG first.')
            c={k:v for k,v in c.items() if k in {'error_code','filename','message','before','after','focus_line','bug_data_url'}}
            job=uuid.uuid4().hex
            with lock:jobs[job]={'status':'queued','progress':'Queued for rendering…'}
            pool.submit(render,job,c);self.send_json({'job':job},202)
        except Exception as e:self.send_json({'error':str(e)},400)
url=f'http://127.0.0.1:{args.port}/index.html'
try:server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
except OSError:sys.exit('Port is already in use. Close the old studio or use --port 8766.')
print('Bug Archive Studio: '+url,flush=True)
if not args.no_browser:threading.Timer(.5,lambda:webbrowser.open(url)).start()
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close();pool.shutdown(wait=False)
