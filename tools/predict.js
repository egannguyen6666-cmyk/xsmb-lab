// Khóa danh sách cho kỳ quay kế tiếp (chỉ thêm, không sửa dòng cũ).
// Usage: node tools/predict.js            (chạy trong thư mục chứa xsmb.csv, xsmn.csv, predictions.json, predictions_mn.json)
const fs = require('fs'), path = require('path');
const coreP = [path.join(__dirname, '..', 'core.js'), path.join(__dirname, 'core.js'), path.join(process.cwd(), 'core.js')].find(f => fs.existsSync(f));
const { XS } = require(coreP);
const dir = process.cwd();
const made = new Date(Date.now() + 7 * 3600e3).toISOString().slice(0, 16).replace('T', ' ') + ' (giờ VN)';
function loadLog(f) {
  const p = path.join(dir, f);
  if (!fs.existsSync(p)) { if (f === 'predictions_mn.json' || f === 'predictions_mt.json') return []; console.error('STOP: thiếu ' + f + '; không tạo nhật ký mới rỗng.'); process.exit(1); }
  let j; try { j = JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { console.error('STOP: ' + f + ' không phải JSON hợp lệ.'); process.exit(1); }
  if (!Array.isArray(j)) { console.error('STOP: ' + f + ' không phải mảng.'); process.exit(1); }
  return j;
}
function save(f, log, before) {
  if (log.length < before) { console.error('STOP: nhật ký ' + f + ' bị ngắn đi'); process.exit(1); }
  fs.writeFileSync(path.join(dir, f), JSON.stringify(log).replace(/\},\{"target"/g, '},\n{"target"') + '\n');
}
// ---- XSMB ----
{
  const S = XS.makeSeries(XS.parseMB(fs.readFileSync(path.join(dir, 'xsmb.csv'), 'utf8')), XS.MB);
  const log = loadLog('predictions.json'), before = log.length;
  for (const e of log) if (!e.picks.top3) e.picks.top3 = XS.top3From(e.picks);
  const t = S.N - 1, last = S.dates[t], target = XS.nextDrawMB(last);
  if (log.some(e => e.target === target)) console.log('XSMB: đã có', target);
  else { const picks = XS.allPicks(S, t); log.push({ target, based_on: last, made_at: made, k: 10, picks }); console.log('XSMB: khóa', target, 'top3=' + picks.top3.join(',')); }
  log.sort((a, b) => a.target < b.target ? -1 : 1); save('predictions.json', log, before);
}
// ---- XSMN, XSMT (mỗi đài) ----
for (const [reg, csvF, logF, cfg] of [['XSMN', 'xsmn.csv', 'predictions_mn.json', XS.MN], ['XSMT', 'xsmt.csv', 'predictions_mt.json', XS.MT]]) {
  if (!fs.existsSync(path.join(dir, csvF))) continue;
  const by = XS.parseMN(fs.readFileSync(path.join(dir, csvF), 'utf8'));
  const { last, sch } = XS.mnSchedule(by);
  const log = loadLog(logF), before = log.length, added = [];
  const next = XS.addDays(last, 1), wd = XS.weekday(next);
  for (const s of Object.keys(by).sort()) {
    if (!sch[s].includes(wd)) continue;
    if (log.some(e => e.target === next && e.station === s)) continue;
    const S = XS.makeSeries(by[s], cfg), t = S.N - 1;
    if (S.N <= cfg.start) continue;
    log.push({ target: next, station: s, based_on: S.dates[t], made_at: made, k: 10, picks: XS.allPicks(S, t) }); added.push(s);
  }
  log.sort((a, b) => a.target < b.target ? -1 : a.target > b.target ? 1 : (a.station < b.station ? -1 : 1));
  save(logF, log, before);
  console.log(reg + ': kỳ', next, added.length ? 'khóa ' + added.join(', ') : 'đã có / không có đài');
}
