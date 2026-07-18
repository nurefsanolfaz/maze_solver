# YAP 441 — Akıllı Labirent Çözücü
**Nurefşan Olfaz**

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

### 1. Test labirenti oluştur
```bash
python generate_maze.py --size 41 --output test_mazes/labirent.png
```

### 2. Labirenti çöz (tüm algoritmalar)
```bash
python main.py test_mazes/labirent.png
```

### 3. Tek algoritma
```bash
python main.py test_mazes/labirent.png --algo bfs
python main.py test_mazes/labirent.png --algo dfs
python main.py test_mazes/labirent.png --algo astar
python main.py test_mazes/labirent.png --algo greedy
```

### 4. Kendi labirentini kullan
PNG veya JPG formatında, şu renk kodlamasına uygun olmalı:
- **Siyah** piksel → Duvar
- **Beyaz** piksel → Geçilebilir yol
- **Kırmızı** piksel → Başlangıç noktası
- **Yeşil** piksel → Bitiş noktası

```bash
python main.py kendi_labirentim.png
```

## Çıktılar

`output/` klasörüne şunlar kaydedilir:
- `solution_bfs.png` — BFS çözüm yolu
- `solution_dfs.png` — DFS çözüm yolu  
- `solution_astar.png` — A* çözüm yolu
- `solution_greedy.png` — Greedy çözüm yolu
- `karsilastirma.png` — 4 algoritma yan yana
- `performans_grafigi.png` — Düğüm sayısı ve süre grafikleri

## Proje Yapısı

```
maze_solver/
├── main.py                   ← Ana çalıştırma
├── generate_maze.py          ← Test labirenti üreticisi
├── requirements.txt
├── algorithms/
│   ├── base_solver.py        ← Ortak soyut sınıf
│   ├── bfs.py                ← Genişlik Öncelikli Arama
│   ├── dfs.py                ← Derinlik Öncelikli Arama
│   ├── astar.py              ← A* (Manhattan sezgiseli)
│   └── greedy.py             ← Greedy Best-First Search
└── utils/
    ├── maze_loader.py        ← PNG/JPG → ızgara dönüştürücü
    └── visualizer.py         ← Görselleştirme ve grafikler
```
