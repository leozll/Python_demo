@echo off

::��������
adb kill-server
adb connect 127.0.0.1:26944


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


