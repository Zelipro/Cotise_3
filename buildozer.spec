[app]
title = Cotise
package.name = Cotisation
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
requirements = python3,kivy,kivymd,sqlite3,reportlab==3.6.12,pillow
icon.filename = %(source.dir)s/Logo.png

[buildozer]
log_level = 2

[android]
api = 34
minapi = 21
ndk = 25b
sdk = 34
android.permissions = INTERNET
android.archs = arm64-v8a  # Temporarily use one arch
orientation = all
android.orientation = all
