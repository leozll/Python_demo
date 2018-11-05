@echo off

::重启进程
adb kill-server
adb connect 127.0.0.1:26944


::启动apk
adb shell am start moe.chionlab.wechatmomentstat/moe.chionlab.wechatmomentstat.gui.MainActivity
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击运行
adb shell input tap 500 1200
ping 127.0.0.1 -n 30 -w 1000 > nul
::左上角导出朋友圈数据
adb shell input tap 150 250
ping 127.0.0.1 -n 3 -w 1000 > nul

::右上角导出
adb shell input tap 650 110
ping 127.0.0.1 -n 3 -w 1000 > nul

::点击完成
adb shell input tap 360 750
ping 127.0.0.1 -n 3 -w 1000 > nul

::返回主页
adb shell input tap 50 100
ping 127.0.0.1 -n 3 -w 1000 > nul

adb shell input tap 50 100
ping 127.0.0.1 -n 3 -w 1000 > nul

::从设备复制文件
adb pull /sdcard/WechatMomentStat/exported_sns.json C:/Users/ZLL/Desktop/exported_sns.json


