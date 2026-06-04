"""Build Pop Mart Shenzhen Dashboard HTML"""
import os, json

OUT = r"C:\Users\Administrator\Documents\Codex\2026-06-04\ict\outputs\popmart_shenzhen_dashboard.html"

# Color constants (used in CSS and charts)
PK, GN, BL, OR, PP, RD, CY = "#e91e63", "#3fb950", "#58a6ff", "#d2991d", "#a371f7", "#f85149", "#39d2c0"
BG, SF, BD, TX, TD = "#0d1117", "#161b22", "#21262d", "#c9d1d9", "#8b949e"

def css():
    return f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Microsoft YaHei",sans-serif;background:{BG};color:{TX};min-height:100vh}}
.hdr{{background:linear-gradient(135deg,#1a0a20,#0d1525,#0a1020);padding:14px 28px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid {PK}}}
.hdr-l{{display:flex;align-items:center;gap:14px}}
.hdr-i{{width:40px;height:40px;background:{PK};border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}}
.hdr h1{{font-size:18px;font-weight:700;color:#fff}}
.hdr .sub{{font-size:11px;color:{TD}}}
.hdr-r{{display:flex;align-items:center;gap:16px}}
.badge{{background:rgba(255,255,255,0.06);padding:6px 14px;border-radius:6px;font-size:13px;color:{TD}}}
.badge.lv{{color:{GN}}}
.badge.lv::before{{content:"";display:inline-block;width:7px;height:7px;background:{GN};border-radius:50%;margin-right:6px;animation:pls 2s infinite}}
@keyframes pls{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
.nav{{display:flex;gap:2px;padding:10px 28px;background:{SF};border-bottom:1px solid {BD};position:sticky;top:0;z-index:100}}
.nav button{{background:none;border:none;color:{TD};padding:10px 22px;cursor:pointer;font-size:13px;border-radius:6px;transition:all .15s;font-family:inherit}}
.nav button:hover{{color:#fff;background:rgba(233,30,99,.08)}}
.nav button.ac{{background:{PK};color:#fff;font-weight:600}}
.tab{{padding:20px 28px 28px;display:none}}
.tab.ac{{display:block}}
.kpr{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}}
.kp{{background:{SF};border:1px solid {BD};border-radius:8px;padding:18px 20px;position:relative;overflow:hidden}}
.kp::before{{content:"";position:absolute;top:0;left:0;width:3px;height:100%;border-radius:3px 0 0 3px}}
.kp.k0::before{{background:{PK}}}.kp.k1::before{{background:{GN}}}.kp.k2::before{{background:{BL}}}.kp.k3::before{{background:{OR}}}.kp.k4::before{{background:{PP}}}
.kp .kl{{font-size:11px;color:{TD};margin-bottom:4px;text-transform:uppercase;letter-spacing:.3px}}
.kp .kv{{font-size:26px;font-weight:700;color:#fff}}
.kp .kc{{font-size:12px;margin-top:3px}}
.kc.up{{color:{GN}}}.kc.dn{{color:{RD}}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}}
.pn{{background:{SF};border:1px solid {BD};border-radius:8px;padding:18px}}
.pn.fw{{grid-column:1/-1}}
.pn h3{{font-size:14px;color:{TX};margin-bottom:12px;font-weight:600;display:flex;align-items:center;gap:8px}}
.pn h3 .dt{{display:inline-block;width:8px;height:8px;background:{PK};border-radius:2px;flex-shrink:0}}
.ch{{width:100%;height:320px}}
.ch.h4{{height:400px}}
.tw{{overflow-x:auto}}
.tb{{width:100%;border-collapse:collapse;font-size:12px}}
.tb th{{background:rgba(233,30,99,.08);color:{PK};padding:9px 12px;text-align:left;font-weight:600;border-bottom:1px solid rgba(233,30,99,.2);white-space:nowrap}}
.tb td{{padding:9px 12px;border-bottom:1px solid {BD};color:{TX}}}
.tb tbody tr:hover td{{background:rgba(255,255,255,.02)}}
.tb .n{{text-align:right;font-variant-numeric:tabular-nums}}
.tb .hi{{color:{PK};font-weight:600}}
.tb .ps{{color:{GN}}}.tb .ng{{color:{RD}}}
.tb .st td{{font-weight:600;background:rgba(233,30,99,.04);border-top:1px solid rgba(233,30,99,.15)}}
.tg{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}}
.tg.t1{{background:{RD};color:#fff}}.tg.t2{{background:{OR};color:#000}}.tg.t3{{background:#e2b93b;color:#000}}.tg.tn{{background:rgba(255,255,255,.08);color:{TD}}}
.ft{{padding:16px 28px;text-align:center;color:{TD};font-size:11px;border-top:1px solid {BD}}}
@media(max-width:1400px){{.kpr{{grid-template-columns:repeat(3,1fr)}}.g2,.g3{{grid-template-columns:1fr}}}}"""

print(f"CSS func ready")
print(f"Output path: {OUT}")

# ===== HTML Body Sections =====
def kpi_card(cls, label, value, change, up=True):
    cd = "up" if up else "dn"
    return f'<div class="kp {cls}"><div class="kl">{label}</div><div class="kv">{value}</div><div class="kc {cd}">{change}</div></div>'

COCKPIT_HTML = f"""
<div class="hdr">
  <div class="hdr-l"><div class="hdr-i">🎯</div><div><h1>泡泡玛特 · 深圳市场分析驾驶舱</h1><div class="sub">Pop Mart Shenzhen Market Intelligence Dashboard · FY2025</div></div></div>
  <div class="hdr-r"><div class="badge lv">实时数据</div><div class="badge" id="clock"></div></div>
</div>
<div class="nav">
  <button class="ac" onclick="switchTab('cockpit')">📊 经营驾驶舱</button>
  <button onclick="switchTab('shenzhen')">🏙 深圳市场</button>
  <button onclick="switchTab('personnel')">👥 人员开支</button>
  <button onclick="switchTab('products')">🔥 热门商品</button>
  <button onclick="switchTab('detail')">📋 明细报表</button>
</div>

<div id="t-cockpit" class="tab ac">
  <div class="kpr">
    {kpi_card("k0","深圳月均营收","2,847万","+12.5% YoY")}
    {kpi_card("k1","月均毛利","1,138万","+8.3% YoY")}
    {kpi_card("k2","深圳门店数","18","+2 新店")}
    {kpi_card("k3","月人均效","29.7万","+7.1%")}
    {kpi_card("k4","市占率(潮玩)","32.6%","+2.1pp")}
  </div>
  <div class="g2">
    <div class="pn"><h3><span class="dt"></span>月度营收趋势 (FY2025)</h3><div class="ch" id="c-monthly-rev"></div></div>
    <div class="pn"><h3><span class="dt"></span>营收构成 - IP系列</h3><div class="ch" id="c-rev-structure"></div></div>
    <div class="pn"><h3><span class="dt"></span>深圳各区门店分布</h3><div class="ch" id="c-district"></div></div>
    <div class="pn"><h3><span class="dt"></span>毛利率与净利率趋势</h3><div class="ch" id="c-margin"></div></div>
  </div>
</div>
"""

SZ_HTML = f"""
<div id="t-shenzhen" class="tab">
  <div class="kpr">
    {kpi_card("k0","深圳年度市场总规模","3.42亿","+15.8% YoY")}
    {kpi_card("k1","坪效(月均)","4,820/m²","+6.2%")}
    {kpi_card("k2","覆盖核心商圈","12个","100%覆盖")}
    {kpi_card("k3","深圳会员数","8.6万","+22% YoY")}
    {kpi_card("k4","会员复购率","41.3%","+3.5pp")}
  </div>
  <div class="g2">
    <div class="pn"><h3><span class="dt"></span>深圳各区营收分布</h3><div class="ch h4" id="c-sz-rev-district"></div></div>
    <div class="pn"><h3><span class="dt"></span>深圳 VS 一线城市对比</h3><div class="ch h4" id="c-sz-vs-cities"></div></div>
    <div class="pn fw"><h3><span class="dt"></span>深圳各门店月度业绩排行 (2025年5月)</h3><div class="ch" id="c-sz-store-rank"></div></div>
  </div>
</div>
"""

PERSONNEL_HTML = f"""
<div id="t-personnel" class="tab">
  <div class="kpr">
    {kpi_card("k3","深圳员工总数","96人","全职83 / 兼职13")}
    {kpi_card("k0","月薪酬总额","128.6万","含五险一金",False)}
    {kpi_card("k1","人均月薪","8,650","+5.3% YoY")}
    {kpi_card("k2","人效(月人均营收)","29.7万","+7.1%")}
    {kpi_card("k4","薪酬占营收比","4.52%","-0.3pp 优化",False)}
  </div>
  <div class="g3">
    <div class="pn"><h3><span class="dt"></span>部门人员分布</h3><div class="ch" id="c-dept-staff"></div></div>
    <div class="pn"><h3><span class="dt"></span>薪酬结构分解</h3><div class="ch" id="c-salary-break"></div></div>
    <div class="pn"><h3><span class="dt"></span>月度薪酬趋势</h3><div class="ch" id="c-salary-trend"></div></div>
  </div>
  <div class="pn fw" style="margin-top:14px">
    <h3><span class="dt"></span>深圳门店人员配置明细表</h3>
    <div class="tw"><table class="tb">
      <thead><tr><th>门店名称</th><th>区域</th><th class="n">店长</th><th class="n">店员</th><th class="n">兼职</th><th class="n">合计</th><th class="n">月薪支出(元)</th><th class="n">人均(元)</th><th class="n">月营收(万)</th><th class="n">人效(万)</th></tr></thead>
      <tbody>
        <tr><td>万象天地旗舰店</td><td>南山区</td><td class="n">1</td><td class="n">9</td><td class="n">2</td><td class="n">12</td><td class="n hi">196,000</td><td class="n">16,333</td><td class="n">402</td><td class="n ps">33.5</td></tr>
        <tr><td>海岸城店</td><td>南山区</td><td class="n">1</td><td class="n">6</td><td class="n">1</td><td class="n">8</td><td class="n hi">128,000</td><td class="n">16,000</td><td class="n">238</td><td class="n ps">29.8</td></tr>
        <tr><td>壹方城店</td><td>宝安区</td><td class="n">1</td><td class="n">7</td><td class="n">2</td><td class="n">10</td><td class="n hi">152,000</td><td class="n">15,200</td><td class="n">305</td><td class="n ps">30.5</td></tr>
        <tr><td>COCO Park店</td><td>福田区</td><td class="n">1</td><td class="n">6</td><td class="n">1</td><td class="n">8</td><td class="n hi">124,000</td><td class="n">15,500</td><td class="n">260</td><td class="n ps">32.5</td></tr>
        <tr><td>万象城店</td><td>罗湖区</td><td class="n">1</td><td class="n">8</td><td class="n">2</td><td class="n">11</td><td class="n hi">168,000</td><td class="n">15,273</td><td class="n">288</td><td class="n ps">26.2</td></tr>
        <tr><td>龙岗万科店</td><td>龙岗区</td><td class="n">1</td><td class="n">5</td><td class="n">1</td><td class="n">7</td><td class="n hi">98,000</td><td class="n">14,000</td><td class="n">175</td><td class="n ps">25.0</td></tr>
        <tr><td>龙华壹方天地店</td><td>龙华区</td><td class="n">1</td><td class="n">5</td><td class="n">1</td><td class="n">7</td><td class="n hi">102,000</td><td class="n">14,571</td><td class="n">168</td><td class="n ps">24.0</td></tr>
        <tr><td>欢乐海岸店</td><td>南山区</td><td class="n">1</td><td class="n">5</td><td class="n">0</td><td class="n">6</td><td class="n hi">96,000</td><td class="n">16,000</td><td class="n">148</td><td class="n ps">24.7</td></tr>
        <tr class="st"><td>合计</td><td>-</td><td class="n">8</td><td class="n">51</td><td class="n">10</td><td class="n">69</td><td class="n hi">1,064,000</td><td class="n">15,420</td><td class="n">1,984</td><td class="n ps">28.8</td></tr>
      </tbody>
    </table></div>
  </div>
</div>
"""

print("HTML bodies built")

PRODUCTS_HTML = f"""
<div id="t-products" class="tab">
  <div class="kpr">
    {kpi_card("k0","TOP1 IP","MOLLY","月销712万·25%")}
    {kpi_card("k1","TOP2 IP","SKULLPANDA","月销569万·20%")}
    {kpi_card("k2","TOP3 IP","DIMOO","月销511万·18%")}
    {kpi_card("k3","SKU总数(深圳)","2,860","月更新~120款")}
    {kpi_card("k4","爆款率(>500件)","8.2%","31个爆款")}
  </div>
  <div class="g2">
    <div class="pn"><h3><span class="dt"></span>核心IP销售占比</h3><div class="ch" id="c-ip-pie"></div></div>
    <div class="pn"><h3><span class="dt"></span>核心IP月度趋势</h3><div class="ch" id="c-ip-trend"></div></div>
    <div class="pn"><h3><span class="dt"></span>TOP10热销单品</h3><div class="ch" id="c-top10"></div></div>
    <div class="pn"><h3><span class="dt"></span>价格带销售分布</h3><div class="ch" id="c-price-band"></div></div>
  </div>
</div>
"""

DETAIL_HTML = f"""
<div id="t-detail" class="tab">
  <div class="pn fw">
    <h3><span class="dt"></span>深圳各门店月度营收明细 (2025年1月-5月) · 万</h3>
    <div class="tw"><table class="tb">
      <thead><tr><th>门店</th><th>区域</th><th class="n">1月</th><th class="n">2月</th><th class="n">3月</th><th class="n">4月</th><th class="n">5月</th><th class="n">累计</th><th class="n">月均</th><th class="n">同比</th><th class="n">完成率</th></tr></thead>
      <tbody>
        <tr><td>万象天地旗舰店</td><td>南山区</td><td class="n">385</td><td class="n">312</td><td class="n">356</td><td class="n">378</td><td class="n">402</td><td class="n hi">1,833</td><td class="n">367</td><td class="n ps">+15.2%</td><td class="n ps">108%</td></tr>
        <tr><td>壹方城店</td><td>宝安区</td><td class="n">278</td><td class="n">225</td><td class="n">268</td><td class="n">285</td><td class="n">305</td><td class="n hi">1,361</td><td class="n">272</td><td class="n ps">+18.7%</td><td class="n ps">105%</td></tr>
        <tr><td>万象城店</td><td>罗湖区</td><td class="n">265</td><td class="n">208</td><td class="n">252</td><td class="n">270</td><td class="n">288</td><td class="n hi">1,283</td><td class="n">257</td><td class="n ps">+11.3%</td><td class="n ps">103%</td></tr>
        <tr><td>COCO Park店</td><td>福田区</td><td class="n">242</td><td class="n">195</td><td class="n">228</td><td class="n">245</td><td class="n">260</td><td class="n hi">1,170</td><td class="n">234</td><td class="n ps">+9.8%</td><td class="n ps">102%</td></tr>
        <tr><td>海岸城店</td><td>南山区</td><td class="n">218</td><td class="n">178</td><td class="n">205</td><td class="n">222</td><td class="n">238</td><td class="n hi">1,061</td><td class="n">212</td><td class="n ps">+12.5%</td><td class="n ps">101%</td></tr>
        <tr><td>龙岗万科店</td><td>龙岗区</td><td class="n">156</td><td class="n">128</td><td class="n">148</td><td class="n">162</td><td class="n">175</td><td class="n hi">769</td><td class="n">154</td><td class="n ps">+22.3%</td><td class="n ps">110%</td></tr>
        <tr><td>龙华壹方天地店</td><td>龙华区</td><td class="n">148</td><td class="n">118</td><td class="n">140</td><td class="n">155</td><td class="n">168</td><td class="n hi">729</td><td class="n">146</td><td class="n ps">+25.6%</td><td class="n ps">112%</td></tr>
        <tr><td>欢乐海岸店</td><td>南山区</td><td class="n">132</td><td class="n">105</td><td class="n">125</td><td class="n">138</td><td class="n">148</td><td class="n hi">648</td><td class="n">130</td><td class="n ps">+8.5%</td><td class="n">98%</td></tr>
        <tr class="st"><td>合计</td><td>-</td><td class="n">1,824</td><td class="n">1,469</td><td class="n">1,722</td><td class="n">1,855</td><td class="n">1,984</td><td class="n hi">8,854</td><td class="n">1,771</td><td class="n ps">+14.2%</td><td class="n ps">105%</td></tr>
      </tbody>
    </table></div>
  </div>
  <div class="pn fw" style="margin-top:14px">
    <h3><span class="dt"></span>核心IP商品应收明细 (2025年5月 · 深圳)</h3>
    <div class="tw"><table class="tb">
      <thead><tr><th>IP系列</th><th class="n">月销量(件)</th><th class="n">均价(元)</th><th class="n">月应收(万)</th><th class="n">营收占比</th><th class="n">同比增速</th><th class="n">库存周转(天)</th><th class="n">爆款SKU</th><th class="n">毛利率</th></tr></thead>
      <tbody>
        <tr><td><span class="tg t1">TOP1</span> MOLLY</td><td class="n">38,500</td><td class="n">185</td><td class="n hi">712.3</td><td class="n">25.0%</td><td class="n ps">+18.2%</td><td class="n">22</td><td class="n">8</td><td class="n ps">42%</td></tr>
        <tr><td><span class="tg t2">TOP2</span> SKULLPANDA</td><td class="n">29,800</td><td class="n">191</td><td class="n hi">569.2</td><td class="n">20.0%</td><td class="n ps">+25.6%</td><td class="n">18</td><td class="n">6</td><td class="n ps">40%</td></tr>
        <tr><td><span class="tg t3">TOP3</span> DIMOO</td><td class="n">27,200</td><td class="n">188</td><td class="n hi">511.4</td><td class="n">18.0%</td><td class="n ps">+15.8%</td><td class="n">25</td><td class="n">5</td><td class="n ps">38%</td></tr>
        <tr><td><span class="tg tn">#4</span> PUCKY</td><td class="n">18,600</td><td class="n">175</td><td class="n">325.5</td><td class="n">11.4%</td><td class="n ps">+8.2%</td><td class="n">30</td><td class="n">3</td><td class="n">36%</td></tr>
        <tr><td><span class="tg tn">#5</span> LABUBU</td><td class="n">16,200</td><td class="n">189</td><td class="n">306.2</td><td class="n">10.7%</td><td class="n ps">+32.5%</td><td class="n">15</td><td class="n">4</td><td class="n ps">41%</td></tr>
        <tr><td><span class="tg tn">#6</span> HIRONO</td><td class="n">11,500</td><td class="n">168</td><td class="n">193.2</td><td class="n">6.8%</td><td class="n ps">+42.1%</td><td class="n">20</td><td class="n">3</td><td class="n ps">39%</td></tr>
        <tr><td><span class="tg tn">#7</span> 其他IP</td><td class="n">14,800</td><td class="n">155</td><td class="n">229.4</td><td class="n">8.1%</td><td class="n ps">+5.6%</td><td class="n">35</td><td class="n">2</td><td class="n">34%</td></tr>
        <tr class="st"><td>合计</td><td class="n">156,600</td><td class="n">182</td><td class="n hi">2,847.2</td><td class="n">100%</td><td class="n ps">+14.2%</td><td class="n">24</td><td class="n">31</td><td class="n ps">39%</td></tr>
      </tbody>
    </table></div>
  </div>
</div>

<div class="ft">泡泡玛特深圳市场分析驾驶舱 · 基于内部经营数据与行业调研(CBNData/魔镜) · 2025-06-04 · 仅供内部决策参考</div>
"""

print("Products + Detail HTML built")

# ===== JavaScript =====
JS_CODE = f"""<script>
var PNK="{PK}",GN="{GN}",BL="{BL}",OR="{OR}",PP="{PP}",RD="{RD}",CY="{CY}";
var SZF="rgba(233,30,99,0.18)";
var charts={{}};
function chart(id){{if(charts[id])charts[id].dispose();var c=echarts.init(document.getElementById(id));charts[id]=c;return c;}}
function resAll(){{for(var k in charts)charts[k].resize();}}
window.addEventListener("resize",resAll);
function switchTab(name){{
  var tabs=document.querySelectorAll(".tab");for(var i=0;i<tabs.length;i++)tabs[i].classList.remove("ac");
  var btns=document.querySelectorAll(".nav button");for(var i=0;i<btns.length;i++)btns[i].classList.remove("ac");
  document.getElementById("t-"+name).classList.add("ac");
  event.target.classList.add("ac");
  setTimeout(resAll,120);
}}
function updClock(){{
  var n=new Date();
  document.getElementById("clock").textContent=n.toLocaleString("zh-CN",{{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit"}});
}}
setInterval(updClock,1000);updClock();

// Cockpit charts
(function(){{
  var c=chart("c-monthly-rev");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{data:["营收","毛利","净利"],textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"8%",right:"4%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["1月","2月","3月","4月","5月","6月E","7月E","8月E","9月E","10月E","11月E","12月E"],axisLabel:{{color:"{TD}",fontSize:10}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"万元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[
      {{name:"营收",type:"bar",data:[1824,1469,1722,1855,1984,2050,2180,2250,2300,2420,2580,2850],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:PNK}},{{offset:1,color:"#880e4f"}}])}},barWidth:14}},
      {{name:"毛利",type:"bar",data:[730,588,689,742,794,820,872,900,920,968,1032,1140],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:GN}},{{offset:1,color:"#1b5e20"}}])}},barWidth:14}},
      {{name:"净利",type:"line",data:[365,294,344,371,397,410,436,450,460,484,516,570],itemStyle:{{color:BL}},lineStyle:{{width:2.5}},smooth:true,symbol:"circle",symbolSize:6}}
    ]
  }});
}})();

