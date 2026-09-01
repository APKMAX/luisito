import time
import os
from jnius import autoclass


contador = 0
total = 0


def guardar_info(texto):

    try:

        activity = autoclass(
            "org.kivy.android.PythonActivity"
        ).mActivity


        carpeta = activity.getFilesDir().getAbsolutePath()


        archivo = os.path.join(
            carpeta,
            "Info.txt"
        )


        with open(archivo, "w") as f:
            f.write(texto)


    except Exception as e:

        print(
            "Error guardando archivo:",
            e
        )


while True:

    try:

        global contador
        global total


        contador += 1


        suma = sum(range(1, 101))


        total += suma


        variable_info = (
            f"Ciclo: {contador}\n"
            f"Suma realizada: {suma}\n"
            f"Total acumulado: {total}\n"
        )


        guardar_info(
            variable_info
        )


    except Exception as e:

        print(
            "Error servicio:",
            e
        )


    time.sleep(5)
