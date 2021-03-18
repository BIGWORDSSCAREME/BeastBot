adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png %1
adb shell rm /sdcard/screen.png