import LCD_1in44
import time
import random
import os
from PIL import Image, ImageDraw, ImageFont

# 🎨 Executive Suite Palette
COLOR_BG = (13, 17, 23)          # #0D1117 - Fondo sobrio
COLOR_TEXT = (201, 209, 217)     # #C9D1D9 - Texto general
COLOR_ACCENT = (88, 166, 255)    # #58A6FF - Azul acento
COLOR_GOLD = (255, 215, 0)       # #FFD700 - Detalle premium
COLOR_SUCCESS = (46, 160, 67)    # #2EA043 - Verde confianza


def generar_wallet():
    return f"wallet_{''.join(random.choices('abcdef0123456789', k=6))}"


def draw_tanke_scene(draw, font, width, height, percent, origen, destino, estado, tick):
    draw.rectangle([(0, 0), (width, height)], fill=COLOR_BG)

    top_y = 6
    body_y = 30
    status_y = 62
    footer_y = height - 14

    # Título corporativo
    draw.text((10, top_y), "PRIVATE TRANSFER CHANNEL",
              fill=COLOR_ACCENT, font=font)

    # Wallets
    draw.text((10, body_y), f"Sender:    {origen}", fill=COLOR_TEXT, font=font)
    draw.text((10, body_y + 12),
              f"Recipient: {destino}", fill=COLOR_TEXT, font=font)

    # Progreso
    barra_len = int((percent / 100) * 10)
    barra = '█' * barra_len + ' ' * (10 - barra_len)
    draw.text((10, status_y), f"[{barra}] {percent}%",
              fill=COLOR_SUCCESS, font=font)

    # Estado
    draw.text((10, status_y + 12),
              f"Status: {estado}", fill=COLOR_TEXT, font=font)

    # Referencia
    ref = ''.join(random.choices('ABCDEF0123456789', k=6))
    draw.text((10, status_y + 24),
              f"Transaction Ref: #{ref}", fill=COLOR_ACCENT, font=font)

    # Footer - Hash dinámico
    hash_dynamic = ''.join(random.choices('abcdef0123456789', k=16))
    draw.text((10, footer_y),
              f"Hash: {hash_dynamic}", fill=COLOR_GOLD, font=font)


def main():
    LCD = LCD_1in44.LCD()
    LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT)
    LCD.LCD_Clear()

    width = LCD.width
    height = LCD.height

    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
    if not os.path.exists(font_path):
        print("⚠️ Fuente no encontrada, usando la predeterminada.")
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, 10)

    tick = 0

    while True:
        origen = generar_wallet()
        destino = generar_wallet()

        for percent in range(0, 101, random.choice([3, 4, 5])):
            image = Image.new("RGB", (width, height), COLOR_BG)
            draw = ImageDraw.Draw(image)

            estado = random.choice([
                "Initializing secure channel...",
                "Keys exchanged ✓",
                "Multi-sig in progress...",
                "Settlement in process...",
                "Final verification running...",
            ])

            draw_tanke_scene(draw, font, width, height,
                             percent, origen, destino, estado, tick)

            LCD.LCD_ShowImage(image, 0, 0)
            time.sleep(0.25)
            tick += 1

        time.sleep(2)


if __name__ == '__main__':
    main()
