"""
Labirent üreticisi — Yinelemeli Geri İzleme (Recursive Backtracking)

Mükemmel labirent üretir: döngüsüz, herhangi iki hücre arasında
tek bir yol bulunur.

Kullanım:
  python generate_maze.py --size 41 --output test_mazes/labirent.png
"""

import argparse
import numpy as np
from PIL import Image


def generate_maze(N: int, seed: int = 42) -> np.ndarray:
    """N×N mükemmel labirent üretir. 0=yol, 1=duvar."""
    np.random.seed(seed)
    maze = np.ones((N, N), dtype=np.int8)
    visited = np.zeros((N, N), dtype=bool)

    # Yinelemeli Geri İzleme (stack tabanlı)
    stack = [(1, 1)]
    maze[1][1] = 0
    visited[1][1] = True
    dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        r, c = stack[-1]
        candidates = [
            (dr, dc) for dr, dc in dirs
            if 0 < r + dr < N - 1 and 0 < c + dc < N - 1
            and not visited[r + dr][c + dc]
        ]
        if not candidates:
            stack.pop()
            continue
        dr, dc = candidates[np.random.randint(len(candidates))]
        maze[r + dr // 2][c + dc // 2] = 0
        maze[r + dr][c + dc] = 0
        visited[r + dr][c + dc] = True
        stack.append((r + dr, c + dc))

    return maze


def maze_to_image(maze: np.ndarray, cell_size: int = 15) -> Image.Image:
    """Labirent matrisini renk kodlamalı PNG görüntüsüne çevirir."""
    N = maze.shape[0]
    h = N * cell_size
    img_arr = np.zeros((h, h, 3), dtype=np.uint8)

    for r in range(N):
        for c in range(N):
            color = [255, 255, 255] if maze[r][c] == 0 else [0, 0, 0]
            img_arr[r*cell_size:(r+1)*cell_size,
                    c*cell_size:(c+1)*cell_size] = color

    # Başlangıç: kırmızı (1,1)
    img_arr[1*cell_size:(2)*cell_size, 1*cell_size:(2)*cell_size] = [255, 0, 0]
    # Bitiş: yeşil (N-2, N-2)
    img_arr[(N-2)*cell_size:(N-1)*cell_size,
            (N-2)*cell_size:(N-1)*cell_size] = [0, 255, 0]

    return Image.fromarray(img_arr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Labirent Üreticisi")
    parser.add_argument("--size",   type=int, default=41,
                        help="Labirent boyutu (tek sayı olmalı, örn: 41)")
    parser.add_argument("--seed",   type=int, default=42)
    parser.add_argument("--cell",   type=int, default=15,
                        help="Piksel cinsinden hücre boyutu")
    parser.add_argument("--output", type=str, default="test_mazes/labirent.png")
    args = parser.parse_args()

    import os
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    maze = generate_maze(args.size, args.seed)
    img  = maze_to_image(maze, args.cell)
    img.save(args.output)
    print(f"Labirent oluşturuldu: {args.output} ({args.size}×{args.size}, seed={args.seed})")
