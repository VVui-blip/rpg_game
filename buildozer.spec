[app]
title = Pixel Realm RPG
package.name = pixelrealmrpg
package.domain = org.vdev

source.dir = .
source.include_exts = py,png,jpg,jpeg,atlas,ogg,wav,ttf,json,tmx,tsx

version = 0.1.0

requirements = python3,pygame-ce

orientation = landscape
fullscreen = 1

icon.filename = %(source.dir)s/assets/sprites/icon.png

android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
