[app]
title = Cotise
package.name = Cotisation
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
requirements = python3,kivy,kivymd,sqlite3,fpdf2,pillow
icon.filename = %(source.dir)s/Logo.png

[buildozer]
log_level = 2

[android]
api = 34
minapi = 21
ndk = 25b
sdk = 34
android.permissions = INTERNET
android.archs = arm64-v8a  # Start with one arch to simplify
orientation = all
android.orientation = all
