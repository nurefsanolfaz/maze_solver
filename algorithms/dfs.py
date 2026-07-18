"""
Derinlik Öncelikli Arama (DFS)

Özellikler:
- LIFO yığını kullanır (yinelemeli uygulama)
- Python özyineleme sınırını aşmamak için yığın tabanlı uygulandı
- Bellek karmaşıklığı: O(b*m) — BFS'ten belirgin biçimde düşük
- Mükemmel labirentte tek yol olduğundan optimal yolu bulur;
  döngülü labirentlerde optimal olmayan yollar üretebilir
"""

from typing import List, Tuple, Optional
from algorithms.base_solver import BaseSolver


class DFS(BaseSolver):

    def _search(self) -> Tuple[Optional[List[Tuple]], int]:
        stack = [self.start]
        came_from = {self.start: None}
        visited = set()
        visited_order = []
        visited_count = 0

        while stack:
            current = stack.pop()

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
                    stack.append(neighbor)

        self._visited_cells = visited
        self._visited_order = visited_order
        return None, visited_count
