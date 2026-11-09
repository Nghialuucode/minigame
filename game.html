<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#10131b;--ink:#e9edf5;--mute:#8b93a7;--acc:#2de2c0;--warn:#ff6b57;--glass:rgba(22,26,38,.66);--line:rgba(255,255,255,.1)}
*{box-sizing:border-box;margin:0}
html,body{height:100%;background:var(--bg);color:var(--ink);font-family:Sora,system-ui,sans-serif;overflow:hidden;user-select:none;-webkit-user-select:none}
#c{position:fixed;inset:0;width:100%;height:100%;display:block;touch-action:none;cursor:grab}
.glass{background:var(--glass);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid var(--line);border-radius:16px}
button{font:inherit;color:inherit;border:0;cursor:pointer;background:rgba(255,255,255,.08);border-radius:10px;padding:8px 12px;transition:transform .12s,background .15s}
button:hover{background:rgba(255,255,255,.16)}button:active{transform:scale(.95)}
button:focus-visible,input:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
#hud{position:fixed;left:14px;top:14px;padding:12px 14px;min-width:180px;font-size:13px}
#turn{font-size:15px;font-weight:600}#turn b{color:var(--acc)}
#score{margin-top:8px;display:grid;gap:4px;color:var(--mute)}
#score div{display:flex;justify-content:space-between;gap:16px}#score .on{color:var(--ink)}
#tools{position:fixed;right:14px;top:14px;display:flex;gap:6px;padding:6px}
#pad{position:fixed;right:14px;top:70px;padding:10px;display:grid;grid-template-columns:repeat(6,1fr);gap:5px;max-height:calc(100% - 170px);overflow:auto}
#pad.hide{display:none}
#pad button{width:38px;height:34px;padding:0;font-size:12px;font-weight:600;background:rgba(255,255,255,.07)}
#pad button.lock{opacity:.28}
#pad button.sel{background:var(--acc);color:#06201a}
#bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);display:flex;align-items:center;gap:10px;padding:10px 12px;max-width:calc(100% - 24px);flex-wrap:wrap;justify-content:center}
#bar input{width:78px;background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:10px;color:var(--ink);padding:8px 10px;font:inherit}
#pull{background:var(--acc);color:#06201a;font-weight:800;padding:10px 20px}
#pull:disabled{opacity:.35;cursor:not-allowed}
#msg{font-size:13px;color:var(--mute);min-width:150px;text-align:center}
#toast{position:fixed;left:50%;top:70px;transform:translate(-50%,-10px);padding:10px 16px;font-size:14px;opacity:0;pointer-events:none;transition:.25s}
#toast.show{opacity:1;transform:translate(-50%,0)}
#end{position:fixed;inset:0;display:none;place-items:center;background:rgba(8,10,16,.6);backdrop-filter:blur(4px)}
#end.show{display:grid}
#end .box{padding:28px 32px;text-align:center;max-width:340px}
#end h2{font-size:26px;font-weight:800;margin-bottom:6px;color:var(--warn)}
#end p{color:var(--mute);font-size:14px;line-height:1.5;margin-bottom:16px}
#end .rank{margin-bottom:18px;display:grid;gap:4px;font-size:14px}
@media(max-width:640px){#hud{min-width:0;padding:8px 10px}#score{display:none}#pad{top:64px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body>
<canvas id="c"></canvas>
<div id="hud" class="glass"><div id="turn"></div><div id="score"></div></div>
<div id="tools" class="glass">
  <button id="bSnd" title="Bật/tắt âm thanh"></button>
  <button id="bPad">Bảng số</button>
  <button id="bReset">Chơi lại</button>
</div>
<div id="pad" class="glass"></div>
<div id="toast" class="glass"></div>
<div id="bar" class="glass">
  <input id="num" type="number" min="1" placeholder="Nhập số" inputmode="numeric" aria-label="Nhập số khối gỗ">
  <div id="msg"></div>
  <button id="pull" disabled>Rút gỗ</button>
</div>
<div id="end"><div class="glass box"><h2 id="eT"></h2><p id="eP"></p><div class="rank" id="eR"></div><button id="again" style="background:var(--acc);color:#06201a;font-weight:800;padding:10px 22px">Chơi ván mới</button></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cannon.js/0.6.2/cannon.min.js"></script>
<script>
const CFG = __CONFIG__;
// ---- Vật lý & luật (đã nới ngưỡng sập để tháp bền hơn) ----
const PHYS = {FRICTION:.78, GRAVITY:-22, SPEED:2.2, PULL_DIST:3.5,
              TILT:.72, SAG:.5, DRIFT:2.4};
const L=3, H=.6, W=1, GAP=.02, STEP=H+GAP, OFF=W+GAP;
const $=s=>document.querySelector(s);

// ================= ÂM THANH =================
const Snd={ctx:null,on:CFG.sound,vol:CFG.volume,nb:null,
 init(){if(!this.on)return;if(!this.ctx){const A=window.AudioContext||window.webkitAudioContext;if(!A)return;this.ctx=new A();const n=this.ctx.sampleRate;this.nb=this.ctx.createBuffer(1,n,n);const d=this.nb.getChannelData(0);for(let i=0;i<n;i++)d[i]=Math.random()*2-1}
  if(this.ctx.state==='suspended')this.ctx.resume()},
 ready(){return this.on&&this.ctx&&this.ctx.state==='running'},
 G(g){return Math.max(.0002,g*this.vol)},
 tone(f0,f1,dur,type='sine',g=.2,delay=0){if(!this.ready())return;const c=this.ctx,t=c.currentTime+delay,o=c.createOscillator(),a=c.createGain();
  o.type=type;o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(Math.max(f1,20),t+dur);
  a.gain.setValueAtTime(this.G(g),t);a.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(a).connect(c.destination);o.start(t);o.stop(t+dur+.02)},
 noise(dur,type,f0,f1,g,delay=0,q=1){if(!this.ready())return;const c=this.ctx,t=c.currentTime+delay,s=c.createBufferSource(),f=c.createBiquadFilter(),a=c.createGain();
  s.buffer=this.nb;s.loop=true;f.type=type;f.Q.value=q;f.frequency.setValueAtTime(f0,t);f.frequency.exponentialRampToValueAtTime(Math.max(f1,20),t+dur);
  a.gain.setValueAtTime(.0001,t);a.gain.linearRampToValueAtTime(this.G(g),t+Math.min(.03,dur/4));a.gain.exponentialRampToValueAtTime(.0001,t+dur);
  s.connect(f).connect(a).connect(c.destination);s.start(t);s.stop(t+dur+.02)},
 click(){this.tone(880,1320,.06,'triangle',.12)},
 select(){this.tone(520,780,.1,'triangle',.15);this.tone(780,1040,.1,'sine',.08,.06)},
 warn(){this.tone(220,150,.22,'sawtooth',.1)},
 slide(d){this.noise(d,'bandpass',350,900,.22,0,2.5);this.noise(d,'lowpass',220,160,.16)},
 thud(v,delay=0){const g=Math.min(.55,.08*v);this.noise(.14,'lowpass',500,120,g,delay);this.tone(130,55,.16,'sine',g*.9,delay)},
 good(){[523,659,784].forEach((f,i)=>this.tone(f,f,.14,'triangle',.1,i*.07))},
 vanish(){this.tone(450,900,.15,'triangle',.1);this.tone(900,600,.14,'sine',.06,.08)},
 collapse(){for(let i=0;i<16;i++)this.thud(3+Math.random()*5,i*.09+Math.random()*.08);this.noise(1.8,'lowpass',700,60,.5);
  [392,330,262,196].forEach((f,i)=>this.tone(f,f*.98,.25,'sawtooth',.08,1.3+i*.18))}
};

// ---- Bridge từ Streamlit sidebar: điều khiển âm thanh LIVE ----
window.addEventListener('message', e=>{
  const d=e.data;
  if(!d||d.type!=='sound')return;
  Snd.on=!!d.on;
  Snd.vol=Math.max(0,Math.min(1,Number(d.volume)||0));
  if(Snd.on)Snd.init();
  ui();
});

// ================= 3D + VẬT LÝ =================
const cv=$('#c');
const ren=new THREE.WebGLRenderer({canvas:cv,antialias:true});
ren.setPixelRatio(Math.min(devicePixelRatio,2));ren.shadowMap.enabled=true;ren.shadowMap.type=THREE.PCFSoftShadowMap;
ren.outputEncoding=THREE.sRGBEncoding;ren.toneMapping=THREE.ACESFilmicToneMapping;
const scene=new THREE.Scene();scene.background=new THREE.Color(0x10131b);scene.fog=new THREE.Fog(0x10131b,26,60);
const cam=new THREE.PerspectiveCamera(45,1,.1,100);
scene.add(new THREE.HemisphereLight(0xbcd0ff,0x1a1208,.6));
const sun=new THREE.DirectionalLight(0xfff1d6,1.2);sun.position.set(7,15,6);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera,{left:-9,right:9,top:9,bottom:-9,near:1,far:40});sun.shadow.bias=-.0004;scene.add(sun);
const rim=new THREE.PointLight(0x2de2c0,.8,30);rim.position.set(-6,7,-6);scene.add(rim);
const floor=new THREE.Mesh(new THREE.CircleGeometry(60,64),new THREE.MeshStandardMaterial({color:0x1a1f2c,roughness:.85}));
floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;scene.add(floor);
const ring=new THREE.Mesh(new THREE.RingGeometry(2.7,2.76,64),new THREE.MeshBasicMaterial({color:0x2de2c0,transparent:true,opacity:.55}));
ring.rotation.x=-Math.PI/2;ring.position.y=.01;scene.add(ring);

