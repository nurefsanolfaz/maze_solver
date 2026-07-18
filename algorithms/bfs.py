"""
Genişlik Öncelikli Arama (BFS)

Özellikler:
- FIFO kuyruğu kullanır
- Eşit maliyetli adımlarda optimal yolu garanti eder
- Zaman ve bellek karmaşıklığı: O(b^d)
"""

from collections import deque
from typing import List, Tuple, Optional
from algorithms.base_solver import BaseSolver


class BFS(BaseSolver):

    def _search(self) -> Tuple[Optional[List[Tuple]], int]:
        queue = deque([self.start])
        came_from = {self.start: None}
        visited_order = []
        visited_count = 0

        while queue:
            current = queue.popleft()
            visited_count += 1
            visited_order.append(current)

            if current == self.goal:
                self._visited_cells = set(came_from.keys())
                self._visited_order = visited_order
                return self.reconstruct_path(came_from, current), visited_count

            for neighbor in self.neighbors(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        self._visited_cells = set(came_from.keys())
        self._visited_order = visited_order
        return None, visited_count
