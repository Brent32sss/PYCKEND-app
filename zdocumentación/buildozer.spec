[app]

# (str) Title of your application
title = Pickly

# (str) Package name
package.name = pickly

# (str) Package domain (needed for android/ios packaging)
package.domain = com.pickly

# (source.dir) Source directory (where you put your main.py)
source.dir = .

# (list) Source include patterns (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source exclude patterns
#source.exclude_exts = spec

# (list) List of directory to exclude from include on Android
#android.gradle_dependencies =

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash of the application (image or drawable XML)
# presplash.filename = %(source.dir)s/data/presplash.png

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should match android.minapi
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate that the application should be treated as a library (Android only)
# android.is_library = False

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.archs = arm64-v8a

# (bool) Indicate that the application should be treated as a library (Android only)
# android.is_library = False

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional libraries to copy into libs/armeabi*/
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/androidv7/*.so
#android.add_libs_arm64_v8a = libs/android64/*.so

# (bool) Indicate that the screen should stay on
# android.wakelock = False

# (list) Pattern matching allowed src_dirs of internal storage of Android
#android.private_storage_size = 2GB

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android gradle dependencies
#android.gradle_dependencies = 

# (list) Pattern matching allowed src_dirs of internal storage of Android
#android.private_storage_size = 2GB

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon buildozer run if buildozer spec is older than last buildozer.spec in .buildozer
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
