"""
BaseSolver: Tüm arama algoritmalarının türediği soyut temel sınıf.

Raporda belirtilen mimari:
- Dört yönlü komşu üretme fonksiyonu
- came_from sözlüğüyle yol yeniden yapılandırma
- Zamanlama sarmalayıcısı
"""

import time
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any


class BaseSolver(ABC):
    # Dört yönlü hareket: Yukarı, Aşağı, Sol, Sağ
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, maze: List[List[int]], start: Tuple, goal: Tuple):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = start
        self.goal = goal
        self._visited_cells = set()    # Ziyaret edilen hücreler (küme)
        self._visited_order = []       # Ziyaret sırası (liste)

    def is_valid(self, r: int, c: int) -> bool:
        """Hücrenin geçerli ve geçilebilir olup olmadığını kontrol eder."""
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.maze[r][c] == 0)

    def neighbors(self, r: int, c: int):
        """Dört yönlü geçilebilir komşuları döndürür."""
        for dr, dc in self.DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                yield (nr, nc)

    def reconstruct_path(self, came_from: Dict, goal: Tuple) -> List[Tuple]:
        """came_from sözlüğünden yolu geri izleyerek yeniden yapılandırır."""
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        return path

    @abstractmethod
    def _search(self) -> Tuple[Optional[List[Tuple]], int]:
        """(yol, ziyaret_sayısı) döndürür. Yol bulunamazsa None."""
        pass

    def solve(self) -> Tuple[Optional[List[Tuple]], Dict[str, Any]]:
        """Algoritmayı çalıştırır, yolu ve performans istatistiklerini döndürür."""
        t0 = time.perf_counter()
        path, visited_count = self._search()
        elapsed_ms = (time.perf_counter() - t0) * 1000

        stats = {
            "path_length": len(path) - 1 if path else 0,
            "visited_count": visited_count,
            "visited_cells": self._visited_cells,
            "visited_order": self._visited_order,
            "time_ms": elapsed_ms,
        }
        return path, stats