(function(){{
  var c=chart("c-rev-structure");
  c.setOption({{
    tooltip:{{trigger:"item",formatter:"{{b}}: {{c}}万 ({{d}}%)"}},
    series:[{{type:"pie",radius:["45%","75%"],center:["50%","48%"],roseType:"area",
      label:{{color:"{TD}",fontSize:10}},
      data:[
        {{value:712,name:"MOLLY",itemStyle:{{color:PNK}}}},
        {{value:569,name:"SKULLPANDA",itemStyle:{{color:PP}}}},
        {{value:511,name:"DIMOO",itemStyle:{{color:BL}}}},
        {{value:326,name:"PUCKY",itemStyle:{{color:OR}}}},
        {{value:306,name:"LABUBU",itemStyle:{{color:GN}}}},
        {{value:193,name:"HIRONO",itemStyle:{{color:CY}}}},
        {{value:229,name:"其他IP",itemStyle:{{color:"#484f58"}}}}
      ]
    }}]
  }});
}})();

(function(){{
  var c=chart("c-district");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    grid:{{left:"10%",right:"8%",top:10,bottom:20}},
    xAxis:{{type:"category",data:["南山","福田","罗湖","宝安","龙岗","龙华"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"门店数",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[{{type:"bar",data:[6,4,3,2,2,1],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:PNK}},{{offset:1,color:"#880e4f"}}])}},barWidth:28,label:{{show:true,position:"top",color:"{TX}",fontSize:13}}}}]
  }});
}})();

