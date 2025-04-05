import LCD_1in44
import time
import random
import os
from PIL import Image, ImageDraw, ImageFont

# 🎨 Paleta CALLEJERA BOLITERO CUBANO
COLOR_NARANJA_CALLE = (255, 140, 0)
COLOR_ROJO_SUERTE = (255, 50, 50)
COLOR_VERDE_BILLETE = (0, 255, 100)
COLOR_AZUL_RADIO = (50, 150, 255)


def get_crypto_file():
    num = ''.join(random.choices('0123456789', k=3))
    return f"jugada_{num}.dat"


def draw_transfer_scene(draw, font, width, height, percent, source, estado, tick):
    draw.rectangle([(0, 0), (width, height)], fill="black")

    # Posiciones base
    top_y = 0
    arrow_y = 30
    status_y = 65
    blob_y = height - 18

    # Jugada origen y destino simplificados
    draw.text((10, top_y), f"📤 Jugada: {source}",
              fill=COLOR_VERDE_BILLETE, font=font)
    draw.text((10, top_y + 12), f"📥 Destino: banca_oculta.blt",
              fill=COLOR_AZUL_RADIO, font=font)

    # Flechas animadas
    flechas = ">" * ((tick % 8) + 5)
    draw.text((width // 2 - 20, arrow_y), flechas,
              fill=COLOR_VERDE_BILLETE, font=font)
    draw.text((width // 2 - 60, arrow_y + 12), " PASANDO LA JUGADA ",
              fill=COLOR_ROJO_SUERTE, font=font)

    # Barra de progreso
    progreso = int((percent / 100) * 10)
    barra = '▓' * progreso + '░' * (10 - progreso)
    draw.text((10, status_y), f"[{barra}] {percent}%",
              fill=COLOR_VERDE_BILLETE, font=font)
    draw.text((10, status_y + 12),
              f"Estado: {estado}", fill=COLOR_NARANJA_CALLE, font=font)

    numeros = '-'.join(random.choices(['01', '12', '23',
                       '34', '45', '56', '67', '78', '89', '90'], k=3))
    draw.text((10, status_y + 24),
              f"Números: {numeros}", fill=COLOR_ROJO_SUERTE, font=font)

    # Animación ASCII inferior estilo bolita
    animaciones = [
        "  🎲 Tirando los dados... ",
        "  💸 Contando billete... ",
        "  🔐 Sellando jugada...  ",
        "  🎯 Números en el aire  ",
        "  🔄 Repartiendo suerte  ",
    ]
    frame = animaciones[(tick // 2) % len(animaciones)]
    draw.text((width // 2 - 55, blob_y), frame,
              fill=COLOR_NARANJA_CALLE, font=font)


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
                "Autenticando jugada...", "Firma lista ✓", "Cerrando la caja...",
                "Validado", "Marcando número..."
            ])
            draw_transfer_scene(draw, font, width, height,
                                percent, source, estado, tick)

            LCD.LCD_ShowImage(image, 0, 0)
            time.sleep(0.25)
            tick += 1

        time.sleep(1.5)


if __name__ == '__main__':
    main()
