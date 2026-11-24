/* XSMB Lab — bộ tính toán dùng chung cho trang web và script (Node).
   Một "chuỗi" (series) là dãy kỳ quay của một miền (XSMB) hoặc một đài (XSMN).
   Mọi chỉ báo của kỳ t chỉ dùng dữ liệu đến hết kỳ t. */
(function (root) {
  const TET = {2026:'2026-02-17',2027:'2027-02-06',2028:'2028-01-26',2029:'2029-02-13',2030:'2030-02-03',2031:'2031-01-23',2032:'2032-02-11',2033:'2033-01-31',2034:'2034-02-19',2035:'2035-02-08',2036:'2036-01-28',2037:'2037-02-15',2038:'2038-02-04',2039:'2039-01-24',2040:'2040-02-12'};
  // XSMB không quay từ ngày trước mùng 1 đến hết mùng 3 (đúng với mọi năm 2010–2026). XSMN không nghỉ Tết.
  function tetBreak(iso) {
    const y = +iso.slice(0, 4);
    for (const yy of [y, y + 1]) {
      const t = TET[yy]; if (!t) continue;
      const diff = Math.round((Date.parse(iso + 'T00:00:00Z') - Date.parse(t + 'T00:00:00Z')) / 864e5);
      if (diff >= -1 && diff <= 2) return t;
    }
    return null;
  }
  const addDays = (iso, n) => { const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  function nextDrawMB(iso) { let d = addDays(iso, 1); while (tetBreak(d)) d = addDays(d, 1); return d; }
  const weekday = iso => new Date(iso + 'T00:00:00Z').getUTCDay();

  const STATIONS = {'an-giang':'An Giang','bac-lieu':'Bạc Liêu','ben-tre':'Bến Tre','binh-duong':'Bình Dương','binh-phuoc':'Bình Phước','binh-thuan':'Bình Thuận','ca-mau':'Cà Mau','can-tho':'Cần Thơ','da-lat':'Đà Lạt','dong-nai':'Đồng Nai','dong-thap':'Đồng Tháp','hau-giang':'Hậu Giang','kien-giang':'Kiên Giang','long-an':'Long An','soc-trang':'Sóc Trăng','tay-ninh':'Tây Ninh','tien-giang':'Tiền Giang','tra-vinh':'Trà Vinh','vinh-long':'Vĩnh Long','vung-tau':'Vũng Tàu','tp-hcm':'TP.HCM','binh-dinh':'Bình Định','da-nang':'Đà Nẵng','dak-lak':'Đắk Lắk','dak-nong':'Đắk Nông','gia-lai':'Gia Lai','khanh-hoa':'Khánh Hòa','kon-tum':'Kon Tum','ninh-thuan':'Ninh Thuận','phu-yen':'Phú Yên','quang-binh':'Quảng Bình','quang-nam':'Quảng Nam','quang-ngai':'Quảng Ngãi','quang-tri':'Quảng Trị','thua-thien-hue':'Thừa Thiên Huế'};

  function jit(t, k) { let h = (t * 2654435761 ^ (k + 1) * 40503) >>> 0; h ^= h >>> 15; h = Math.imul(h, 2246822507) >>> 0; h ^= h >>> 13; return h / 4294967296; }

  /* rows: [{date, two: '0123...'}] — two = chuỗi 2 số cuối của m giải */
  function makeSeries(rows, opt) {
    const N = rows.length, m = opt.m, cnt = new Uint8Array(N * 100), pref = new Int32Array((N + 1) * 100), gan = new Uint16Array(N * 100), dates = [];
    rows.forEach((r, i) => { dates.push(r.date); for (let j = 0; j < 2 * m; j += 2) cnt[i * 100 + (+r.two.substr(j, 2))]++; });
    for (let i = 0; i < N; i++) for (let k = 0; k < 100; k++) { pref[(i + 1) * 100 + k] = pref[i * 100 + k] + cnt[i * 100 + k]; gan[i * 100 + k] = cnt[i * 100 + k] ? 0 : (i ? gan[(i - 1) * 100 + k] : 0) + 1; }
    return Object.assign({ N, m, cnt, pref, gan, dates, P: 1 - Math.pow(0.99, m), hitsBy: {} }, opt);
  }
  function freq(S, t, w) { const a = new Float64Array(100), lo = Math.max(0, t - w + 1); for (let k = 0; k < 100; k++) a[k] = S.pref[(t + 1) * 100 + k] - S.pref[lo * 100 + k]; return a; }
  function scores(S, id, t) {
    const W = S.W;
    if (id === 'hot30') return freq(S, t, W[0]); if (id === 'hot90') return freq(S, t, W[1]); if (id === 'hot180') return freq(S, t, W[2]);
    if (id === 'cold30') return freq(S, t, W[0]).map(x => -x);
    if (id === 'gan') return Float64Array.from(S.gan.subarray(t * 100, t * 100 + 100));
    if (id === 'roi') return Float64Array.from(S.cnt.subarray(t * 100, t * 100 + 100));
    if (id === 'rand') return new Float64Array(100);
    const s = new Float64Array(100);
    for (const w of W) { const f = freq(S, t, w), mu = S.m * w / 100, sd = Math.sqrt(S.m * w * 0.0099); for (let k = 0; k < 100; k++) s[k] += (f[k] - mu) / sd / 3; }
    return s;
  }
  function topK(s, t, K) { const key = new Float64Array(100); for (let k = 0; k < 100; k++) key[k] = s[k] + jit(t, k) * 1e-6; const idx = [...Array(100).keys()]; idx.sort((a, b) => key[b] - key[a]); return idx.slice(0, K); }
  const IDS = ['combo', 'hot30', 'hot90', 'hot180', 'cold30', 'gan', 'roi', 'rand'];
  function top3From(p) { const L = ['combo', 'hot30', 'hot90', 'hot180', 'roi']; return p.combo.map((k, i) => [k, L.filter(id => p[id].includes(k)).length, i]).sort((a, b) => (b[1] - a[1]) || (a[2] - b[2])).slice(0, 3).map(x => x[0]); }
  function allPicks(S, t) { const p = {}; for (const id of IDS) p[id] = topK(scores(S, id, t), t, 10); p.top3 = top3From(p); return p; }
  function picksFor(S, id, t) { if (id !== 'top3') return topK(scores(S, id, t), t, 10); const p = {}; for (const x of ['combo', 'hot30', 'hot90', 'hot180', 'roi']) p[x] = topK(scores(S, x, t), t, 10); return top3From(p); }

  const rev = k => (k % 10) * 10 + Math.floor(k / 10);
  function danPicks(S, method, size, t) {
    if (method === 'tan-suat') return topK(scores(S, 'combo', t), t, size);
    if (method === 'cau-chay') {
      const f1 = freq(S, t, S.WC[0]), f2 = freq(S, t, S.WC[1]), s = new Float64Array(100);
      for (let k = 0; k < 100; k++) { let d = 0; for (let i = t; i > t - 3 && i >= 0; i--) if (S.cnt[i * 100 + k]) d++; s[k] = d * 1000 + f1[k] * 20 + f2[k]; }
      return topK(s, t, size);
    }
    const order = topK(scores(S, 'combo', t), t, 100), out = [];
    for (const k of order) { if (out.length >= size) break; if (out.includes(k)) continue; out.push(k); const r = rev(k); if (r !== k && out.length < size && !out.includes(r)) out.push(r); }
    return out;
  }

  /* Cấu hình theo miền */
  const MB = { region: 'mb', m: 27, W: [30, 90, 180], WC: [7, 30], WL: ['30 ngày', '90 ngày', '180 ngày'], start: 180, unit: 'ngày' };
  const MN = { region: 'mn', m: 18, W: [10, 26, 52], WC: [3, 10], WL: ['10 kỳ', '26 kỳ', '52 kỳ'], start: 52, unit: 'kỳ' };
  const MT = Object.assign({}, MN, { region: 'mt' });
  function parseMB(text) { return text.trim().split(/\r?\n/).slice(1).map(l => { const [date, two] = l.split(','); return { date, two }; }); }
  function parseMN(text) { const by = {}; for (const l of text.trim().split(/\r?\n/).slice(1)) { const [date, st, two] = l.split(','); (by[st] = by[st] || []).push({ date, two }); } for (const s in by) by[s].sort((a, b) => a.date < b.date ? -1 : 1); return by; }
  /* Lịch quay XSMN: thứ trong tuần của mỗi đài, suy từ 10 tuần dữ liệu gần nhất */
  function mnSchedule(by) {
    let last = ''; for (const s in by) { const d = by[s][by[s].length - 1].date; if (d > last) last = d; }
    const from = addDays(last, -70), sch = {};
    for (const s in by) { const w = new Set(); for (const r of by[s]) if (r.date > from) w.add(weekday(r.date)); sch[s] = [...w]; }
    return { last, sch };
  }
  function nextDrawStation(sch, s, afterIso) { let d = addDays(afterIso, 1); for (let i = 0; i < 14; i++) { if (sch[s].includes(weekday(d))) return d; d = addDays(d, 1); } return null; }

  root.XS = { TET, tetBreak, addDays, nextDrawMB, weekday, STATIONS, jit, makeSeries, freq, scores, topK, IDS, top3From, allPicks, picksFor, rev, danPicks, MB, MN, MT, parseMB, parseMN, mnSchedule, nextDrawStation };
})(typeof module !== 'undefined' ? module.exports : window);
