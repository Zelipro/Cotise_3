[app]
# Nom de votre application
title = Cotiser

# Nom du package (doit être unique, format : org.nom)
package.name = gestioncotisations
package.domain = org.elisco

# Fichier principal de votre application
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.exclude_dirs = tests, bin, venv

# Version de l'application
version = 1.0

# Dépendances Python nécessaires
requirements = python3,kivy==2.3.0,kivymd==2.3.0,sqlite3,reportlab,pillow

# Orientation de l'application (landscape, portrait, ou all)
orientation = portrait

# Permissions Android nécessaires
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Fichier d'icône (facultatif, placez une image .png dans le répertoire)
# icon.filename = %(source.dir)s/icon.png

# Fichier de splash screen (facultatif)
# presplash.filename = %(source.dir)s/presplash.png

# Version minimale de l'API Android
android.api = 21

# Architecture cible
android.archs = arm64-v8a, armeabi-v7a

# Autres paramètres pour la signature de l'APK (pour la version release)
# android.release_artifact = aab  # Utilisez 'aab' pour Google Play Store, 'apk' pour debug
# android.add_aapt2 = True

# Dossier où Buildozer stocke les fichiers temporaires
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ant_path = ~/.buildozer/android/platform/apache-ant-1.9.4

[buildozer]
# Niveau de log
log_level = 2

# Activer la compilation en mode debug
android.debug_artifact = apk
