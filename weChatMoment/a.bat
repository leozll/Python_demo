@echo off

:: 手动进入指定朋友圈,初始化刷新指定朋友圈
set loopCount=%1
:: 不指定循环次数的话默认循环10次
if "%loopCount%"=="" (
set loopCount=10)

::重启进程
adb kill-server
adb connect 127.0.0.1:26944

::循环刷新
for /l %%i in (1,1,%loopCount%) do (
echo 第%%i次滑动刷新......
adb shell input swipe 500 1200  500 200
)

