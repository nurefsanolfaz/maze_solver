"""
YAP 441 — Akıllı Labirent Çözücü  Web Sunucusu
Nurefşan Olfaz — 211301008

Kullanım:
  python app.py
  Tarayıcıda: http://localhost:5050
"""

import os
import random
import tempfile
from flask import Flask, request, jsonify, send_from_directory

from generate_maze import generate_maze
from utils.maze_loader import MazeLoader
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.astar import AStar
from algorithms.greedy import GreedyBestFirst

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

ALGORITHMS = {
    "bfs":    BFS,
    "dfs":    DFS,
    "astar":  AStar,
    "greedy": GreedyBestFirst,
}


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "maze_ui.html")


@app.route("/test_mazes/<path:filename>")
def serve_test_maze(filename):
    return send_from_directory(os.path.join(BASE_DIR, "test_mazes"), filename)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """Python backend ile labirent üret, JSON grid döndür."""
    data = request.get_json(silent=True) or {}
    size = int(data.get("size", 41))
    if size % 2 == 0:
        size += 1          # Boyut tek sayı olmalı
    size = max(11, min(size, 151))

    seed = data.get("seed", random.randint(0, 9999))
    maze = generate_maze(size, seed=seed)

    return jsonify({
        "grid": maze.tolist(),
        "rows": size,
        "cols": size,
        "seed": seed,
        "start": [1, 1],
        "goal":  [size - 2, size - 2],
    })


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """PNG/JPG labirent görseli yükle, hücre ızgarasına dönüştür."""
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "Görsel dosyası bulunamadı"}), 400

    # Geçici dosyaya kaydet, MazeLoader ile işle
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
        file.save(tmp_path)

    try:
        loader = MazeLoader(tmp_path)
        maze_grid, start, goal = loader.load()
    finally:
        os.unlink(tmp_path)

    rows = len(maze_grid)
    cols = len(maze_grid[0])

    return jsonify({
        "grid":      maze_grid,
        "rows":      rows,
        "cols":      cols,
        "start":     list(start),
        "goal":      list(goal),
        "cell_size": loader.cell_size,
    })


@app.route("/api/solve", methods=["POST"])
def api_solve():
    """Python algoritmasıyla labirenti çöz, yol + istatistik döndür."""
    data = request.get_json()
    grid   = data["grid"]
    algo   = data.get("algo", "bfs")
    start  = tuple(data.get("start", [1, 1]))
    goal   = tuple(data.get("goal",  [len(grid) - 2, len(grid[0]) - 2]))

    cls = ALGORITHMS.get(algo)
    if cls is None:
        return jsonify({"error": f"Bilinmeyen algoritma: {algo}"}), 400

    solver = cls(grid, start, goal)
    path, stats = solver.solve()

    visited_order = [list(p) for p in stats.get("visited_order", [])]

    return jsonify({
        "path":          [list(p) for p in path] if path else None,
        "path_length":   stats["path_length"],
        "visited_count": stats["visited_count"],
        "visited_order": visited_order,
        "time_ms":       round(stats["time_ms"], 3),
    })


@app.route("/api/save_screenshot", methods=["POST"])
def save_screenshot():
    """Canvas ekran görüntüsünü dosyaya kaydet."""
    import base64
    data = request.get_json()
    img_data = data["image"].split(",")[1]
    with open(os.path.join(BASE_DIR, "output", "ui_screenshot.png"), "wb") as f:
        f.write(base64.b64decode(img_data))
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("\n  Labirent Çözücü başlatılıyor...")
    print("  Tarayıcıda aç: http://localhost:5050\n")
    app.run(debug=True, port=5050)
