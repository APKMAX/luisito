
[app]

title = Lector pago movil
package.name = lectorpagomovil
package.domain = org.ejemplo

source.dir = .
source.include_exts = py

version = 2.1

requirements = python3,kivy,pyjnius

# Servicio correctamente configurado para Android 14+
#services = Counter:./service/main.py:foreground:sticky:foregroundServiceType=specialUse

# Permisos necesarios
#requirements = python3,kivy,pyjnius,android

android.permissions = READ_SMS
orientation = portrait
fullscreen = 0

# Android
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

# Deja esto comentado mientras pruebas (recomendado)
android.release = True
android.release_artifact = apk

# p4a
p4a.branch = master
