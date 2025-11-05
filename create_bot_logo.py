"""
Bot Logo Oluşturucu
Profesyonel futbol tahmin botu logosu
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_bot_logo():
    """512x512 profesyonel bot logosu oluştur"""
    
    # Görsel boyutu
    size = 512
    img = Image.new('RGB', (size, size), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Merkez noktası
    center = size // 2
    
    # 1. Arka plan gradient (koyu mavi -> yeşil)
    for y in range(size):
        # Gradient renk hesaplama
        ratio = y / size
        r = int(26 + (46 - 26) * ratio)
        g = int(26 + (204 - 26) * ratio)
        b = int(46 + (113 - 46) * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # 2. Dış çember (altın)
    outer_radius = 200
    draw.ellipse(
        [center - outer_radius, center - outer_radius,
         center + outer_radius, center + outer_radius],
        outline='#F39C12',
        width=8
    )
    
    # 3. İç çember (yeşil parlak)
    inner_radius = 170
    draw.ellipse(
        [center - inner_radius, center - inner_radius,
         center + inner_radius, center + inner_radius],
        fill='#27AE60',
        outline='#2ECC71',
        width=4
    )
    
    # 4. Futbol topu deseni (beyaz altıgen)
    hexagon_radius = 140
    for i in range(6):
        angle1 = math.radians(60 * i - 30)
        angle2 = math.radians(60 * (i + 1) - 30)
        
        x1 = center + hexagon_radius * math.cos(angle1)
        y1 = center + hexagon_radius * math.sin(angle1)
        x2 = center + hexagon_radius * math.cos(angle2)
        y2 = center + hexagon_radius * math.sin(angle2)
        
        draw.line([(x1, y1), (x2, y2)], fill='#ECF0F1', width=6)
    
    # 5. Merkez beşgen (koyu)
    pentagon_radius = 50
    pentagon_points = []
    for i in range(5):
        angle = math.radians(72 * i - 90)
        x = center + pentagon_radius * math.cos(angle)
        y = center + pentagon_radius * math.sin(angle)
        pentagon_points.append((x, y))
    
    draw.polygon(pentagon_points, fill='#2C3E50', outline='#34495E', width=3)
    
    # 6. AI sinir ağı çizgileri (mavi parlak)
    for i in range(8):
        angle = math.radians(45 * i)
        x1 = center + 60 * math.cos(angle)
        y1 = center + 60 * math.sin(angle)
        x2 = center + 160 * math.cos(angle)
        y2 = center + 160 * math.sin(angle)
        
        # Gradient çizgi efekti
        draw.line([(x1, y1), (x2, y2)], fill='#3498DB', width=2)
        
        # Nokta (node)
        node_radius = 6
        draw.ellipse(
            [x2 - node_radius, y2 - node_radius,
             x2 + node_radius, y2 + node_radius],
            fill='#5DADE2',
            outline='#85C1E9',
            width=2
        )
    
    # 7. İstatistik grafik simgesi (sağ alt köşe)
    graph_x = size - 100
    graph_y = size - 100
    
    # Bar chart
    bars = [
        (graph_x - 30, graph_y - 20, graph_x - 20, graph_y),
        (graph_x - 15, graph_y - 35, graph_x - 5, graph_y),
        (graph_x, graph_y - 25, graph_x + 10, graph_y),
        (graph_x + 15, graph_y - 40, graph_x + 25, graph_y)
    ]
    
    for bar in bars:
        draw.rectangle(bar, fill='#F39C12', outline='#F4D03F', width=1)
    
    # 8. "AI" text (üst kısım)
    try:
        # Font yoksa devam et
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # AI yazısı
    ai_text = "AI"
    bbox = draw.textbbox((0, 0), ai_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center - text_width // 2
    text_y = 40
    
    # Gölge efekti
    draw.text((text_x + 2, text_y + 2), ai_text, fill='#000000', font=font_large)
    draw.text((text_x, text_y), ai_text, fill='#ECF0F1', font=font_large)
    
    # "PREDICT" yazısı (alt kısım)
    predict_text = "PREDICT"
    bbox = draw.textbbox((0, 0), predict_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    
    text_x = center - text_width // 2
    text_y = size - 60
    
    # Gölge efekti
    draw.text((text_x + 1, text_y + 1), predict_text, fill='#000000', font=font_small)
    draw.text((text_x, text_y), predict_text, fill='#F39C12', font=font_small)
    
    # 9. Parlama efekti (sol üst)
    for i in range(5):
        shine_radius = 15 - i * 3
        opacity = 255 - i * 50
        shine_color = (255, 255, 255, opacity)
        
        # PIL doesn't support alpha in RGB mode, so we skip alpha
        draw.ellipse(
            [100 - shine_radius, 100 - shine_radius,
             100 + shine_radius, 100 + shine_radius],
            fill=(255, 255, 255)
        )
    
    # Kaydet
    output_path = 'bot_logo.png'
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Logo oluşturuldu: {output_path}")
    print(f"📐 Boyut: {size}x{size} px")
    print(f"📁 Format: PNG")
    print(f"\n🎯 Şimdi yapmanız gerekenler:")
    print(f"1. Telegram'da @BotFather'ı aç")
    print(f"2. /setuserpic komutunu yaz")
    print(f"3. Botunu seç")
    print(f"4. '{output_path}' dosyasını yükle")
    
    return output_path

if __name__ == "__main__":
    print("🎨 Bot logosu oluşturuluyor...\n")
    create_bot_logo()
