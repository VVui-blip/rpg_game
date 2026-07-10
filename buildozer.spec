[app]
title = Terminal Quest
package.name = terminalquest
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,txt

version = 0.1

requirements = python3,pygame

orientation = landscape
fullscreen = 0

# Icon/presplash: bỏ ảnh vào assets/ rồi bỏ comment 2 dòng dưới
# icon.filename = %(source.dir)s/assets/images/icon.png
# presplash.filename = %(source.dir)s/assets/images/presplash.png

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
