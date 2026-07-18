"""
Harici Labirent Ön-İşleyici (Yarı-Otomatik)

Renkli labirent görsellerini siyah-beyaz formata dönüştürür.
Kullanıcı daha sonra herhangi bir resim editöründe (Paint, Preview vb.)
başlangıç/bitiş noktalarını ve kestirme yolları işaretler.

Adım 1 (Bu script):
  - Tüm duvar renklerini (siyah, kırmızı, koyu renkler) → siyah yapar
  - Tüm yol renklerini (beyaz, cyan, açık renkler) → beyaz yapar
  - İsteğe bağlı boyut indirgeme

Adım 2 (Kullanıcı — resim editöründe):
  - Başlangıç noktasına KIRMIZI piksel/nokta koyar
  - Bitiş noktasına YEŞİL piksel/nokta koyar
  - Kestirme beyaz alanları SİYAH ile boyayarak kapatır
    (dış boşluk, dekoratif beyaz alanlar vb.)

Adım 3 (Çözücü):
  python main.py islenmis_labirent.png

Kullanım:
  python preprocess_external.py <gorsel.png> [cikti.png] [hedef_genislik]

Örnekler:
  python preprocess_external.py queen-1.png                     # varsayılan
  python preprocess_external.py queen-1.png queen_bw.png 800    # 800px genişlik
"""

import sys
import numpy as np
from PIL import Image


def preprocess_to_bw(input_path: str, output_path: str = None,
                     target_width: int = 800):

    if output_path is None:
        output_path = input_path.rsplit(".", 1)[0] + "_bw.png"

    print(f"Yükleniyor: {input_path}")
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    print(f"  Boyut: {w}x{h}")

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # ── Duvar pikselleri ──
    is_black  = (r < 80) & (g < 80) & (b < 80)           # siyah çizgiler
    is_red    = (r > 140) & (g < 100) & (b < 100)         # kırmızı çizgiler
    is_dark   = (r.astype(int) + g.astype(int) + b.astype(int)) < 180  # koyu renkler

    is_wall = is_black | is_red | is_dark

    # ── İkili matris ──
    maze = np.zeros((h, w), dtype=np.uint8)
    maze[is_wall] = 1  # 1=duvar, 0=yol

    # ── Boyut indirgeme ──
    scale = max(1, w // target_width)
    if scale > 1:
        new_h = h // scale
        new_w = w // scale
        trimmed = maze[:new_h * scale, :new_w * scale]
        blocks = trimmed.reshape(new_h, scale, new_w, scale)
        maze_small = (blocks.mean(axis=(1, 3)) > 0.45).astype(np.uint8)
        print(f"  İndirgeme: {scale}x → {new_w}x{new_h}")
    else:
        maze_small = maze
        new_h, new_w = h, w

    # ── Çıktı ──
    out = np.zeros((new_h, new_w, 3), dtype=np.uint8)
    out[maze_small == 0] = [255, 255, 255]
    out[maze_small == 1] = [0, 0, 0]

    Image.fromarray(out).save(output_path)

    print(f"  Kaydedildi: {output_path}")
    print()
    print("=" * 55)
    print("  Sonraki adımlar:")
    print("=" * 55)
    print()
    print(f"  1. '{output_path}' dosyasını bir resim")
    print(f"     editöründe açın (Paint, Preview vb.)")
    print()
    print("  2. Başlangıç noktasına KIRMIZI nokta koyun")
    print("     Bitiş noktasına YEŞİL nokta koyun")
    print()
    print("  3. Algoritmanın kestirmeden gitmemesi için")
    print("     labirent dışındaki beyaz alanları ve")
    print("     dekoratif boşlukları SİYAH ile boyayın")
    print()
    print(f"  4. Kaydedin ve çözücüyü çalıştırın:")
    print(f"     python main.py {output_path}")
    print()

    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    tw  = int(sys.argv[3]) if len(sys.argv) > 3 else 800

    preprocess_to_bw(inp, out, target_width=tw)
