from time import sleep
from jnius import autoclass
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

# ============================================================
# Auto-reinicio si Android mata el servicio
# ============================================================
PythonService = autoclass("org.kivy.android.PythonService")
service = PythonService.mService
service.setAutoRestartService(True)

# ============================================================
# NOTIFICACIÓN FOREGROUND (obligatoria)
# ============================================================
Context = autoclass("android.content.Context")
NotificationBuilder = autoclass("android.app.Notification$Builder")
NotificationChannel = autoclass("android.app.NotificationChannel")
NotificationManager = autoclass("android.app.NotificationManager")
AndroidString = autoclass("java.lang.String")

channel_id = "contador_channel"
channel_name = AndroidString("Servicio Contador")
importance = NotificationManager.IMPORTANCE_LOW  # No suena ni vibra

channel = NotificationChannel(channel_id, channel_name, importance)
notification_service = service.getSystemService(Context.NOTIFICATION_SERVICE)
notification_service.createNotificationChannel(channel)

builder = NotificationBuilder(service, channel_id)
builder.setContentTitle(AndroidString("Contador en segundo plano"))
builder.setContentText(AndroidString("Sumando números..."))
builder.setSmallIcon(service.getApplicationInfo().icon)

# Pone el servicio en foreground (esto es lo que evita que Android lo mate)
service.startForeground(1, builder.build())

# ============================================================
# OSC
# ============================================================
client = OSCClient("127.0.0.1", 3002)

server = OSCThreadServer()
server.listen(address="127.0.0.1", port=3001, default=True)

running = True

def on_stop(*args):
    global running
    print("Servicio recibió orden de parar")
    running = False

server.bind(b"/stop", on_stop)

contador = 0
print("=== Servicio iniciado correctamente ===")

while running:
    contador += 1

    # Actualizar texto de la notificación cada 5 segundos
    if contador % 5 == 0:
        try:
            builder.setContentText(AndroidString(f"Contador: {contador}"))
            service.startForeground(1, builder.build())
        except Exception:
            pass

    # Enviar valor a la app (si está abierta)
    try:
        client.send_message(b"/contador", [contador])
    except Exception:
        pass

    print(f"Contador = {contador}")
    sleep(1)

print("=== Servicio detenido ===")
try:
    server.stop()
    server.close()
except Exception:
    pass
