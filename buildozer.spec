[app]

title = Mi Contador Servicio
package.name = micontador
package.domain = org.ejemplo

#package.domain = org.example

source.dir = .
source.include_exts = py

version = 2
requirements = python3,kivy,pyjnius,android,oscpy

# Servicio (igual que antes)
services = Counter:./service/main.py:foreground:sticky

android.permissions = FOREGROUND_SERVICE, POST_NOTIFICATIONS, WAKE_LOCK

#requirements =  python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

#services = backgroundservice:background_service.py:foreground:sticky:foregroundServiceType=specialUse
#android.permissions = android.permission.FOREGROUND_SERVICE,android.permission.FOREGROUND_SERVICE_SPECIAL_USE,android.permission.POST_NOTIFICATIONS
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a



p4a.branch = master               

android.release = True
android.release_artifact = apk

