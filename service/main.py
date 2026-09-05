from time import sleep
from jnius import autoclass
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

# Auto-reinicio si Android mata el servicio
PythonService = autoclass("org.kivy.android.PythonService")
PythonService.mService.setAutoRestartService(True)

# Cliente OSC para enviar datos a la app (puerto 3002)
client = OSCClient("127.0.0.1", 3002)

# Servidor OSC para recibir la orden de parar (puerto 3001)
server = OSCThreadServer()
server.listen(address="127.0.0.1", port=3001, default=True)

running = True

def on_stop(*args):
    global running
    print("Servicio recibió orden de parar")
    running = False

server.bind(b"/stop", on_stop)

contador = 0

print("=== Servicio iniciado ===")

while running:
    contador += 1

    # Enviamos el valor a la app
    try:
        client.send_message(b"/contador", [contador])
    except Exception as e:
        # Si la app está cerrada, simplemente ignoramos el error
        pass

    print(f"Contador = {contador}")  # Visible en logcat
    sleep(1)

print("=== Servicio detenido ===")
server.stop()
server.close()
