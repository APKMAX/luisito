import time
import traceback


TOTAL = 0


def ejecutar_trabajo():
    global TOTAL

    TOTAL += sum(range(1, 101))

    print(f"[SERVICE] Total acumulado: {TOTAL}", flush=True)


print("[SERVICE] Servicio iniciado", flush=True)

while True:
    try:
        ejecutar_trabajo()

    except Exception:
        traceback.print_exc()

    time.sleep(30)