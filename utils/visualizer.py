"""
Visualizer: Çözüm yolunu görselleştirir ve karşılaştırma grafikleri üretir.

Raporda belirtilen renkler:
  Mavi   → Ziyaret edilen düğümler (frontier)
  Yeşil  → Çözüm yolu
  Kırmızı → Başlangıç
  Sarı   → Bitiş
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Tuple, Dict, Any, Optional


class Visualizer:
    # Renk paleti
    COLOR_WALL     = [30,  30,  30]
    COLOR_PATH     = [245, 245, 245]
    COLOR_VISITED  = [100, 149, 237]   # mavi — ziyaret edilen
    COLOR_SOLUTION = [50,  180,  80]   # yeşil — çözüm yolu
    COLOR_START    = [220,  60,  60]   # kırmızı — başlangıç
    COLOR_GOAL     = [255, 200,   0]   # sarı — bitiş

    def __init__(self, maze: List[List[int]], start: Tuple, goal: Tuple,
                 output_dir: str = "output"):
        self.maze = np.array(maze)
        self.start = start
        self.goal = goal
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.h, self.w = self.maze.shape

    def _base_image(self) -> np.ndarray:
        img = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        img[self.maze == 1] = self.COLOR_WALL
        img[self.maze == 0] = self.COLOR_PATH
        return img

    def save_solution(self, path: List[Tuple], stats: Dict[str, Any],
                      algo_key: str, algo_name: str):
        """Tek algoritma için çözüm görselini kaydeder."""
        img = self._base_image()

        # Çözüm yolunu çiz
        for r, c in path:
            img[r, c] = self.COLOR_SOLUTION
        img[self.start] = self.COLOR_START
        img[self.goal]  = self.COLOR_GOAL

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img, interpolation="nearest")
        ax.set_title(
            f"{algo_name}\n"
            f"Yol: {stats['path_length']} adım  |  "
            f"Ziyaret: {stats['visited_count']} düğüm  |  "
            f"Süre: {stats['time_ms']:.2f} ms",
            fontsize=12, pad=10
        )
        ax.axis("off")

        patches = [
            mpatches.Patch(color=np.array(self.COLOR_START)/255,    label="Başlangıç"),
            mpatches.Patch(color=np.array(self.COLOR_GOAL)/255,     label="Bitiş"),
            mpatches.Patch(color=np.array(self.COLOR_SOLUTION)/255, label="Çözüm Yolu"),
        ]
        ax.legend(handles=patches, loc="upper right", fontsize=9)

        out_path = os.path.join(self.output_dir, f"solution_{algo_key}.png")
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Kaydedildi: {out_path}")

    def save_comparison(self, results: Dict[str, Any]):
        """4 algoritmayı yan yana gösteren karşılaştırma paneli üretir."""
        entries = [(k, n, p, s) for k, (n, p, s) in results.items() if p]
        if not entries:
            return

        n_algo = len(entries)
        fig, axes = plt.subplots(1, n_algo, figsize=(5 * n_algo, 6))
        if n_algo == 1:
            axes = [axes]

        fig.suptitle("Algoritma Karşılaştırması", fontsize=14,
                     fontweight="bold", y=1.01)

        for ax, (key, name, path, stats) in zip(axes, entries):
            img = self._base_image()
            for r, c in path:
                img[r, c] = self.COLOR_SOLUTION
            img[self.start] = self.COLOR_START
            img[self.goal]  = self.COLOR_GOAL

            ax.imshow(img, interpolation="nearest")
            ax.set_title(
                f"{name}\n"
                f"{stats['path_length']} adım\n"
                f"{stats['visited_count']} düğüm\n"
                f"{stats['time_ms']:.1f} ms",
                fontsize=9
            )
            ax.axis("off")

        out_path = os.path.join(self.output_dir, "karsilastirma.png")
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Karşılaştırma: {out_path}")

        self._save_bar_chart(entries)

    def _save_bar_chart(self, entries):
        """Performans çubuğu grafiği üretir."""
        names     = [n.split("(")[0].strip() for _, n, _, _ in entries]
        visits    = [s["visited_count"] for _, _, _, s in entries]
        times     = [s["time_ms"]       for _, _, _, s in entries]

        colors = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63"]
        x = np.arange(len(names))

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        fig.suptitle("Performans Metrikleri", fontsize=12, fontweight="bold")

        for ax, data, title, ylabel in zip(
            axes,
            [visits, times],
            ["Ziyaret Edilen Düğüm Sayısı", "Çalışma Süresi (ms)"],
            ["Düğüm", "ms"]
        ):
            bars = ax.bar(x, data, color=colors[:len(names)],
                          edgecolor="white", linewidth=0.8)
            ax.set_xticks(x)
            ax.set_xticklabels(names, fontsize=9)
            ax.set_title(title, fontsize=10)
            ax.set_ylabel(ylabel)
            ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
            ax.spines[["top", "right"]].set_visible(False)

        out_path = os.path.join(self.output_dir, "performans_grafigi.png")
        fig.tight_layout()
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Grafik: {out_path}")
