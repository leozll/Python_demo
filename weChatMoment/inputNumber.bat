@echo off

set loopCount=%1
echo mobile: %loopCount%

d:
cd D:\Droid4X\Droid4X

::��������
adb kill-server
adb connect 127.0.0.1:26944

::�ر�wechat
adb shell am force-stop com.tencent.mm
::����wechat
adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI



::�������
echo �������
adb shell input tap 530 90
ping 127.0.0.1 -n 5 -w 1000 > nul

::�����ֻ���
echo �����ֻ���
adb shell input text %loopCount%
ping 127.0.0.1 -n 5 -w 1000 > nul

::�������ֻ���
echo �������ֻ���
adb shell input tap 500 200
ping 127.0.0.1 -n 5 -w 1000 > nul

::�������Ϣ
echo �������Ϣ
adb shell input tap 500 860
ping 127.0.0.1 -n 5 -w 1000 > nul

::������Ͻ�ͷ��
echo ������Ͻ�ͷ��
adb shell input tap 650 95
ping 127.0.0.1 -n 5 -w 1000 > nul

::������Ͻ�ͷ��
echo ������Ͻ�ͷ��
adb shell input tap 90 270
ping 127.0.0.1 -n 5 -w 1000 > nul

::������
echo ������Ͻ�ͷ��
adb shell input tap 700 790
ping 127.0.0.1 -n 5 -w 1000 > nul




::ѭ��ˢ��
for /l %%i in (1,1,500) do (
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


