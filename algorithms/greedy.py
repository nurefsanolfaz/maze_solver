"""
Greedy Best-First Search (GBFS)

Özellikler:
- Yalnızca h(n) sezgiselini kullanır; g(n) göz ardı edilir
- Pratikte A*'tan hızlı olabilir
- Optimallik garantisi vermez (genel durum)
- Performansı sezgisel ile labirent topolojisi arasındaki
  uyuma güçlü biçimde bağımlıdır
"""

import heapq
from typing import List, Tuple, Optional
from algorithms.base_solver import BaseSolver


class GreedyBestFirst(BaseSolver):

    def heuristic(self, r: int, c: int) -> int:
        """Manhattan uzaklığı sezgiseli: h(n) = |Δr| + |Δc|"""
        return abs(r - self.goal[0]) + abs(c - self.goal[1])

    def _search(self) -> Tuple[Optional[List[Tuple]], int]:
        h_start = self.heuristic(*self.start)
        open_heap = [(h_start, self.start)]
        came_from = {self.start: None}
        visited = set()
        visited_order = []
        visited_count = 0

        while open_heap:
            _, current = heapq.heappop(open_heap)

            if current in visited:
                continue
            visited.add(current)
            visited_order.append(current)
            visited_count += 1

            if current == self.goal:
                self._visited_cells = visited
                self._visited_order = visited_order
                return self.reconstruct_path(came_from, current), visited_count

            for neighbor in self.neighbors(*current):
                if neighbor not in visited and neighbor not in came_from:
                    came_from[neighbor] = current
                    h = self.heuristic(*neighbor)
                    heapq.heappush(open_heap, (h, neighbor))

        self._visited_cells = visited
        self._visited_order = visited_order
        return None, visited_count
