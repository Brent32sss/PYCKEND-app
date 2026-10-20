[app]

# (str) Title of your application
title = Pickly

# (str) Package name
package.name = pickly

# (str) Package domain (needed for android/ios packaging)
package.domain = com.pickly

# (source.dir) Source directory (where you put your main.py)
source.dir = .

# (list) Source include patterns (incluye código, imágenes, kv y datos json/fuentes)
source.include_exts = py,png,jpg,kv,atlas,json,ttf

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Aceptar automaticamente todas las licencias del SDK de Google / Android
android.accept_sdk_license = True

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon buildozer run if buildozer spec is older than last buildozer.spec in .buildozer
warn_on_root = 1
