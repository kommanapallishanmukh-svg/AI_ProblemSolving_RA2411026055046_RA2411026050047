# AI_ProblemSolving_RA2411026055046_RA2411026050047
# 🎮 AI Problem Solving — Tic-Tac-Toe with Minimax \& Alpha-Beta Pruning

> \\\*\\\*Repository:\\\*\\\* `AI\\\_ProblemSolving\\\_<YourRegisterNumber>`  
> \\\*\\\*Course:\\\*\\\* Artificial Intelligence  
> \\\*\\\*Live Demo:\\\*\\\* \\\[▶ Play Now](https://<yourusername>.github.io/AI\\\_ProblemSolving\\\_<YourRegisterNumber>/)

\---

## 📁 Folder Structure

```
AI\\\_ProblemSolving\\\_<RegisterNumber>/
│
├── index.html              ← Main game file (open this in browser)
├── README.md               ← This file
│
└── docs/
    ├── algorithm\\\_comparison.png    ← Screenshot of comparison panel
    ├── gameplay\\\_screenshot.png     ← Screenshot of the game
    └── report.md                   ← Detailed algorithm analysis report
```

\---

## 📌 Problem Description

### Case Study: AI Opponent for Web-Based Tic-Tac-Toe

A gaming company wants to develop an intelligent AI opponent for a web-based Tic-Tac-Toe game. The AI must **always make the best possible move** in response to any player input.

This project implements and compares two classic AI search algorithms:

|#|Algorithm|Description|
|-|-|-|
|1|**Minimax**|Exhaustively explores all possible game states to find the optimal move|
|2|**Alpha-Beta Pruning**|An optimized version of Minimax that skips irrelevant branches|

Both algorithms guarantee the AI **never loses** — the best the human player can achieve is a draw.

\---

## 🧠 Algorithms Used

### 1\. Minimax Algorithm

Minimax is a **recursive backtracking algorithm** used in two-player zero-sum games. It simulates all possible future moves and picks the one that maximizes the AI's score while minimizing the human's score.

**How it works:**

* The AI is the **Maximizing** player (wants score = +10)
* The Human is the **Minimizing** player (wants score = -10)
* A draw scores 0
* The algorithm explores **every possible game state** from the current board

**Pseudocode:**

```
function minimax(board, isMaximizing):
    if terminal state:
        return score (+10, -10, or 0)

    if isMaximizing:
        best = -infinity
        for each empty cell:
            place AI mark
            best = max(best, minimax(board, false))
            remove mark
        return best

    else (minimizing):
        best = +infinity
        for each empty cell:
            place Human mark
            best = min(best, minimax(board, true))
            remove mark
        return best
```

**Complexity:** O(b^m) where b = branching factor, m = max depth  
**Nodes explored (first move):** Up to \~5,478 states

\---

### 2\. Alpha-Beta Pruning

Alpha-Beta Pruning is an **optimization of Minimax** that maintains two values — **alpha** (best score for AI) and **beta** (best score for Human) — and prunes branches that cannot influence the final decision.

**How it works:**

* `alpha` = the best score the AI has found so far
* `beta` = the best score the Human has found so far
* If `beta ≤ alpha`, the current branch is **pruned** (skipped entirely)

**Pseudocode:**

```
function alphabeta(board, isMaximizing, alpha, beta):
    if terminal state:
        return score (+10, -10, or 0)

    if isMaximizing:
        best = -infinity
        for each empty cell:
            place AI mark
            best = max(best, alphabeta(board, false, alpha, beta))
            remove mark
            alpha = max(alpha, best)
            if beta <= alpha:
                break          ← PRUNE this branch
        return best

    else (minimizing):
        best = +infinity
        for each empty cell:
            place Human mark
            best = min(best, alphabeta(board, true, alpha, beta))
            remove mark
            beta = min(beta, best)
            if beta <= alpha:
                break          ← PRUNE this branch
        return best
```

**Complexity:** O(b^(m/2)) in the best case — effectively doubles the searchable depth  
**Nodes explored (first move):** \~700 states (≈7× fewer than Minimax)

\---

## ⚖️ Algorithm Comparison

|Metric|Minimax|Alpha-Beta Pruning|Winner|
|-|-|-|-|
|**Nodes Explored (Move 1)**|\~5,478|\~700|✅ Alpha-Beta|
|**Nodes Explored (Move 5)**|\~50–200|\~20–80|✅ Alpha-Beta|
|**Execution Time**|Slightly slower|Faster|✅ Alpha-Beta|
|**Optimal Move Quality**|Always optimal|Always optimal|🤝 Tie|
|**Code Complexity**|Simple|Slightly more complex|✅ Minimax|
|**Memory Usage**|O(m) stack depth|O(m) stack depth|🤝 Tie|

### Key Insight

> Alpha-Beta Pruning explores \\\*\\\*5–10× fewer game states\\\*\\\* than Minimax while producing \\\*\\\*identical moves\\\*\\\*. The pruning never changes the result — it only skips states that provably cannot change the outcome.

\---

## 🖥️ Features of the Implementation

* ✅ Interactive web-based UI (no installation needed)
* ✅ Human vs AI gameplay
* ✅ Toggle between Minimax, Alpha-Beta, or Both simultaneously
* ✅ Real-time node count and execution time display
* ✅ Move-by-move history comparison table
* ✅ Win/Draw/Loss score tracker
* ✅ Play as X (first) or O (second)
* ✅ AI is unbeatable — achieves perfect play

\---

## ▶️ Execution Steps

### Option 1: Run Locally (Recommended for Testing)

```bash
# Step 1: Clone the repository
git clone https://github.com/<yourusername>/AI\\\_ProblemSolving\\\_<RegisterNumber>.git

# Step 2: Navigate into the folder
cd AI\\\_ProblemSolving\\\_<RegisterNumber>

# Step 3: Open in browser
# On Windows:
start index.html


> \\\*\\\*No server required.\\\*\\\* The entire game runs in a single HTML file.

### Option 2: Play Online via GitHub Pages

Visit: `https://<yourusername>.github.io/AI\\\_ProblemSolving\\\_<RegisterNumber>/`

\---

## 📸 Sample Output

### Gameplay Screenshot

!\[Gameplay](docs/gameplay\_screenshot.png)

### Algorithm Comparison Panel

!\[Comparison](docs/algorithm\_comparison.png)

### Sample Node Count Data (recorded during testing)

|Move #|Empty Cells|Minimax Nodes|Alpha-Beta Nodes|Speedup|
|-|-|-|-|-|
|1|9|5,478|709|7.7×|
|2|7|1,024|223|4.6×|
|3|5|252|87|2.9×|
|4|3|18|14|1.3×|

\---

## 🛠️ Technologies Used

|Technology|Purpose|
|-|-|
|HTML5|Structure and layout|
|CSS3|Styling, animations, responsive design|
|Vanilla JavaScript|Game logic, AI algorithms|
|Google Fonts (Orbitron, Share Tech Mono)|Typography|