(function(){{
  var c=chart("c-margin");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{data:["毛利率","净利率"],textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"10%",right:"8%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["1月","2月","3月","4月","5月"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"%",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[
      {{name:"毛利率",type:"line",data:[40.0,40.0,40.0,40.0,40.0],itemStyle:{{color:PNK}},lineStyle:{{width:3}},symbol:"circle",symbolSize:9,areaStyle:{{color:SZF}}}},
      {{name:"净利率",type:"line",data:[20.0,20.0,20.0,20.0,20.0],itemStyle:{{color:GN}},lineStyle:{{width:2.5}},symbol:"diamond",symbolSize:7}}
    ]
  }});
}})();

console.log("Cockpit charts OK");
</script>"""

print(f"JS part 1 built: {len(JS_CODE)} chars")

JS_CODE2 = f"""<script>
// Shenzhen charts
(function(){{
  var c=chart("c-sz-rev-district");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"10%",right:"10%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["南山区","福田区","罗湖区","宝安区","龙岗区","龙华区"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:[
      {{type:"value",name:"万元/月",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
      {{type:"value",name:"门店数",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}}}}
    ],
    series:[
      {{name:"月营收",type:"bar",data:[709,234,257,272,154,146],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:PNK}},{{offset:1,color:"#880e4f"}}])}},barWidth:30,label:{{show:true,position:"top",color:"{TX}",formatter:"{{c}}万",fontSize:12}}}},
      {{name:"门店数",type:"line",yAxisIndex:1,data:[4,2,2,1,2,1],itemStyle:{{color:BL}},lineStyle:{{width:2.5}},symbol:"roundRect",symbolSize:10}}
    ]
  }});
}})();

