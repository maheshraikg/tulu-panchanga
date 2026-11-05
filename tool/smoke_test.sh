#!/usr/bin/env bash
# Installs an APK on the running emulator, opens the app, and fails if it
# crashes. Prints the crash stack trace from logcat.
# Usage: tool/smoke_test.sh <apk> <package>
set -u
APK=$1 PKG=$2
adb wait-for-device
adb shell 'while [ "$(getprop sys.boot_completed)" != 1 ]; do sleep 2; done'
adb shell input keyevent 82 || true
adb install -r -g "$APK" || { echo "::error::install failed"; exit 1; }
adb logcat -c
adb shell monkey -p "$PKG" -c android.intent.category.LAUNCHER 1
sleep 40
# Tap around the bottom tabs and back to exercise the main screens.
for x in 300 500 700 900 100; do adb shell input tap $x 2200 || true; sleep 4; done
adb logcat -d > logcat.txt
PID=$(adb shell pidof "$PKG" | tr -d '\r')
echo "app pid: '${PID}'"
echo "===== crash lines ====="
grep -n -A60 "FATAL EXCEPTION\|Fatal signal\|AndroidRuntime\|F DEBUG\|F libc\|Abort message" logcat.txt | head -300
echo "===== app log (tail) ====="
grep -i "$PKG\|flutter" logcat.txt | tail -80
if grep -q "FATAL EXCEPTION\|Fatal signal" logcat.txt || [ -z "$PID" ]; then
  echo "::error::app crashed or is not running"
  exit 1
fi
echo "app is running, no crash"
