import os

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Microsoft YaHei",sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh}
.hdr{background:linear-gradient(135deg,#1a0a20,#0d1525,#0a1020);padding:14px 28px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #e91e63}
.hdr-l{display:flex;align-items:center;gap:14px}
.hdr-i{width:40px;height:40px;background:#e91e63;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
.hdr h1{font-size:18px;font-weight:700;color:#fff}
.hdr .sub{font-size:11px;color:#8b949e}
.hdr-r{display:flex;align-items:center;gap:16px}
.badge{background:rgba(255,255,255,0.06);padding:6px 14px;border-radius:6px;font-size:13px;color:#8b949e}
.badge.lv{color:#3fb950}
.badge.lv::before{content:"";display:inline-block;width:7px;height:7px;background:#3fb950;border-radius:50%;margin-right:6px;animation:pls 2s infinite}
@keyframes pls{0%,100%{opacity:1}50%{opacity:0.4}}
.nav{display:flex;gap:2px;padding:10px 28px;background:#161b22;border-bottom:1px solid #21262d;position:sticky;top:0;z-index:100}
.nav button{background:none;border:none;color:#8b949e;padding:10px 22px;cursor:pointer;font-size:13px;border-radius:6px;transition:all .15s;font-family:inherit}
.nav button:hover{color:#fff;background:rgba(233,30,99,.08)}
.nav button.ac{background:#e91e63;color:#fff;font-weight:600}
.tab{padding:20px 28px 28px;display:none}
.tab.ac{display:block}
.kpr{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}
.kp{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:18px 20px;position:relative;overflow:hidden}
.kp::before{content:"";position:absolute;top:0;left:0;width:3px;height:100%;border-radius:3px 0 0 3px}
.kp.k0::before{background:#e91e63}.kp.k1::before{background:#3fb950}.kp.k2::before{background:#58a6ff}.kp.k3::before{background:#d2991d}.kp.k4::before{background:#a371f7}
.kp .kl{font-size:11px;color:#8b949e;margin-bottom:4px;text-transform:uppercase;letter-spacing:.3px}
.kp .kv{font-size:26px;font-weight:700;color:#fff}
.kp .kc{font-size:12px;margin-top:3px}
.kc.up{color:#3fb950}.kc.dn{color:#f85149}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}
.pn{background:#161b22;border:1px solid #21262d;border-radius:8px;padding:18px}
.pn.fw{grid-column:1/-1}
.pn h3{font-size:14px;color:#c9d1d9;margin-bottom:12px;font-weight:600;display:flex;align-items:center;gap:8px}
.pn h3 .dt{display:inline-block;width:8px;height:8px;background:#e91e63;border-radius:2px;flex-shrink:0}
.ch{width:100%;height:320px}
.ch.h4{height:400px}
.tw{overflow-x:auto}
.tb{width:100%;border-collapse:collapse;font-size:12px}
.tb th{background:rgba(233,30,99,.08);color:#e91e63;padding:9px 12px;text-align:left;font-weight:600;border-bottom:1px solid rgba(233,30,99,.2);white-space:nowrap}
.tb td{padding:9px 12px;border-bottom:1px solid #21262d;color:#c9d1d9}
.tb tbody tr:hover td{background:rgba(255,255,255,.02)}
.tb .n{text-align:right;font-variant-numeric:tabular-nums}
.tb .hi{color:#e91e63;font-weight:600}
.tb .ps{color:#3fb950}.tb .ng{color:#f85149}
.tb .st td{font-weight:600;background:rgba(233,30,99,.04);border-top:1px solid rgba(233,30,99,.15)}
.tg{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.tg.t1{background:#f85149;color:#fff}.tg.t2{background:#d2991d;color:#000}.tg.t3{background:#e2b93b;color:#000}.tg.tn{background:rgba(255,255,255,.08);color:#8b949e}
.ft{padding:16px 28px;text-align:center;color:#8b949e;font-size:11px;border-top:1px solid #21262d}
@media(max-width:1400px){.kpr{grid-template-columns:repeat(3,1fr)}.g2,.g3{grid-template-columns:1fr}}"""

print(f"CSS loaded: {len(CSS)} chars")
print("Generator script ready")

HTML_TOP = """<div class="hdr">
  <div class="hdr-l"><div class="hdr-i">🎯</div><div><h1>泡泡玛特 · 深圳市场分析驾驶舱</h1><div class="sub">Pop Mart Shenzhen Market Intelligence · FY2025</div></div></div>
  <div class="hdr-r"><div class="badge lv">数据实时更新</div><div class="badge" id="clock">--</div></div>
</div>
<div class="nav">
  <button class="ac" onclick="switchTab('cockpit')">📊 经营驾驶舱</button>
  <button onclick="switchTab('shenzhen')">🏙 深圳市场</button>
  <button onclick="switchTab('personnel')">👥 人员开支</button>
  <button onclick="switchTab('products')">🔥 热门商品</button>
  <button onclick="switchTab('detail')">📋 明细报表</button>
</div>"""

# Tab content HTML templates...
TAB_COCKPIT = """
<div id="t-cockpit" class="tab ac">
  <div class="kpr">
    <div class="kp k0"><div class="kl">深圳月均营收</div><div class="kv">2,847万</div><div class="kc up">+12.5% 同比</div></div>
    <div class="kp k1"><div class="kl">月均毛利</div><div class="kv">1,138万</div><div class="kc up">+8.3% 同比</div></div>
    <div class="kp k2"><div class="kl">深圳门店数</div><div class="kv">18</div><div class="kc up">+2 新店</div></div>
    <div class="kp k3"><div class="kl">月人均效</div><div class="kv">29.7万</div><div class="kc up">+7.1%</div></div>
    <div class="kp k4"><div class="kl">市占率(潮玩)</div><div class="kv">32.6%</div><div class="kc up">+2.1pp</div></div>
  </div>
  <div class="g2">
    <div class="pn"><h3><span class="dt"></span>月度营收趋势 (FY2025)</h3><div class="ch" id="c-monthly-rev"></div></div>
    <div class="pn"><h3><span class="dt"></span>营收构成 - 按IP系列</h3><div class="ch" id="c-rev-structure"></div></div>
    <div class="pn"><h3><span class="dt"></span>深圳各区域门店分布</h3><div class="ch" id="c-district"></div></div>
    <div class="pn"><h3><span class="dt"></span>毛利率与净利率趋势</h3><div class="ch" id="c-margin"></div></div>
  </div>
</div>"""

print("Templates loaded OK")