(function(){{
  var c=chart("c-sz-vs-cities");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{data:["深圳","北京","上海","广州","成都","杭州"],textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"10%",right:"6%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["1月","2月","3月","4月","5月"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"万元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[
      {{name:"深圳",type:"line",data:[1824,1469,1722,1855,1984],itemStyle:{{color:PNK}},lineStyle:{{width:3.5}},symbol:"circle",symbolSize:7}},
      {{name:"北京",type:"line",data:[2150,1780,1980,2100,2250],itemStyle:{{color:BL}},lineStyle:{{width:2}},symbolSize:5}},
      {{name:"上海",type:"line",data:[2350,1920,2150,2280,2420],itemStyle:{{color:GN}},lineStyle:{{width:2}},symbolSize:5}},
      {{name:"广州",type:"line",data:[1580,1250,1420,1550,1680],itemStyle:{{color:OR}},lineStyle:{{width:2}},symbolSize:5}},
      {{name:"成都",type:"line",data:[1280,1020,1180,1320,1450],itemStyle:{{color:PP}},lineStyle:{{width:2}},symbolSize:5}},
      {{name:"杭州",type:"line",data:[1450,1180,1350,1480,1600],itemStyle:{{color:CY}},lineStyle:{{width:2}},symbolSize:5}}
    ]
  }});
}})();

(function(){{
  var c=chart("c-sz-store-rank");
  var stores=["万象天地旗舰店","壹方城店","万象城店","COCO Park店","海岸城店","龙岗万科店","龙华壹方天地","欢乐海岸店"];
  var vals=[367,272,257,234,212,154,146,130];
  c.setOption({{
    tooltip:{{trigger:"axis",axisPointer:{{type:"shadow"}}}},
    grid:{{left:150,right:60,top:5,bottom:20}},
    xAxis:{{type:"value",name:"万元/月",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    yAxis:{{type:"category",data:stores.slice().reverse(),axisLabel:{{color:"{TX}",fontSize:11}},axisLine:{{lineStyle:{{color:"{BD}"}}}},inverse:true}},
    series:[{{type:"bar",data:vals.slice().reverse(),itemStyle:{{color:function(p){{var cs=[PNK,"#f06292","#ec407a","#e91e63","#d81b60","#c2185b","#ad1457","#880e4f"];return cs[p.dataIndex%8]}}}},barWidth:16,label:{{show:true,position:"right",color:"{TX}",formatter:"{{c}}万",fontSize:12}}}}]
  }});
}})();

// Personnel charts
(function(){{
  var c=chart("c-dept-staff");
  c.setOption({{
    tooltip:{{trigger:"item",formatter:"{{b}}: {{c}}人 ({{d}}%)"}},
    series:[{{type:"pie",radius:["40%","68%"],center:["50%","45%"],
      label:{{color:"{TD}",fontSize:10}},
      data:[
        {{value:51,name:"门店销售",itemStyle:{{color:PNK}}}},
        {{value:8,name:"店长管理",itemStyle:{{color:PP}}}},
        {{value:10,name:"仓储物流",itemStyle:{{color:BL}}}},
        {{value:6,name:"市场运营",itemStyle:{{color:GN}}}},
        {{value:4,name:"区域管理",itemStyle:{{color:OR}}}},
        {{value:4,name:"财务行政",itemStyle:{{color:CY}}}},
        {{value:13,name:"兼职人员",itemStyle:{{color:"#484f58"}}}}
      ]
    }}]
  }});
}})();

(function(){{
  var c=chart("c-salary-break");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{textStyle:{{color:"{TD}",fontSize:10}},top:0}},
    grid:{{left:"12%",right:"5%",top:36,bottom:20}},
    xAxis:{{type:"category",data:["门店销售","店长","仓储","市场","区域","财务"],axisLabel:{{color:"{TD}",fontSize:9}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"万元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[
      {{name:"基本工资",type:"bar",stack:"total",data:[35.7,9.6,7.0,4.8,4.0,3.2],itemStyle:{{color:PNK}},barWidth:20}},
      {{name:"绩效奖金",type:"bar",stack:"total",data:[10.2,2.4,1.5,1.2,1.0,0.8],itemStyle:{{color:OR}}}},
      {{name:"五险一金",type:"bar",stack:"total",data:[10.7,2.9,2.1,1.4,1.2,1.0],itemStyle:{{color:BL}}}},
      {{name:"其他福利",type:"bar",stack:"total",data:[3.1,0.8,0.5,0.4,0.3,0.2],itemStyle:{{color:GN}}}}
    ]
  }});
}})();

(function(){{
  var c=chart("c-salary-trend");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{data:["薪酬总额","人均薪资"],textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"12%",right:"12%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["1月","2月","3月","4月","5月"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:[
      {{type:"value",name:"万元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
      {{type:"value",name:"元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}}}}
    ],
    series:[
      {{name:"薪酬总额",type:"bar",data:[122,118,125,130,128.6],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:PNK}},{{offset:1,color:"#880e4f"}}])}},barWidth:20,label:{{show:true,position:"top",color:"{TX}",fontSize:11}}}},
      {{name:"人均薪资",type:"line",yAxisIndex:1,data:[8200,8150,8350,8550,8650],itemStyle:{{color:BL}},lineStyle:{{width:2.5}},symbol:"circle",symbolSize:8}}
    ]
  }});
}})();

console.log("SZ + Personnel charts OK");
</script>"""

print(f"JS part 2 built: {len(JS_CODE2)} chars")

JS_CODE3 = f"""<script>
// Products charts
(function(){{
  var c=chart("c-ip-pie");
  c.setOption({{
    tooltip:{{trigger:"item",formatter:"{{b}}: {{c}}万 ({{d}}%)"}},
    series:[{{type:"pie",radius:"52%",center:["50%","45%"],
      label:{{formatter:"{{b}}\\n{{d}}%",color:"{TX}",fontSize:10}},
      emphasis:{{label:{{fontSize:16,fontWeight:"bold"}}}},
      data:[
        {{value:712,name:"MOLLY",itemStyle:{{color:PNK}}}},
        {{value:569,name:"SKULLPANDA",itemStyle:{{color:PP}}}},
        {{value:511,name:"DIMOO",itemStyle:{{color:BL}}}},
        {{value:326,name:"PUCKY",itemStyle:{{color:OR}}}},
        {{value:306,name:"LABUBU",itemStyle:{{color:GN}}}},
        {{value:193,name:"HIRONO",itemStyle:{{color:CY}}}},
        {{value:229,name:"其他IP",itemStyle:{{color:"#484f58"}}}}
      ]
    }}]
  }});
}})();

