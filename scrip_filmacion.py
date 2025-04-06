import random
import time
from datetime import datetime
from collections import deque

CRYPTO = ['MBL']
MAX_LINES = 100  # Máximo número de líneas visibles

log_buffer = deque(maxlen=MAX_LINES)


def generar_wallet():
    return f"0x{''.join(random.choices('abcdef0123456789', k=12))}"


def generar_hash():
    return ''.join(random.choices('abcdef0123456789', k=24))


def generar_monto(cripto):
    if cripto == 'BTC':
        return round(random.uniform(0.001, 1.5), 6)
    elif cripto == 'ETH':
        return round(random.uniform(0.01, 12), 5)
    elif cripto == 'USDT' or cripto == 'DAI':
        return round(random.uniform(10, 10000), 2)
    elif cripto == 'XMR':
        return round(random.uniform(0.5, 30), 4)
    else:
        return round(random.uniform(1, 200), 3)


def generar_linea_tx():
    cripto = random.choice(CRYPTO)
    from_wallet = generar_wallet()
    to_wallet = generar_wallet()
    tx_hash = generar_hash()
    monto = generar_monto(cripto)
    timestamp = datetime.utcnow().strftime("%H:%M:%S")

    linea = f"[{timestamp}] {monto:>9} {cripto}  | {from_wallet} → {to_wallet}  | #{tx_hash}"
    return linea


def print_log():
    print("\033c", end="")  # Limpia pantalla sin parpadear (ANSI clear)
    print("🧾  MONITOR TRANSACCIONES MAMBI LIBRE TIEMPO REAL".center(80))
    print("-" * 80)
    for linea in log_buffer:
        print(linea)
    print("-" * 80)
    print("🔁 Ctrl+C para salir")


def main():
    try:
        while True:
            nueva_linea = generar_linea_tx()
            log_buffer.append(nueva_linea)
            print_log()
            time.sleep(random.uniform(0.04, 0.25))
    except KeyboardInterrupt:
        print("\n🛑 Monitor detenido.")


if __name__ == '__main__':
    main()
