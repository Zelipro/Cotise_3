[app]
title = Cotise
package.name = Cotise
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,jpeg,db,webp
source.include_patterns = Pages/*,*.db,*.jpeg,*.jpg,*.png,*.webp
version = 1.1
requirements = python3,kivy,kivymd,sqlite3,pillow
icon.filename = %(source.dir)s/Logo.png


[buildozer]
log_level = 2

[android]
api = 34
minapi = 21
ndk = 25b
sdk = 34
android.archs = arm64-v8a , armeabi-v7a  # Start with one arch to simplify
orientation = all
android.orientation = all
