"""
YAP 441 — Akıllı Labirent Çözücü
Nurefşan Olfaz — 211301008

Kullanım:
  python main.py <labirent.png>              # tüm algoritmalar
  python main.py <labirent.png> --algo bfs  # tek algoritma
  python main.py <labirent.png> --no-save   # görsel kaydetme
"""

import sys
import argparse

from utils.maze_loader import MazeLoader
from utils.visualizer import Visualizer
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.astar import AStar
from algorithms.greedy import GreedyBestFirst


ALGORITHMS = {
    "bfs":    ("BFS (Genişlik Öncelikli)",   BFS),
    "dfs":    ("DFS (Derinlik Öncelikli)",   DFS),
    "astar":  ("A* (Manhattan Sezgiseli)",   AStar),
    "greedy": ("Greedy Best-First Search",   GreedyBestFirst),
}


def run(name, cls, maze, start, goal):
    print(f"\n{'─'*48}")
    print(f"  {name}")
    print(f"{'─'*48}")
    solver = cls(maze, start, goal)
    path, stats = solver.solve()
    if path:
        print(f"  ✓ Çözüm bulundu")
        print(f"  • Yol uzunluğu  : {stats['path_length']} adım")
        print(f"  • Ziyaret edilen: {stats['visited_count']} düğüm")
        print(f"  • Süre          : {stats['time_ms']:.3f} ms")
    else:
        print(f"  ✗ Çözüm bulunamadı")
    return path, stats


def main():
    parser = argparse.ArgumentParser(description="Akıllı Labirent Çözücü")
    parser.add_argument("image", help="Labirent görseli (PNG veya JPG)")
    parser.add_argument("--algo",
                        choices=list(ALGORITHMS.keys()) + ["all"],
                        default="all")
    parser.add_argument("--output",  default="output")
    parser.add_argument("--no-save", action="store_true")
    args = parser.parse_args()

    # Labirenti yükle
    print(f"\nLabirent yükleniyor: {args.image}")
    loader = MazeLoader(args.image)
    maze, start, goal = loader.load()
    print(f"  Boyut     : {len(maze)}×{len(maze[0])} hücre")
    print(f"  Başlangıç : {start}")
    print(f"  Bitiş     : {goal}")

    # Algoritmalar
    selected = ALGORITHMS.keys() if args.algo == "all" else [args.algo]
    results = {}

    for key in selected:
        name, cls = ALGORITHMS[key]
        path, stats = run(name, cls, maze, start, goal)
        results[key] = (name, path, stats)

    # Görselleştir
    if not args.no_save:
        viz = Visualizer(maze, start, goal, args.output)
        for key, (name, path, stats) in results.items():
            if path:
                viz.save_solution(path, stats, key, name)
        viz.save_comparison(results)
        print(f"\nGörseller '{args.output}/' klasörüne kaydedildi.")

    # Özet tablo
    print(f"\n{'='*56}")
    print(f"  {'KARŞILAŞTIRMA TABLOSU':^52}")
    print(f"{'='*56}")
    print(f"  {'Algoritma':<26} {'Yol':>6} {'Ziyaret':>9} {'Süre(ms)':>10}")
    print(f"  {'─'*52}")
    for key, (name, path, stats) in results.items():
        if path:
            print(f"  {name:<26} {stats['path_length']:>6} "
                  f"{stats['visited_count']:>9} {stats['time_ms']:>10.3f}")
        else:
            print(f"  {name:<26} {'YOK':>6} {stats['visited_count']:>9} "
                  f"{stats['time_ms']:>10.3f}")
    print()


if __name__ == "__main__":
    main()
