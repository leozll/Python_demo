@echo off

:: �ֶ�����ָ������Ȧ,��ʼ��ˢ��ָ������Ȧ
set loopCount=%1
:: ��ָ��ѭ�������Ļ�Ĭ��ѭ��10��
if "%loopCount%"=="" (
set loopCount=10)

::��������
adb kill-server
adb connect 127.0.0.1:26944

::ѭ��ˢ��
for /l %%i in (1,1,%loopCount%) do (
echo ��%%i�λ���ˢ��......
adb shell input swipe 500 1200  500 200
)








::����apk
adb shell am start moe.chionlab.wechatmomentstat/moe.chionlab.wechatmomentstat.gui.MainActivity
ping 127.0.0.1 -n 5 -w 1000 > nul

::�������
adb shell input tap 500 1200
ping 127.0.0.1 -n 30 -w 1000 > nul
::���Ͻǵ�������Ȧ����
adb shell input tap 150 250
ping 127.0.0.1 -n 3 -w 1000 > nul

::���Ͻǵ���
adb shell input tap 650 110
ping 127.0.0.1 -n 3 -w 1000 > nul

::������
adb shell input tap 360 750
ping 127.0.0.1 -n 3 -w 1000 > nul

::������ҳ
adb shell input tap 50 100
ping 127.0.0.1 -n 3 -w 1000 > nul

adb shell input tap 50 100
ping 127.0.0.1 -n 3 -w 1000 > nul

::���豸�����ļ�
adb pull /sdcard/WechatMomentStat/exported_sns.json C:/Users/ZLL/Desktop/exported_sns.json




python C:\Users\ZLL\Desktop\Convert2CSV.py

::ɾ��wechat����
adb shell rm /data/data/com.tencent.mm/MicroMsg/1f2d60f3e1348a8b657ffb1ac670713d/SnsMicroMsg.db 
::�ر�wechat
adb shell am force-stop com.tencent.mm
::����wechat
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI
