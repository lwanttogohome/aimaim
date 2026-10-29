
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aim Training",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp { background:#111317; color:#f5f5f5; }
.block-container { max-width:1200px; padding-top:1.5rem; }
h1,h2,h3,p,label { color:#f5f5f5; }
div[data-testid="stSelectbox"] > div > div {
    background:#22252c; color:white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='color:#ff4655;margin-bottom:0'>🎯 AIM TRAINING</h1>",
    unsafe_allow_html=True,
)
st.caption("VALORANT 스타일 에임 연습 · 사격 · 플릭 · 반응 · 트래킹")

c1, c2, c3 = st.columns(3)

with c1:
    mode = st.selectbox(
        "훈련 모드",
        ["정밀 사격", "플릭 에임", "반응 훈련", "트래킹 에임"],
    )

with c2:
    difficulty = st.selectbox(
        "난이도", ["쉬움", "보통", "어려움"], index=1
    )

with c3:
    duration = st.selectbox(
        "훈련 시간", [30, 60, 90], index=0,
        format_func=lambda x: f"{x}초",
    )

sizes = {"쉬움": 48, "보통": 34, "어려움": 23}
speeds = {"쉬움": 1800, "보통": 1100, "어려움": 650}
tracking_speeds = {"쉬움": 100, "보통": 170, "어려움": 240}

mode_codes = {
    "정밀 사격": "precision",
    "플릭 에임": "flick",
    "반응 훈련": "reaction",
    "트래킹 에임": "tracking",
}

size = sizes[difficulty]
speed = speeds[difficulty]
tracking_speed = tracking_speeds[difficulty]
mode_code = mode_codes[mode]

descriptions = {
    "정밀 사격": "표적을 하나씩 정확하게 클릭하세요.",
    "플릭 에임": "위치가 바뀌는 표적을 빠르게 조준하세요.",
    "반응 훈련": "나타나는 표적을 제한 시간 안에 맞히세요.",
    "트래킹 에임": "마우스를 움직여 이동하는 표적 위에 계속 유지하세요.",
}

st.markdown(
    f"""
    <div style="background:#202329;border-left:5px solid #ff4655;
    padding:14px 18px;margin:12px 0;border-radius:4px">
    <b>{mode}</b><br>
    <span style="color:#c7c9d0">{descriptions[mode]}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

game = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing:border-box}
body {
    margin:0;background:#111317;color:#f5f5f5;
    font-family:Arial,"Malgun Gothic",sans-serif
}
.stats {
    display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
    gap:8px;margin-bottom:12px
}
.stat {
    background:#202329;border:1px solid #373a43;
    border-radius:5px;padding:12px 8px
}
.label {color:#aeb2bc;font-size:12px;margin-bottom:7px}
.value {font-size:clamp(17px,3vw,26px);font-weight:800}
.red {color:#ff4655}
.arena {
    height:450px;position:relative;overflow:hidden;
    background:radial-gradient(ellipse at center,#282b32,#13151a);
    border:1px solid #41444c;cursor:crosshair;
    user-select:none;touch-action:pan-y
}
.grid {
    position:absolute;inset:0;pointer-events:none;opacity:.17;
    background-image:linear-gradient(#666 1px,transparent 1px),
    linear-gradient(90deg,#666 1px,transparent 1px);
    background-size:40px 40px
}
.target {
    position:absolute;display:none;padding:0;
    border:3px solid white;border-radius:50%;
    transform:translate(-50%,-50%);background:#ff4655;
    box-shadow:0 0 0 5px #ff465533,0 0 22px #ff465577;
    z-index:2;pointer-events:auto
}
.target:before {
    content:"";position:absolute;inset:20%;
    border:2px solid white;border-radius:50%
}
.target:after {
    content:"";position:absolute;width:20%;height:20%;
    left:40%;top:40%;background:white;border-radius:50%
}
.crosshair {
    position:absolute;width:18px;height:18px;
    transform:translate(-50%,-50%);pointer-events:none;
    display:none;z-index:4
}
.crosshair:before,.crosshair:after {
    content:"";position:absolute;background:white
}
.crosshair:before {width:2px;height:18px;left:8px}
.crosshair:after {height:2px;width:18px;top:8px}
.overlay {
    position:absolute;inset:0;z-index:5;
    display:flex;align-items:center;justify-content:center;
    background:#0d1015df;text-align:center;padding:16px
}
.panel {width:min(100%,400px)}
.panel h2 {font-size:27px;margin:0 0 10px}
.panel p {font-size:14px;color:#c4c7cf;line-height:1.65}
.action {
    background:#ff4655;color:white;border:0;border-radius:3px;
    padding:13px 24px;font-weight:800;cursor:pointer;font-size:15px
}
.secondary {
    border:1px solid #484c56;background:#252830;color:white;
    padding:10px 15px;cursor:pointer;border-radius:3px
}
.bottom {
    display:flex;justify-content:space-between;align-items:center;
    flex-wrap:wrap;gap:8px;margin-top:12px
}
.note {color:#aeb2bc;font-size:12px}
.results {
    display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0
}
.cell {padding:11px;background:#202329;border:1px solid #42454e}
.cell small {display:block;color:#aeb2bc;margin-bottom:6px}
.cell strong {font-size:21px}
@media(max-width:500px) {
    .arena {height:390px}
    .stat {padding:9px 5px}
    .label {font-size:10px}
}
</style>
</head>
<body>
<div class="stats">
 <div class="stat"><div class="label">남은 시간</div><div class="value" id="time">30초</div></div>
 <div class="stat"><div class="label" id="scoreLabel">명중</div><div class="value red" id="score">0</div></div>
 <div class="stat"><div class="label" id="accuracyLabel">정확도</div><div class="value" id="accuracy">0%</div></div>
 <div class="stat"><div class="label" id="reactionLabel">평균 반응</div><div class="value" id="reaction">--</div></div>
</div>

<div class="arena" id="arena">
 <div class="grid"></div>
 <div class="crosshair" id="crosshair"></div>
 <div class="target" id="target"></div>
 <div class="overlay" id="overlay">
  <div class="panel" id="panel">
   <h2>훈련 준비 완료</h2>
   <p id="intro">표적을 정확하게 조준하세요.</p>
   <button class="action" id="start">훈련 시작</button>
  </div>
 </div>
</div>

<div class="bottom">
 <span class="note" id="status">시작 버튼을 눌러 훈련하세요.</span>
 <button class="secondary" id="restart">다시 시작 ↻</button>
</div>

<script>
(() => {
 const MODE = "__MODE__";
 const DURATION = __DURATION__;
 const SIZE = __SIZE__;
 const MOVE_INTERVAL = __SPEED__;
 const TRACK_SPEED = __TRACK_SPEED__;

 const arena = document.getElementById("arena");
 const target = document.getElementById("target");
 const overlay = document.getElementById("overlay");
 const panel = document.getElementById("panel");
 const crosshair = document.getElementById("crosshair");

 let running = false;
 let hits = 0, misses = 0;
 let reactionTimes = [];
 let deadline = 0, spawnTime = 0;
 let countdown = null, movement = null, targetTimeout = null;
 let mouseX = -1000, mouseY = -1000;
 let tx = 0, ty = 0, vx = 1, vy = 1;
 let lastFrame = 0, trackedMs = 0, totalTrackMs = 0;
 let trackingLoop = null;

 function updateStats() {
   const attempts = hits + misses;
   const acc = attempts ? Math.round(hits / attempts * 100) : 0;
   const avg = reactionTimes.length
     ? Math.round(reactionTimes.reduce((a,b)=>a+b,0)/reactionTimes.length)
     : 0;

   document.getElementById("score").textContent =
     MODE === "tracking" ? Math.floor(trackedMs / 1000) + "s" : hits;

   document.getElementById("accuracy").textContent =
     MODE === "tracking"
       ? (totalTrackMs ? Math.round(trackedMs / totalTrackMs * 100) : 0) + "%"
       : acc + "%";

   document.getElementById("reaction").textContent =
     avg ? avg + "ms" : "--";
 }

 function randomPosition() {
   const pad = SIZE / 2 + 8;
   return {
     x: pad + Math.random() * Math.max(1, arena.clientWidth - 2 * pad),
     y: pad + Math.random() * Math.max(1, arena.clientHeight - 2 * pad)
   };
 }

 function placeTarget() {
   if (!running) return;
   const p = randomPosition();
   tx = p.x;
   ty = p.y;
   target.style.width = SIZE + "px";
   target.style.height = SIZE + "px";
   target.style.left = tx + "px";
   target.style.top = ty + "px";
   target.style.display = "block";
   spawnTime = performance.now();

   clearTimeout(targetTimeout);

   if (MODE === "reaction") {
     targetTimeout = setTimeout(() => {
       if (!running || target.style.display === "none") return;
       target.style.display = "none";
       misses++;
       updateStats();
       setTimeout(() => { if (running) placeTarget(); }, 180);
     }, Math.max(800, MOVE_INTERVAL + 300));
   }
 }

 function startTracking() {
   const p = randomPosition();
   tx = p.x;
   ty = p.y;
   const angle = Math.random() * Math.PI * 2;
   vx = Math.cos(angle);
   vy = Math.sin(angle);
   lastFrame = performance.now();

   trackingLoop = setInterval(() => {
     if (!running) return;

     const now = performance.now();
     const dt = Math.min(0.04, (now - lastFrame) / 1000);
     lastFrame = now;

     const pad = SIZE / 2 + 5;
     tx += vx * TRACK_SPEED * dt;
     ty += vy * TRACK_SPEED * dt;

     if (tx < pad || tx > arena.clientWidth - pad) {
       vx *= -1;
       tx = Math.max(pad, Math.min(arena.clientWidth - pad, tx));
     }
     if (ty < pad || ty > arena.clientHeight - pad) {
       vy *= -1;
       ty = Math.max(pad, Math.min(arena.clientHeight - pad, ty));
     }

     target.style.left = tx + "px";
     target.style.top = ty + "px";

     const rect = arena.getBoundingClientRect();
     const mx = mouseX;
     const my = mouseY;
     const cx = rect.left + tx;
     const cy = rect.top + ty;
     const radius = SIZE / 2 + 3;
     const onTarget = Math.hypot(mx - cx, my - cy) <= radius;

     totalTrackMs += dt * 1000;
     if (onTarget) trackedMs += dt * 1000;

     updateStats();
   }, 16);
 }

 function startGame() {
   clearInterval(countdown);
   clearInterval(movement);
   clearInterval(trackingLoop);
   clearTimeout(targetTimeout);

   hits = 0;
   misses = 0;
   reactionTimes = [];
   trackedMs = 0;
   totalTrackMs = 0;
   running = true;
   deadline = performance.now() + DURATION * 1000;

   overlay.style.display = "none";
   crosshair.style.display = "block";
   document.getElementById("status").textContent =
     MODE === "tracking" ? "마우스를 표적 위에 유지하세요!" : "표적을 조준하세요!";

   if (MODE === "tracking") {
     document.getElementById("scoreLabel").textContent = "추적 성공";
     document.getElementById("accuracyLabel").textContent = "추적률";
     document.getElementById("reactionLabel").textContent = "추적 시간";
     target.style.width = SIZE + "px";
     target.style.height = SIZE + "px";
     target.style.display = "block";
     startTracking();
   } else {
     document.getElementById("scoreLabel").textContent = "명중";
     document.getElementById("accuracyLabel").textContent = "정확도";
     document.getElementById("reactionLabel").textContent = "평균 반응";
     placeTarget();

     if (MODE === "flick") {
       movement = setInterval(placeTarget, MOVE_INTERVAL);
     }
     if (MODE === "precision") {
       movement = setInterval(placeTarget, Math.max(2300, MOVE_INTERVAL * 2));
     }
   }

   updateStats();

   countdown = setInterval(() => {
     const remaining = Math.max(0, deadline - performance.now());
     document.getElementById("time").textContent =
       (remaining / 1000).toFixed(1) + "초";
     if (remaining <= 0) finishGame();
   }, 50);
 }

 function finishGame() {
   if (!running) return;
   running = false;
   clearInterval(countdown);
   clearInterval(movement);
   clearInterval(trackingLoop);
   clearTimeout(targetTimeout);
   target.style.display = "none";
   overlay.style.display = "flex";
   crosshair.style.display = "none";

   const attempts = hits + misses;
   const acc = attempts ? Math.round(hits / attempts * 100) : 0;
   const avg = reactionTimes.length
     ? Math.round(reactionTimes.reduce((a,b)=>a+b,0)/reactionTimes.length)
     : 0;

   let resultHtml = "";

   if (MODE === "tracking") {
     const trackingRate = totalTrackMs
       ? Math.round(trackedMs / totalTrackMs * 100) : 0;

     resultHtml = `
       <div style="font-size:34px;font-weight:800;color:#ff4655">
         ${(trackedMs/1000).toFixed(1)}초 추적 성공
       </div>
       <div class="results">
        <div class="cell"><small>추적률</small><strong>${trackingRate}%</strong></div>
        <div class="cell"><small>총 훈련 시간</small><strong>${DURATION}초</strong></div>
       </div>
       <p>표적 위에 커서를 유지한 시간이 길수록 좋은 결과입니다.</p>
     `;
   } else {
     resultHtml = `
       <div style="font-size:34px;font-weight:800;color:#ff4655">${hits}회 명중</div>
       <div class="results">
        <div class="cell"><small>정확도</small><strong>${acc}%</strong></div>
        <div class="cell"><small>평균 반응</small><strong>${avg ? avg+"ms" : "--"}</strong></div>
        <div class="cell"><small>빗나감</small><strong>${misses}회</strong></div>
        <div class="cell"><small>총 시도</small><strong>${attempts}회</strong></div>
       </div>
     `;
   }

   panel.innerHTML = `
     <h2>훈련 종료</h2>
     <p>이번 훈련의 결과입니다.</p>
     ${resultHtml}
     <button class="action" id="again">다시 훈련하기 ↻</button>
   `;

   document.getElementById("again").addEventListener("click", startGame);
   document.getElementById("time").textContent = "0.0초";
   document.getElementById("status").textContent = "훈련이 끝났습니다.";
   updateStats();
 }

 arena.addEventListener("mousemove", e => {
   mouseX = e.clientX;
   mouseY = e.clientY;
   const rect = arena.getBoundingClientRect();
   crosshair.style.left = (e.clientX - rect.left) + "px";
   crosshair.style.top = (e.clientY - rect.top) + "px";
 });

 arena.addEventListener("mouseleave", () => {
   mouseX = -1000;
   mouseY = -1000;
 });

 arena.addEventListener("click", e => {
   if (!running || MODE === "tracking") return;

   if (e.target === target) {
     hits++;
     reactionTimes.push(Math.round(performance.now() - spawnTime));
     clearTimeout(targetTimeout);

     if (MODE === "precision") {
       target.style.display = "none";
       setTimeout(() => { if (running) placeTarget(); }, 160);
     } else {
       placeTarget();
     }
   } else {
     misses++;
   }
   updateStats();
 });

 document.getElementById("intro").textContent =
   MODE === "tracking"
     ? "움직이는 표적 위에 마우스를 유지하세요. 클릭할 필요가 없습니다."
     : "표적을 빠르고 정확하게 클릭하세요.";

 document.getElementById("start").addEventListener("click", startGame);
 document.getElementById("restart").addEventListener("click", startGame);

 window.addEventListener("resize", () => {
   if (running && MODE === "tracking") {
     tx = Math.min(tx, arena.clientWidth - SIZE / 2);
     ty = Math.min(ty, arena.clientHeight - SIZE / 2);
   } else if (running) {
     placeTarget();
   }
 });
})();
</script>
</body>
</html>
"""

game = (
    game
    .replace("__MODE__", mode_code)
    .replace("__DURATION__", str(duration))
    .replace("__SIZE__", str(size))
    .replace("__SPEED__", str(speed))
    .replace("__TRACK_SPEED__", str(tracking_speed))
)

components.html(game, height=590, scrolling=False)

st.markdown("---")
st.caption(
    "개인 연습용 브라우저 미니게임입니다. "
    "실제 VALORANT 클라이언트나 Riot 계정과 연동되지 않습니다."
)
