[app]

title = luisito
package.name = luisito
package.domain = org.myapp

source.dir = .
source.include_exts = py,png,osm,mp3
source.include_patterns = iconos/*, *.png, *.osm, *.mp3

version = 1

requirements =  python3,kivy==2.3.1,plyer@https://github.com/kivy/plyer/archive/master.zip,requests

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icono_ico.png
presplash.filename = %(source.dir)s/icono_inicio.png

android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

# Permisos necesarios
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,POST_NOTIFICATIONS

p4a.branch = master               

android.release = True
android.release_artifact = apk

