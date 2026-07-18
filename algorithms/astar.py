"""
A* Arama Algoritması

Özellikler:
- f(n) = g(n) + h(n) ile sıralanmış minimum-yığın kullanır
- h(n) = |Δr| + |Δc| Manhattan uzaklığı sezgiseli
- Dört bağlantılı ızgarada admissible → hem tam hem optimal
- Zaman ve bellek karmaşıklığı: O(b^d)
"""

import heapq
from typing import List, Tuple, Optional
from algorithms.base_solver import BaseSolver


class AStar(BaseSolver):

    def heuristic(self, r: int, c: int) -> int:
        """Manhattan uzaklığı sezgiseli: h(n) = |Δr| + |Δc|"""
        return abs(r - self.goal[0]) + abs(c - self.goal[1])

    def _search(self) -> Tuple[Optional[List[Tuple]], int]:
        h_start = self.heuristic(*self.start)
        # (f_skoru, g_skoru, düğüm)
        open_heap = [(h_start, 0, self.start)]
        came_from = {self.start: None}
        g_score = {self.start: 0}
        visited = set()
        visited_order = []
        visited_count = 0

        while open_heap:
            f, g, current = heapq.heappop(open_heap)

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
                if neighbor in visited:
                    continue
                tentative_g = g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    came_from[neighbor] = current
                    h = self.heuristic(*neighbor)
                    heapq.heappush(open_heap, (tentative_g + h, tentative_g, neighbor))

        self._visited_cells = visited
        self._visited_order = visited_order
        return None, visited_count
