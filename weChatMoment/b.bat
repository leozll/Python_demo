@echo off

::��������
adb kill-server
adb connect 127.0.0.1:26944

::����apk
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI
ping 127.0.0.1 -n 5 -w 1000 > nul

::��������Ȧ
::adb shell input tap 450 1200
::adb shell input tap 450 230

set loopSeq=1
::��ʼѭ��ˢ��

echo ��%loopSeq%�λ���ˢ��......
adb shell input swipe 500 200  500 1200
ping 127.0.0.1 -n 2 -w 1000 > nul

if "%loopSeq%"=="10" (
GOTO :end)

set /a loopSeq+=1 
GOTO :start



