d:
cd D:\Users\ZLL\AppData\Local\Android\sdk\platform-tools

adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI
adb shell input tap 500 1200
adb shell input tap 500 125
adb shell input swipe 500 200  500 700



adb shell input swipe 500 1200  500 700



adb shell ls /storage/emulated/0



##初始化刷新执行人的朋友圈
##循环滑动查看所有朋友圈信息
for /l %i in (1,1,200) do adb shell input swipe 1200 500  1200 200
##启动导出apk
adb shell am start moe.chionlab.wechatmomentstat/moe.chionlab.wechatmomentstat.gui.MainActivity
##点击导出
adb shell input tap 500 700
##确定导出
adb shell input tap 150 130
##导出
adb shell input tap 1225 63
adb shell input tap 650 422
##从设备复制文件
adb pull /storage/sdcard0/WechatMomentStat/exported_sns.json exported_sns.json
adb pull /sdcard/WechatMomentStat/exported_sns.json exported_sns.json

