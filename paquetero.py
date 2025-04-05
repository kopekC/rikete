import LCD_1in44
import time
import random
import os
from PIL import Image, ImageDraw, ImageFont

# 🎨 Paleta CYBERPUNK LATINO PAPI
COLOR_FUCSIA = (255, 0, 255)
COLOR_VERDE_FOSFO = (57, 255, 20)
COLOR_CIAN = (0, 255, 255)
COLOR_AMARILLO = (255, 255, 0)


def get_crypto_file():
    name = ''.join(random.choices('abcdef0123456789', k=8))
    return f"0x{name[:4]}...{name[4:]}"


def draw_transfer_scene(draw, font, width, height, percent, source, estado, tick):
    draw.rectangle([(0, 0), (width, height)], fill="black")

    # Posiciones base
    left_x = 5
    right_x = width - 100
    top_y = 0
    arrow_y = 40
    status_y = 70
    blob_y = height - 18

    # Carpeta origen
    draw.text((left_x, top_y), "+------------+", fill=COLOR_CIAN, font=font)
    draw.text((left_x, top_y + 12),
              f"| {source} |", fill=COLOR_FUCSIA, font=font)
    draw.text((left_x, top_y + 24), "+------------+",
              fill=COLOR_CIAN, font=font)

    # Carpeta destino
    draw.text((right_x, top_y), "+----------------+",
              fill=COLOR_CIAN, font=font)
    draw.text((right_x, top_y + 12), "| cartera_fría.dat |",
              fill=COLOR_FUCSIA, font=font)
    draw.text((right_x, top_y + 24), "+----------------+",
              fill=COLOR_CIAN, font=font)

    # Flechas animadas
    flechas = ">" * ((tick % 8) + 5)
    draw.text((width // 2 - 20, arrow_y), flechas,
              fill=COLOR_VERDE_FOSFO, font=font)
    draw.text((width // 2 - 40, arrow_y + 12),
              " TRANSFIRIENDO ", fill=COLOR_FUCSIA, font=font)

    # Barra de progreso
    progreso = int((percent / 100) * 10)
    barra = '█' * progreso + '░' * (10 - progreso)
    draw.text((10, status_y), f"[{barra}] {percent}%",
              fill=COLOR_VERDE_FOSFO, font=font)
    draw.text((10, status_y + 12),
              f"Estado: {estado}", fill=COLOR_FUCSIA, font=font)

    hash_display = ':'.join(random.choices('ABCDEF0123456789', k=8))
    draw.text((10, status_y + 24),
              f"Hash: {hash_display}", fill=COLOR_VERDE_FOSFO, font=font)

    # Animación ASCII inferior
    animaciones = [
        "   ▓▓▓▓▓▓▓▓▓▓   ",
        " ▓▓  moviendo ▓▓ ",
        "   ▓▓▓▓▓▓▓▓▓▓   ",
        "   ░░░░░░░░░░   ",
        " ░░ cifrando ░░ ",
        "   ░░░░░░░░░░   ",
    ]
    frame = animaciones[(tick // 2) % len(animaciones)]
    draw.text((width // 2 - 45, blob_y), frame, fill=COLOR_AMARILLO, font=font)


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
        source = get_crypto_file()
        for percent in range(0, 101, random.choice([2, 3, 4])):
            image = Image.new("RGB", (width, height), "black")
            draw = ImageDraw.Draw(image)

            estado = random.choice([
                "Enrutando...", "Firma válida ✓", "Cifrando...",
                "Validado", "Subiendo..."
            ])
            draw_transfer_scene(draw, font, width, height,
                                percent, source, estado, tick)

            LCD.LCD_ShowImage(image, 0, 0)
            time.sleep(0.25)
            tick += 1

        time.sleep(1.5)


if __name__ == '__main__':
    main()