(function(){{
  var c=chart("c-ip-trend");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    legend:{{data:["MOLLY","SKULLPANDA","DIMOO","LABUBU"],textStyle:{{color:"{TD}"}},top:0}},
    grid:{{left:"10%",right:"6%",top:40,bottom:20}},
    xAxis:{{type:"category",data:["1月","2月","3月","4月","5月"],axisLabel:{{color:"{TD}"}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"万元",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[
      {{name:"MOLLY",type:"line",data:[580,450,550,620,712],itemStyle:{{color:PNK}},lineStyle:{{width:3}},areaStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:"rgba(233,30,99,0.25)"}},{{offset:1,color:"rgba(233,30,99,0.01)"}}])}},smooth:true,symbol:"circle",symbolSize:7}},
      {{name:"SKULLPANDA",type:"line",data:[420,350,420,500,569],itemStyle:{{color:PP}},lineStyle:{{width:2.5}},smooth:true,symbol:"circle",symbolSize:6}},
      {{name:"DIMOO",type:"line",data:[400,320,380,450,511],itemStyle:{{color:BL}},lineStyle:{{width:2.5}},smooth:true,symbol:"circle",symbolSize:6}},
      {{name:"LABUBU",type:"line",data:[200,180,230,270,306],itemStyle:{{color:GN}},lineStyle:{{width:2.5}},smooth:true,symbol:"circle",symbolSize:6}}
    ]
  }});
}})();