const world=new CANNON.World();world.gravity.set(0,PHYS.GRAVITY,0);world.allowSleep=true;world.solver.iterations=22;
const wood=new CANNON.Material('wood');
world.addContactMaterial(new CANNON.ContactMaterial(wood,wood,{friction:PHYS.FRICTION,restitution:0,frictionEquationRelaxation:3}));
const gnd=new CANNON.Body({mass:0,material:wood});gnd.addShape(new CANNON.Plane());gnd.quaternion.setFromEuler(-Math.PI/2,0,0);world.addBody(gnd);

// ================= KHỐI GỖ =================
const boxGeo=new THREE.BoxGeometry(L,H,W);
function woodTex(w,h,hue,light,num,fs,pw){
  const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');
  x.fillStyle=`hsl(${hue},46%,${light}%)`;x.fillRect(0,0,w,h);
  for(let i=0;i<h/2;i++){x.strokeStyle=`rgba(60,32,10,${Math.random()*.10})`;x.lineWidth=1+Math.random()*1.5;x.beginPath();const y=Math.random()*h;x.moveTo(0,y);x.bezierCurveTo(w*.3,y+Math.random()*6-3,w*.7,y+Math.random()*6-3,w,y);x.stroke()}
  if(num!=null){
    x.fillStyle='rgba(16,19,27,.82)';const ph=h*.8,px=(w-pw)/2,py=(h-ph)/2,r=ph*.28;
    x.beginPath();x.moveTo(px+r,py);x.arcTo(px+pw,py,px+pw,py+ph,r);x.arcTo(px+pw,py+ph,px,py+ph,r);x.arcTo(px,py+ph,px,py,r);x.arcTo(px,py,px+pw,py,r);x.fill();
    x.fillStyle='#fff1d8';x.font=`800 ${fs}px Sora,system-ui,sans-serif`;x.textAlign='center';x.textBaseline='middle';x.fillText(num,w/2,h/2+fs*.04)}
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;t.anisotropy=4;return t}
function makeMats(id){
  const hue=26+Math.random()*8,li=52+Math.random()*10,mk=t=>new THREE.MeshStandardMaterial({map:t,roughness:.72,metalness:0});
  const end=mk(woodTex(192,115,hue,li,id,66,128)),top=mk(woodTex(256,96,hue,li-4,null)),lng=mk(woodTex(640,128,hue,li,id,88,190));
  return {list:[end,top,lng],arr:[end,end,top,top,lng,lng]}}

let blocks=[],hold=null,selected=null,hover=null,state='idle',turn=0,scores=[],time=0,shake=0,fx=[],lastHit=0,dir={x:1,z:0},pull={s:0,t:0,start:null,vy:null};
const N=CFG.players.length;

function pose(layer,slot){const y=H/2+layer*STEP,o=(slot-1)*OFF;return layer%2===0?{x:0,y,z:o,r:0}:{x:o,y,z:0,r:Math.PI/2}}
function addBody(b,p,drop=0){
  const body=new CANNON.Body({mass:1,material:wood});body.addShape(new CANNON.Box(new CANNON.Vec3(L/2,H/2,W/2)));
  body.position.set(p.x,p.y+drop,p.z);body.quaternion.setFromEuler(0,p.r,0);
  body.allowSleep=true;body.sleepSpeedLimit=.2;body.sleep
