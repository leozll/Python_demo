::删除wechat缓存
adb shell rm /data/data/com.tencent.mm/MicroMsg/1f2d60f3e1348a8b657ffb1ac670713d/SnsMicroMsg.db 
::关闭wechat
adb shell am force-stop com.tencent.mm
::重启wechat
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI
