[app]

title = myapp
package.name = myapp
package.domain = org.example

source.dir = .
source.include_exts = py,java,xml
#source.include_patterns = iconos/*, *.png, *.osm, *.mp3

version = 1

requirements =  python3,kivy==2.3.1,pyjnius

orientation = portrait
fullscreen = 0

android.manifest = AndroidManifest.xml

android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a



p4a.branch = master               

android.release = True
android.release_artifact = apk

