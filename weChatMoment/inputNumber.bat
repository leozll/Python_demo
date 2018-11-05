@echo off

set loopCount=%1
echo mobile: %loopCount%

d:
cd D:\Droid4X\Droid4X

::重启进程
adb kill-server
adb connect 127.0.0.1:26944

::关闭wechat
adb shell am force-stop com.tencent.mm
::重启wechat
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI



::点击搜索
echo 点击搜索
adb shell input tap 530 90
ping 127.0.0.1 -n 5 -w 1000 > nul

::输入手机号
echo 输入手机号
adb shell input text %loopCount%
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击查号手机号
echo 点击查号手机号
adb shell input tap 500 200
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击发消息
echo 点击发消息
adb shell input tap 500 860
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击右上角头像
echo 点击右上角头像
adb shell input tap 650 95
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击左上角头像
echo 点击右上角头像
adb shell input tap 90 270
ping 127.0.0.1 -n 5 -w 1000 > nul

::点击相册
echo 点击右上角头像
adb shell input tap 700 790
ping 127.0.0.1 -n 5 -w 1000 > nul




::循环刷新
for /l %%i in (1,1,500) do (
echo 第%%i次滑动刷新......
adb shell input swipe 500 1200  500 200
)








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


python C:\Users\ZLL\Desktop\Convert2CSV.py

::删除wechat缓存
adb shell rm /data/data/com.tencent.mm/MicroMsg/1f2d60f3e1348a8b657ffb1ac670713d/SnsMicroMsg.db 


