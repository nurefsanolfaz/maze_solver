"""
MazeLoader: PNG/JPG labirent görselini ikili ızgara matrisine dönüştürür.

Renk kodlaması (raporda tanımlandığı gibi):
  Siyah  (RGB: 0,0,0)           → Duvar  (1)
  Beyaz  (RGB: 255,255,255)     → Yol    (0)
  Kırmızı (R>180, G<80, B<80)  → Başlangıç
  Yeşil   (R<80, G>180, B<80)  → Bitiş

Önemli: Kırmızı pikselin gri tonlama değeri ≈ 76 olduğundan
duvar eşiğinin (128) altında kalır. Bu nedenle kırmızı ve yeşil
maskeler eşiklemeden ÖNCE uygulanarak yol (0) olarak işaretlenir.

Hücre-Seviye İndirgeme:
  Görsel labirentlerde her mantıksal hücre birden fazla pikselle
  temsil edilir (örn. cell_size=15 → 15×15 piksel blok). MazeLoader
  bunu otomatik tespit ederek piksel ızgarasını mantıksal hücre
  ızgarasına indirger. Böylece algoritmalar hücre seviyesinde çalışır
  ve raporlanan sonuçlarla tutarlı çıktı üretir.
"""

import numpy as np
from PIL import Image
from typing import List, Tuple


class MazeLoader:
    WALL_THRESHOLD = 128  # Gri tonlama eşiği

    def __init__(self, image_path: str):
        self.image_path = image_path
        self._cell_size = None  # Otomatik tespit edilir

    @property
    def cell_size(self) -> int:
        """Tespit edilen piksel-başına-hücre oranı."""
        return self._cell_size

    def load(self) -> Tuple[List[List[int]], Tuple, Tuple]:
        """
        Görseli yükler, hücre seviyesine indirger ve
        (ızgara, başlangıç, bitiş) döndürür.
        ızgara: 0=yol, 1=duvar
        """
        img = Image.open(self.image_path).convert("RGB")
        arr = np.array(img)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

        # ── 1. Renk maskeleri (orijinal piksel seviyesinde) ──
        red_mask   = (r > 180) & (g < 80) & (b < 80)   # başlangıç
        green_mask = (r < 80)  & (g > 180) & (b < 80)  # bitiş

        # ── 2. Gri tonlama ile eşikleme ──
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        maze = (gray < self.WALL_THRESHOLD).astype(np.int8)

        # Kırmızı ve yeşil pikseller yol olarak işaretlenir
        maze[red_mask]   = 0
        maze[green_mask] = 0

        # ── 3. Hücre boyutu tespiti ve indirgeme ──
        cs = self._detect_cell_size(maze)
        self._cell_size = cs

        if cs > 1:
            maze       = self._downsample_grid(maze, cs)
            red_mask   = self._downsample_mask(red_mask, cs)
            green_mask = self._downsample_mask(green_mask, cs)

        # ── 4. Başlangıç ve bitiş koordinatları ──
        start_pixels = list(zip(*np.where(red_mask)))
        goal_pixels  = list(zip(*np.where(green_mask)))

        if start_pixels:
            start = tuple(map(int, start_pixels[len(start_pixels) // 2]))
        else:
            start = self._find_entry(maze, from_top=True)

        if goal_pixels:
            goal = tuple(map(int, goal_pixels[len(goal_pixels) // 2]))
        else:
            goal = self._find_entry(maze, from_top=False)

        return maze.tolist(), start, goal

    # ────────────────────────────────────────────────────────
    #  Hücre-seviye indirgeme yardımcı metodları
    # ────────────────────────────────────────────────────────

    def _detect_cell_size(self, maze: np.ndarray) -> int:
        """
        Piksel ızgarasındaki hücre boyutunu otomatik tespit eder.

        Yöntem: İlk birkaç satırdaki piksel geçişlerinden (duvar↔yol)
        run-length analizi yapılır. Tüm run uzunluklarının OBEB'i
        (GCD) hücre boyutunu verir. Örneğin cell_size=15 ile üretilmiş
        bir 615×615 görüntüde run uzunlukları 15'in katları olur →
        GCD = 15.
        """
        from math import gcd
        from functools import reduce

        h, w = maze.shape
        if h < 3 or w < 3:
            return 1

        run_lengths = []

        # Yatay run-length analizi (ilk 80 satır yeterli)
        for r in range(min(h, 80)):
            run_start = 0
            for c in range(1, w):
                if maze[r, c] != maze[r, c - 1]:
                    run_lengths.append(c - run_start)
                    run_start = c
            run_lengths.append(w - run_start)

        if not run_lengths:
            return 1

        cs = reduce(gcd, run_lengths)

        # Doğrulama: boyutlar eşit bölünmeli ve anlamlı olmalı
        if cs > 1 and h % cs == 0 and w % cs == 0:
            return cs

        # Fallback: GCD başarısız → en sık tekrar eden run uzunluğunu dene
        from collections import Counter
        counts = Counter(rl for rl in run_lengths if rl > 1)
        for candidate, _ in counts.most_common():
            if h % candidate == 0 and w % candidate == 0:
                return candidate

        return 1

    def _downsample_grid(self, maze: np.ndarray, cs: int) -> np.ndarray:
        """
        Piksel ızgarasını hücre ızgarasına indirger.
        Her cs×cs blokun merkezindeki pikseli örnekler.
        """
        h, w = maze.shape
        rows, cols = h // cs, w // cs
        half = cs // 2
        return maze[half::cs, half::cs][:rows, :cols].copy()

    def _downsample_mask(self, mask: np.ndarray, cs: int) -> np.ndarray:
        """
        Boolean maskeyi hücre seviyesine indirger.
        Blok içinde herhangi bir True piksel varsa hücre True olur.
        """
        h, w = mask.shape
        rows, cols = h // cs, w // cs
        trimmed = mask[:rows * cs, :cols * cs]
        return trimmed.reshape(rows, cs, cols, cs).any(axis=(1, 3))

    def _find_entry(self, maze: np.ndarray, from_top: bool) -> Tuple:
        """Kırmızı/yeşil piksel yoksa ilk geçilebilir hücreyi döndürür."""
        h, w = maze.shape
        rows = range(h) if from_top else range(h - 1, -1, -1)
        for row in rows:
            for col in range(w):
                if maze[row][col] == 0:
                    return (int(row), int(col))
        return (0, 0) if from_top else (h - 1, w - 1)
