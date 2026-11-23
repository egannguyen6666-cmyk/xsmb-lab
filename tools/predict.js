// Usage: node predict.js xsmb.csv predictions.json
// Appends the frozen picks (top 10 of each indicator) for the draw after the last date in xsmb.csv.
// Same scoring and tie-break as index.html. Never overwrites an existing entry.
const fs = require('fs');
const [csvPath, logPath] = process.argv.slice(2);
const K = 10;
const IDS = ['combo','hot30','hot90','hot180','cold30','gan','roi','rand'];
const lines = fs.readFileSync(csvPath, 'utf8').trim().split('\n').slice(1);
const N = lines.length, dates = [], cnt = new Uint8Array(N*100), pref = new Int32Array((N+1)*100), ganA = new Uint16Array(N*100);
lines.forEach((ln,i)=>{const [d,s]=ln.split(',');dates.push(d);for(let j=0;j<54;j+=2)cnt[i*100+(+s.substr(j,2))]++;});
for(let i=0;i<N;i++)for(let k=0;k<100;k++){pref[(i+1)*100+k]=pref[i*100+k]+cnt[i*100+k];ganA[i*100+k]=cnt[i*100+k]?0:(i?ganA[(i-1)*100+k]:0)+1;}
function jit(t,k){let h=(t*2654435761 ^ (k+1)*40503)>>>0; h^=h>>>15; h=Math.imul(h,2246822507)>>>0; h^=h>>>13; return h/4294967296;}
function freq(t,w){const a=new Float64Array(100),lo=Math.max(0,t-w+1);for(let k=0;k<100;k++)a[k]=pref[(t+1)*100+k]-pref[lo*100+k];return a;}
function scores(id,t){
  if(id==='hot30')return freq(t,30); if(id==='hot90')return freq(t,90); if(id==='hot180')return freq(t,180);
  if(id==='cold30')return freq(t,30).map(x=>-x);
  if(id==='gan')return Float64Array.from(ganA.subarray(t*100,t*100+100));
  if(id==='roi')return Float64Array.from(cnt.subarray(t*100,t*100+100));
  if(id==='rand')return new Float64Array(100);
  const s=new Float64Array(100);
  for(const w of [30,90,180]){const f=freq(t,w),mu=27*w/100,sd=Math.sqrt(27*w*0.0099);for(let k=0;k<100;k++)s[k]+=(f[k]-mu)/sd/3;}
  return s;
}
function topK(s,t,K){const key=new Float64Array(100);for(let k=0;k<100;k++)key[k]=s[k]+jit(t,k)*1e-6;const idx=[...Array(100).keys()];idx.sort((a,b)=>key[b]-key[a]);return idx.slice(0,K);}
const TET={2026:'2026-02-17',2027:'2027-02-06',2028:'2028-01-26',2029:'2029-02-13',2030:'2030-02-03',2031:'2031-01-23',2032:'2032-02-11',2033:'2033-01-31',2034:'2034-02-19',2035:'2035-02-08',2036:'2036-01-28',2037:'2037-02-15',2038:'2038-02-04',2039:'2039-01-24',2040:'2040-02-12'};
// XSMB không quay từ 30 Tết (ngày trước mùng 1) đến hết mùng 3 — đúng với mọi năm 2010–2026 trong dữ liệu.
function tetBreak(iso){const y=+iso.slice(0,4);for(const yy of [y,y+1]){const t=TET[yy];if(!t)continue;const diff=Math.round((Date.parse(iso+'T00:00:00Z')-Date.parse(t+'T00:00:00Z'))/864e5);if(diff>=-1&&diff<=2)return t;}return null;}
function nextDraw(iso){const d=new Date(iso+'T00:00:00Z');do{d.setUTCDate(d.getUTCDate()+1);}while(tetBreak(d.toISOString().slice(0,10)));return d.toISOString().slice(0,10);}
const t = N-1, last = dates[t];
const target = nextDraw(last);
// Append-only log: refuse to run if the existing log cannot be read, so history is never replaced by an empty file.
if (!fs.existsSync(logPath)) { console.error('STOP: predictions.json not found. Copy it from the artifact first; never start a new empty log.'); process.exit(1); }
let log; try { log = JSON.parse(fs.readFileSync(logPath,'utf8')); } catch(e) { console.error('STOP: predictions.json is not valid JSON; not touching it.'); process.exit(1); }
if (!Array.isArray(log)) { console.error('STOP: predictions.json is not an array.'); process.exit(1); }
const before = log.length;
// Top 3 đề xuất: inside the "Tổng hợp nóng" top 10, rank by how many of the 5 frequency-based lists
// (combo, hot30, hot90, hot180, roi) contain the number; ties keep the combo order. Uses only the locked lists.
function top3(p){const L=['combo','hot30','hot90','hot180','roi'];return p.combo.map((k,i)=>[k,L.filter(id=>p[id].includes(k)).length,i]).sort((a,b)=>(b[1]-a[1])||(a[2]-b[2])).slice(0,3).map(x=>x[0]);}
for (const e of log) if (!e.picks.top3) e.picks.top3 = top3(e.picks);
const exists = log.some(e=>e.target===target);
const picks = {}; for (const id of IDS) picks[id] = topK(scores(id,t),t,K); picks.top3 = top3(picks);
const made = new Date(Date.now()+7*3600e3).toISOString().slice(0,16).replace('T',' ') + ' (giờ VN)';
if (!exists) log.push({target, based_on:last, made_at:made, k:K, picks});
if (log.length < before) { console.error('STOP: log would shrink'); process.exit(1); }
log.sort((a,b)=>a.target<b.target?-1:1);
fs.writeFileSync(logPath, JSON.stringify(log, null, 0).replace(/\},\{"target"/g,'},\n{"target"') + '\n');
console.log(exists ? 'exists '+target+' (kept unchanged)' : 'added '+target+' top3='+picks.top3.join(','), 'entries', log.length);
