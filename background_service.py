import time
import traceback
from jnius import autoclass


TOTAL = 0
CICLO = 0


def actualizar_notificacion(texto):
    try:
        PythonService = autoclass(
            "org.kivy.android.PythonService"
        )

        servicio = PythonService.mService

        if servicio:
            servicio.updateNotification(texto)

    except Exception as e:
        print(
            "[NOTIFICACION ERROR]",
            e,
            flush=True
        )


def ejecutar_trabajo():

    global TOTAL
    global CICLO

    CICLO += 1

    # Trabajo de prueba
    suma = sum(range(1, 101))

    TOTAL += suma


    mensaje = (
        f"Ciclo: {CICLO} | "
        f"Suma: {suma} | "
        f"Total: {TOTAL}"
    )


    print(
        "[SERVICE]",
        mensaje,
        flush=True
    )


    actualizar_notificacion(
        mensaje
    )


print(
    "[SERVICE] Servicio iniciado",
    flush=True
)


while True:

    try:
        ejecutar_trabajo()

    except Exception:
        traceback.print_exc()


    time.sleep(5)