(function(){{
  var c=chart("c-top10");
  var items=["MOLLY-星座系列","SKULLPANDA-温度系列","DIMOO-水族馆","LABUBU-森林系列","MOLLY-校园系列","PUCKY-精灵系列","SKULLPANDA-漫游","DIMOO-社会大学","HIRONO-小王子","LABUBU-水果系列"];
  var vals=[185,152,138,125,118,105,98,92,85,78];
  c.setOption({{
    tooltip:{{trigger:"axis",axisPointer:{{type:"shadow"}}}},
    grid:{{left:150,right:50,top:5,bottom:20}},
    xAxis:{{type:"value",name:"万元/月",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    yAxis:{{type:"category",data:items.slice().reverse(),axisLabel:{{color:"{TX}",fontSize:9}},axisLine:{{lineStyle:{{color:"{BD}"}}}},inverse:true}},
    series:[{{type:"bar",data:vals.slice().reverse(),itemStyle:{{color:function(p){{var cs=[PNK,PP,BL,GN,PNK,OR,PP,BL,CY,GN];return cs[p.dataIndex%10]}}}},barWidth:14,label:{{show:true,position:"right",color:"{TX}",formatter:"{{c}}万",fontSize:11}}}}]
  }});
}})();

(function(){{
  var c=chart("c-price-band");
  c.setOption({{
    tooltip:{{trigger:"axis"}},
    grid:{{left:"10%",right:"6%",top:10,bottom:20}},
    xAxis:{{type:"category",data:[["<59元"],["59-99"],["99-159"],["159-259"],["259-499"],["500+"]],axisLabel:{{color:"{TD}",fontSize:10}},axisLine:{{lineStyle:{{color:"{BD}"}}}}}},
    yAxis:{{type:"value",name:"万元/月",nameTextStyle:{{color:"{TD}"}},axisLabel:{{color:"{TD}"}},splitLine:{{lineStyle:{{color:"{BD}",type:"dashed"}}}}}},
    series:[{{type:"bar",data:[285,712,854,512,341,142],itemStyle:{{color:new echarts.graphic.LinearGradient(0,0,0,1,[{{offset:0,color:PNK}},{{offset:1,color:"#880e4f"}}])}},barWidth:22,label:{{show:true,position:"top",color:"{TX}",formatter:"{{c}}万",fontSize:12}}}}]
  }});
}})();

console.log("All charts loaded: " + Object.keys(charts).length);
</script>"""

print(f"JS part 3 built: {len(JS_CODE3)} chars")

# ===== Assemble and write =====
FULL_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泡泡玛特 · 深圳市场分析驾驶舱 | Pop Mart Shenzhen</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
{css()}
</style>
</head>
<body>
{COCKPIT_HTML}
{SZ_HTML}
{PERSONNEL_HTML}
{PRODUCTS_HTML}
{DETAIL_HTML}
{JS_CODE}
{JS_CODE2}
{JS_CODE3}
</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"[OK] Dashboard written: {OUT}")
print(f"   Size: {len(FULL_HTML):,} chars")
print(f"   Charts: 16 ECharts visualizations")
print(f"   Tabs: Cockpit, Shenzhen, Personnel, Products, Detail")
