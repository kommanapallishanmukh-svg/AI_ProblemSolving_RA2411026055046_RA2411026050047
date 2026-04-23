<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tic-Tac-Toe AI — Minimax vs Alpha-Beta</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --card:      #1a2236;
    --border:    #2a3a5c;
    --neon-x:    #00e5ff;
    --neon-o:    #ff4081;
    --neon-win:  #69ff47;
    --text:      #e0e8ff;
    --muted:     #6b7fa8;
    --accent:    #7c5cfc;
    --font-head: 'Orbitron', monospace;
    --font-mono: 'Share Tech Mono', monospace;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 16px 48px;
    background-image:
      radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,92,252,0.18) 0%, transparent 60%),
      radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,229,255,0.12) 0%, transparent 55%);
  }

  /* ── HEADER ── */
  header {
    text-align: center;
    margin-bottom: 32px;
  }
  header h1 {
    font-family: var(--font-head);
    font-size: clamp(22px, 5vw, 42px);
    font-weight: 900;
    letter-spacing: 4px;
    text-transform: uppercase;
    background: linear-gradient(90deg, var(--neon-x), var(--accent), var(--neon-o));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  header p {
    color: var(--muted);
    font-size: 13px;
    margin-top: 6px;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  /* ── CONTROLS BAR ── */
  .controls {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    justify-content: center;
    margin-bottom: 28px;
  }
  .control-group {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--muted);
  }
  .control-group label { white-space: nowrap; }
  .control-group select {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    padding: 4px 10px;
    font-family: var(--font-mono);
    font-size: 13px;
    cursor: pointer;
    outline: none;
  }
  .algo-toggle {
    display: flex;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }
  .algo-toggle button {
    padding: 8px 18px;
    border: none;
    background: transparent;
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .algo-toggle button.active {
    background: var(--accent);
    color: #fff;
  }

  /* ── MAIN LAYOUT ── */
  .main-grid {
    display: grid;
    grid-template-columns: 280px 1fr 280px;
    gap: 24px;
    width: 100%;
    max-width: 1000px;
    align-items: start;
  }
  @media (max-width: 860px) {
    .main-grid { grid-template-columns: 1fr; }
    .side-panel { display: flex; flex-wrap: wrap; gap: 16px; }
    .side-panel .stat-card { flex: 1; min-width: 140px; }
  }

  /* ── SCORE PANEL ── */
  .side-panel { display: flex; flex-direction: column; gap: 16px; }
  .stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
  }
  .stat-card .label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
  }
  .stat-card .value {
    font-family: var(--font-head);
    font-size: 28px;
    font-weight: 700;
  }
  .stat-card.player .value { color: var(--neon-x); }
  .stat-card.ai     .value { color: var(--neon-o); }
  .stat-card.draw   .value { color: var(--muted); }

  /* ── GAME AREA ── */
  .game-area { display: flex; flex-direction: column; align-items: center; gap: 20px; }

  .status-bar {
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 15px;
    letter-spacing: 2px;
    text-transform: uppercase;
  }
  .status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--neon-win);
    animation: pulse 1.2s infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.7); }
  }

  /* ── BOARD ── */
  .board-wrapper {
    position: relative;
  }
  .board {
    display: grid;
    grid-template-columns: repeat(3, 110px);
    grid-template-rows: repeat(3, 110px);
    gap: 0;
    background: transparent;
    position: relative;
  }

  /* SVG grid lines */
  .board-lines {
    position: absolute;
    inset: 0;
    width: 330px;
    height: 330px;
    pointer-events: none;
  }

  .cell {
    width: 110px;
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-family: var(--font-head);
    font-size: 52px;
    font-weight: 900;
    position: relative;
    z-index: 1;
    transition: background 0.15s;
    user-select: none;
    -webkit-user-select: none;
  }
  .cell:hover:not(.taken):not(.locked) {
    background: rgba(124,92,252,0.08);
    border-radius: 8px;
  }
  .cell.x-mark { color: var(--neon-x); }
  .cell.o-mark { color: var(--neon-o); }
  .cell.win-cell {
    background: rgba(105,255,71,0.1);
    border-radius: 8px;
    animation: winFlash 0.6s ease;
  }
  @keyframes winFlash {
    0%   { background: rgba(105,255,71,0.4); }
    100% { background: rgba(105,255,71,0.1); }
  }
  .cell.thinking { cursor: not-allowed; }

  /* ── BUTTONS ── */
  .btn-row { display: flex; gap: 12px; }
  .btn {
    padding: 10px 28px;
    border-radius: 8px;
    border: 1.5px solid var(--border);
    background: var(--card);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 13px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn:hover { border-color: var(--accent); color: var(--accent); }
  .btn.primary {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }
  .btn.primary:hover { background: #9b7dff; border-color: #9b7dff; }

  /* ── COMPARISON PANEL ── */
  .compare-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .compare-panel .panel-title {
    font-family: var(--font-head);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
  }

  .compare-row { display: flex; flex-direction: column; gap: 6px; }
  .compare-row .row-label {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }
  .algo-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .algo-box {
    background: var(--surface);
    border-radius: 8px;
    padding: 10px;
    text-align: center;
  }
  .algo-box .algo-name {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .algo-box .algo-val {
    font-family: var(--font-head);
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
  }
  .algo-box.winner .algo-val { color: var(--neon-win); }
  .algo-box .algo-unit { font-size: 10px; color: var(--muted); margin-top: 2px; }

  .speedup-badge {
    background: rgba(105,255,71,0.1);
    border: 1px solid rgba(105,255,71,0.3);
    border-radius: 8px;
    padding: 8px 12px;
    text-align: center;
    font-size: 12px;
    color: var(--neon-win);
  }

  .history-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 200px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .history-item {
    display: grid;
    grid-template-columns: 28px 1fr 1fr;
    gap: 6px;
    align-items: center;
    font-size: 11px;
    padding: 6px 8px;
    background: var(--surface);
    border-radius: 6px;
    border-left: 3px solid var(--border);
  }
  .history-item.mm-won  { border-left-color: var(--neon-x); }
  .history-item.ab-won  { border-left-color: var(--neon-o); }
  .history-item.tie     { border-left-color: var(--muted); }
  .history-item .move-num { color: var(--muted); font-size: 10px; }
  .history-item .mm-col  { color: var(--neon-x); }
  .history-item .ab-col  { color: var(--neon-o); }

  /* ── THINKING OVERLAY ── */
  .thinking-overlay {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(10,14,26,0.7);
    border-radius: 12px;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 12px;
    z-index: 10;
  }
  .thinking-overlay.show { display: flex; }
  .thinking-label {
    font-family: var(--font-head);
    font-size: 14px;
    letter-spacing: 3px;
    color: var(--accent);
    animation: blink 1s infinite;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
  .dots span {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin: 0 3px;
    background: var(--accent);
    animation: bounce 1s infinite;
  }
  .dots span:nth-child(2) { animation-delay: 0.2s; }
  .dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%,80%,100%{transform:translateY(0)} 40%{transform:translateY(-8px)} }
</style>
</head>
<body>

<header>
  <h1>Tic-Tac-Toe AI</h1>
  <p>Minimax vs Alpha-Beta Pruning — Real-time Algorithm Analysis</p>
</header>

<!-- CONTROLS -->
<div class="controls">
  <div class="control-group">
    <label>You play as:</label>
    <select id="playerSide">
      <option value="X">X (goes first)</option>
      <option value="O">O (goes second)</option>
    </select>
  </div>
  <div class="algo-toggle">
    <button id="btnMinimax" class="active" onclick="setAlgo('minimax')">Minimax</button>
    <button id="btnAlpha"   onclick="setAlgo('alphabeta')">Alpha-Beta</button>
    <button id="btnBoth"    onclick="setAlgo('both')">Both</button>
  </div>
</div>

<!-- MAIN GRID -->
<div class="main-grid">

  <!-- LEFT: Score -->
  <div class="side-panel">
    <div class="stat-card player">
      <div class="label">You (X)</div>
      <div class="value" id="scorePlayer">0</div>
    </div>
    <div class="stat-card ai">
      <div class="label">AI (O)</div>
      <div class="value" id="scoreAI">0</div>
    </div>
    <div class="stat-card draw">
      <div class="label">Draws</div>
      <div class="value" id="scoreDraw">0</div>
    </div>
    <div class="stat-card" style="margin-top:8px;">
      <div class="label">Total Games</div>
      <div class="value" style="font-size:22px;color:var(--accent)" id="scoreTotal">0</div>
    </div>
  </div>

  <!-- CENTER: Game -->
  <div class="game-area">
    <div class="status-bar">
      <div class="status-dot" id="statusDot"></div>
      <span id="statusText">Your Turn — Place X</span>
    </div>

    <div class="board-wrapper">
      <!-- SVG Grid Lines -->
      <svg class="board-lines" viewBox="0 0 330 330" xmlns="http://www.w3.org/2000/svg">
        <!-- Vertical lines -->
        <line x1="110" y1="12" x2="110" y2="318" stroke="#2a3a5c" stroke-width="2" stroke-linecap="round"/>
        <line x1="220" y1="12" x2="220" y2="318" stroke="#2a3a5c" stroke-width="2" stroke-linecap="round"/>
        <!-- Horizontal lines -->
        <line x1="12" y1="110" x2="318" y2="110" stroke="#2a3a5c" stroke-width="2" stroke-linecap="round"/>
        <line x1="12" y1="220" x2="318" y2="220" stroke="#2a3a5c" stroke-width="2" stroke-linecap="round"/>
      </svg>

      <div class="board" id="board">
        <!-- 9 cells generated by JS -->
      </div>

      <div class="thinking-overlay" id="thinkingOverlay">
        <div class="thinking-label">AI THINKING</div>
        <div class="dots"><span></span><span></span><span></span></div>
      </div>
    </div>

    <div class="btn-row">
      <button class="btn primary" onclick="resetGame()">New Game</button>
      <button class="btn" onclick="resetAll()">Reset All</button>
    </div>
  </div>

  <!-- RIGHT: Comparison -->
  <div class="compare-panel">
    <div class="panel-title">Algorithm Analysis</div>

    <div class="compare-row">
      <div class="row-label">Nodes Explored</div>
      <div class="algo-compare">
        <div class="algo-box" id="boxNodesM">
          <div class="algo-name">Minimax</div>
          <div class="algo-val" id="nodesM">—</div>
          <div class="algo-unit">states</div>
        </div>
        <div class="algo-box" id="boxNodesA">
          <div class="algo-name">Alpha-Beta</div>
          <div class="algo-val" id="nodesA">—</div>
          <div class="algo-unit">states</div>
        </div>
      </div>
    </div>

    <div class="compare-row">
      <div class="row-label">Execution Time</div>
      <div class="algo-compare">
        <div class="algo-box" id="boxTimeM">
          <div class="algo-name">Minimax</div>
          <div class="algo-val" id="timeM">—</div>
          <div class="algo-unit">ms</div>
        </div>
        <div class="algo-box" id="boxTimeA">
          <div class="algo-name">Alpha-Beta</div>
          <div class="algo-val" id="timeA">—</div>
          <div class="algo-unit">ms</div>
        </div>
      </div>
    </div>

    <div class="speedup-badge" id="speedupBadge" style="display:none"></div>

    <div class="compare-row">
      <div class="row-label">Move History</div>
      <div style="display:grid;grid-template-columns:28px 1fr 1fr;gap:6px;font-size:10px;color:var(--muted);padding:0 8px;margin-bottom:2px;">
        <span>#</span><span style="color:var(--neon-x)">Minimax</span><span style="color:var(--neon-o)">Alpha-Beta</span>
      </div>
      <div class="history-list" id="historyList">
        <div style="color:var(--muted);font-size:11px;text-align:center;padding:12px">No moves yet</div>
      </div>
    </div>

    <div style="font-size:10px;color:var(--muted);line-height:1.6;padding-top:4px;border-top:1px solid var(--border)">
      <strong style="color:var(--text)">Minimax</strong> — explores every possible game state exhaustively.<br><br>
      <strong style="color:var(--text)">Alpha-Beta</strong> — prunes branches that can't affect the outcome, exploring fewer states.
    </div>
  </div>

</div>

<script>
// ═══════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════
let board       = Array(9).fill(null);
let playerMark  = 'X';
let aiMark      = 'O';
let gameOver    = false;
let scores      = { player: 0, ai: 0, draw: 0 };
let activeAlgo  = 'minimax';   // 'minimax' | 'alphabeta' | 'both'
let moveNumber  = 0;
let history     = [];

// ═══════════════════════════════════════════════════
//  INIT BOARD CELLS
// ═══════════════════════════════════════════════════
function initBoard() {
  const boardEl = document.getElementById('board');
  boardEl.innerHTML = '';
  for (let i = 0; i < 9; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.dataset.index = i;
    cell.addEventListener('click', () => onCellClick(i));
    boardEl.appendChild(cell);
  }
}

// ═══════════════════════════════════════════════════
//  GAME LOGIC HELPERS
// ═══════════════════════════════════════════════════
const WIN_LINES = [
  [0,1,2],[3,4,5],[6,7,8],  // rows
  [0,3,6],[1,4,7],[2,5,8],  // cols
  [0,4,8],[2,4,6]           // diagonals
];

function checkWinner(b) {
  for (let [a, x, c] of WIN_LINES) {
    if (b[a] && b[a] === b[x] && b[a] === b[c]) {
      return { winner: b[a], line: [a, x, c] };
    }
  }
  return null;
}

function isDraw(b) { return b.every(c => c !== null); }

function getEmpty(b) {
  return b.map((v, i) => v === null ? i : -1).filter(i => i !== -1);
}

// ═══════════════════════════════════════════════════
//  ALGORITHM 1: MINIMAX
// ═══════════════════════════════════════════════════
let mmNodes = 0;

function minimax(b, isMaximizing) {
  mmNodes++;
  const result = checkWinner(b);
  if (result) return result.winner === aiMark ? 10 : -10;
  if (isDraw(b)) return 0;

  if (isMaximizing) {
    let best = -Infinity;
    for (let i of getEmpty(b)) {
      b[i] = aiMark;
      best = Math.max(best, minimax(b, false));
      b[i] = null;
    }
    return best;
  } else {
    let best = Infinity;
    for (let i of getEmpty(b)) {
      b[i] = playerMark;
      best = Math.min(best, minimax(b, true));
      b[i] = null;
    }
    return best;
  }
}

function bestMoveMinimax(b) {
  mmNodes = 0;
  const t0 = performance.now();
  let bestScore = -Infinity, bestMove = -1;
  for (let i of getEmpty(b)) {
    b[i] = aiMark;
    const score = minimax(b, false);
    b[i] = null;
    if (score > bestScore) { bestScore = score; bestMove = i; }
  }
  const t1 = performance.now();
  return { move: bestMove, nodes: mmNodes, time: +(t1 - t0).toFixed(3) };
}

// ═══════════════════════════════════════════════════
//  ALGORITHM 2: ALPHA-BETA PRUNING
// ═══════════════════════════════════════════════════
let abNodes = 0;

function alphabeta(b, isMaximizing, alpha, beta) {
  abNodes++;
  const result = checkWinner(b);
  if (result) return result.winner === aiMark ? 10 : -10;
  if (isDraw(b)) return 0;

  if (isMaximizing) {
    let best = -Infinity;
    for (let i of getEmpty(b)) {
      b[i] = aiMark;
      best = Math.max(best, alphabeta(b, false, alpha, beta));
      b[i] = null;
      alpha = Math.max(alpha, best);
      if (beta <= alpha) break;   // ← PRUNING: beta cut-off
    }
    return best;
  } else {
    let best = Infinity;
    for (let i of getEmpty(b)) {
      b[i] = playerMark;
      best = Math.min(best, alphabeta(b, true, alpha, beta));
      b[i] = null;
      beta = Math.min(beta, best);
      if (beta <= alpha) break;   // ← PRUNING: alpha cut-off
    }
    return best;
  }
}

function bestMoveAlphaBeta(b) {
  abNodes = 0;
  const t0 = performance.now();
  let bestScore = -Infinity, bestMove = -1;
  for (let i of getEmpty(b)) {
    b[i] = aiMark;
    const score = alphabeta(b, false, -Infinity, Infinity);
    b[i] = null;
    if (score > bestScore) { bestScore = score; bestMove = i; }
  }
  const t1 = performance.now();
  return { move: bestMove, nodes: abNodes, time: +(t1 - t0).toFixed(3) };
}

// ═══════════════════════════════════════════════════
//  CELL CLICK HANDLER
// ═══════════════════════════════════════════════════
function onCellClick(index) {
  if (gameOver || board[index] !== null) return;
  placeMove(index, playerMark);
  if (gameOver) return;
  setTimeout(aiMove, 300);
}

function placeMove(index, mark) {
  board[index] = mark;
  renderBoard();
  const result = checkWinner(board);
  if (result) { endGame(result.winner, result.line); return; }
  if (isDraw(board)) { endGame(null, null); return; }
  if (mark === playerMark) {
    setStatus(`AI is thinking...`, false);
  } else {
    setStatus(`Your Turn — Place ${playerMark}`, true);
  }
}

// ═══════════════════════════════════════════════════
//  AI MOVE
// ═══════════════════════════════════════════════════
function aiMove() {
  if (gameOver) return;
  showThinking(true);

  setTimeout(() => {
    let mmResult = null, abResult = null;

    if (activeAlgo === 'minimax' || activeAlgo === 'both') {
      mmResult = bestMoveMinimax([...board]);
    }
    if (activeAlgo === 'alphabeta' || activeAlgo === 'both') {
      abResult = bestMoveAlphaBeta([...board]);
    }

    // Pick move to actually play
    const chosenMove = (abResult || mmResult).move;

    // Update comparison panel
    updateComparison(mmResult, abResult);

    // Record history
    moveNumber++;
    addHistory(moveNumber, mmResult, abResult);

    showThinking(false);
    placeMove(chosenMove, aiMark);
  }, 80);
}

// ═══════════════════════════════════════════════════
//  END GAME
// ═══════════════════════════════════════════════════
function endGame(winner, line) {
  gameOver = true;
  if (winner === playerMark) {
    scores.player++;
    setStatus('You Win! 🎉', true);
    if (line) highlightWin(line);
  } else if (winner === aiMark) {
    scores.ai++;
    setStatus('AI Wins!', false);
    if (line) highlightWin(line);
  } else {
    scores.draw++;
    setStatus('Draw — Perfect Play!', true);
  }
  scores.total = (scores.total || 0) + 1;
  updateScores();
  lockBoard();
}

function lockBoard() {
  document.querySelectorAll('.cell').forEach(c => c.classList.add('locked', 'taken'));
}

function highlightWin(line) {
  line.forEach(i => {
    document.querySelectorAll('.cell')[i].classList.add('win-cell');
  });
}

// ═══════════════════════════════════════════════════
//  RENDER
// ═══════════════════════════════════════════════════
function renderBoard() {
  const cells = document.querySelectorAll('.cell');
  board.forEach((val, i) => {
    cells[i].textContent = val || '';
    cells[i].className = 'cell';
    if (val === 'X') cells[i].classList.add('x-mark', 'taken');
    if (val === 'O') cells[i].classList.add('o-mark', 'taken');
  });
}

function setStatus(text, playerActive) {
  document.getElementById('statusText').textContent = text;
  const dot = document.getElementById('statusDot');
  dot.style.background = playerActive ? 'var(--neon-win)' : 'var(--neon-o)';
}

function updateScores() {
  document.getElementById('scorePlayer').textContent = scores.player;
  document.getElementById('scoreAI').textContent     = scores.ai;
  document.getElementById('scoreDraw').textContent   = scores.draw;
  document.getElementById('scoreTotal').textContent  = scores.total || 0;
}

function showThinking(show) {
  document.getElementById('thinkingOverlay').classList.toggle('show', show);
}

// ═══════════════════════════════════════════════════
//  COMPARISON PANEL
// ═══════════════════════════════════════════════════
function updateComparison(mm, ab) {
  // Nodes
  if (mm) {
    document.getElementById('nodesM').textContent = mm.nodes.toLocaleString();
    document.getElementById('timeM').textContent  = mm.time.toFixed(3);
  }
  if (ab) {
    document.getElementById('nodesA').textContent = ab.nodes.toLocaleString();
    document.getElementById('timeA').textContent  = ab.time.toFixed(3);
  }

  // Highlight winner
  ['boxNodesM','boxNodesA','boxTimeM','boxTimeA'].forEach(id =>
    document.getElementById(id).classList.remove('winner'));

  if (mm && ab) {
    if (ab.nodes < mm.nodes) document.getElementById('boxNodesA').classList.add('winner');
    else                      document.getElementById('boxNodesM').classList.add('winner');

    if (ab.time <= mm.time)  document.getElementById('boxTimeA').classList.add('winner');
    else                      document.getElementById('boxTimeM').classList.add('winner');

    const speedup = mm.nodes > 0 ? (mm.nodes / ab.nodes).toFixed(1) : '—';
    const badge = document.getElementById('speedupBadge');
    badge.style.display = 'block';
    badge.textContent = `Alpha-Beta explored ${speedup}× fewer states than Minimax`;
  }
}

function addHistory(num, mm, ab) {
  const list = document.getElementById('historyList');
  if (num === 1) list.innerHTML = '';

  const item = document.createElement('div');
  const mmVal = mm ? mm.nodes : '—';
  const abVal = ab ? ab.nodes : '—';

  let cls = 'history-item';
  if (mm && ab) {
    if (ab.nodes < mm.nodes) cls += ' ab-won';
    else cls += ' mm-won';
  } else if (mm) cls += ' mm-won';
  else            cls += ' ab-won';

  item.className = cls;
  item.innerHTML = `
    <span class="move-num">#${num}</span>
    <span class="mm-col">${typeof mmVal === 'number' ? mmVal.toLocaleString() : mmVal}</span>
    <span class="ab-col">${typeof abVal === 'number' ? abVal.toLocaleString() : abVal}</span>
  `;
  list.insertBefore(item, list.firstChild);
}

// ═══════════════════════════════════════════════════
//  CONTROLS
// ═══════════════════════════════════════════════════
function setAlgo(algo) {
  activeAlgo = algo;
  document.getElementById('btnMinimax').classList.toggle('active', algo === 'minimax');
  document.getElementById('btnAlpha').classList.toggle('active',   algo === 'alphabeta');
  document.getElementById('btnBoth').classList.toggle('active',    algo === 'both');
}

document.getElementById('playerSide').addEventListener('change', function() {
  playerMark = this.value;
  aiMark     = playerMark === 'X' ? 'O' : 'X';
  resetGame();
});

function resetGame() {
  board    = Array(9).fill(null);
  gameOver = false;
  moveNumber = 0;
  initBoard();
  renderBoard();
  showThinking(false);

  if (playerMark === 'X') {
    setStatus(`Your Turn — Place X`, true);
  } else {
    setStatus(`AI goes first...`, false);
    setTimeout(aiMove, 400);
  }
}

function resetAll() {
  scores = { player: 0, ai: 0, draw: 0, total: 0 };
  history = [];
  updateScores();
  document.getElementById('historyList').innerHTML =
    '<div style="color:var(--muted);font-size:11px;text-align:center;padding:12px">No moves yet</div>';
  document.getElementById('nodesM').textContent = '—';
  document.getElementById('nodesA').textContent = '—';
  document.getElementById('timeM').textContent  = '—';
  document.getElementById('timeA').textContent  = '—';
  document.getElementById('speedupBadge').style.display = 'none';
  resetGame();
}

// ── BOOT ──
initBoard();
setStatus(`Your Turn — Place X`, true);
</script>
</body>
</html>
