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

