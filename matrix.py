import LCD_1in44
import time
import random
from PIL import Image, ImageDraw, ImageFont


def generate_random_line():
    # Simulated cold wallet routing logs / fragments
    crypto_words = [
        "TXID: " + ''.join(random.choices("abcdef1234567890", k=10)),
        "0x" + ''.join(random.choices("abcdef1234567890", k=12)),
        "recv: BTC -> 0.0345",
        "send: ETH -> 1.004",
        "Nonce: " + str(random.randint(1000, 9999)),
        "SIG_OK ✓", "HASH_MISMATCH ✗",
        "P2P_ROUTING...", "Ξ VALID BLOCK",
        "WALLET SYNCED", "ENCRYPTION ACTIVE",
        "IPFS_CHUNK", "LOADER@NODE_4",
        "SYNC_CHAIN", "▲ MEMORY FRAGMENT"
    ]
    return random.choice(crypto_words)


def main():
    LCD = LCD_1in44.LCD()
    print("********** Init LCD **********")
    LCD.LCD_Init(LCD_1in44.SCAN_DIR_DFT)
    LCD.LCD_Clear()

    width = LCD.width
    height = LCD.height
    font = ImageFont.truetype(
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 10)

    cols = width // 8
    rows = height // 12
    trail_length = 6

    # For each column, keep a stream of vertical data positions
    stream_positions = [random.randint(0, rows) for _ in range(cols)]
    trails = [[] for _ in range(cols)]

    while True:
        image = Image.new("RGB", (width, height), "black")
        draw = ImageDraw.Draw(image)

        for col in range(cols):
            x = col * 8
            y = stream_positions[col] * 12

            text = generate_random_line()[:8]  # Trim to width
            trails[col].insert(0, (text, y))

            if len(trails[col]) > trail_length:
                trails[col] = trails[col][:trail_length]

            for i, (trail_text, trail_y) in enumerate(trails[col]):
                green_intensity = 255 - (i * (255 // trail_length))
                color = (0, green_intensity, 0)
                draw.text((x, trail_y), trail_text, font=font, fill=color)

            # Move stream downward
            stream_positions[col] = (stream_positions[col] + 1) % rows

        # Random chance to simulate glitches or new line bursts
        if random.random() < 0.1:
            glitch_col = random.randint(0, cols - 1)
            trails[glitch_col] = []

        LCD.LCD_ShowImage(image, 0, 0)
        time.sleep(0.12)


if __name__ == '__main__':
    main()
