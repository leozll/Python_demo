from io import BytesIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from PIL import Image
from os import listdir
import os
from selenium.webdriver.chrome.options import Options


class GetCheckPic:
    def __init__(self, username, password, browser):
        self.username = username  # 微博账号
        self.password = password  # 微博密码
        self.browser = browser  # 无头浏览器
        self.wait = WebDriverWait(self.browser, 20)  # 等待时间
        self.url = "https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/"  # 目标url

    def open(self):  # 打开网页
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, "loginName")))  # 用户名标签
        password = self.wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))  # 密码标签
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, "loginAction")))  # 提交按钮标签
        username.send_keys(self.username)  # 输入账号
        password.send_keys(self.password)  # 输入密码
        time.sleep(1)
        submit.click()  # 按提交按钮
        time.sleep(2)

    def get_position(self):  # 获取验证码图片的位置
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "patt-shadow")))  # 出现验证码图片的html标签
        except TimeoutError:
            print("验证码未出现")
            self.open()  # 未出现验证码图片标签则重新打开网页
        time.sleep(2)
        location = img.location  # 获取验证码图片的位置
        size = img.size  # 验证码图片的大小
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']  # 验证码图片的坐标
        return top, bottom, left, right

    def is_pixel_equal(self, image1, image2, x, y):  # 像素匹配
        threshold = 20  # 阈值
        pixel1 = image1.load()[x, y]  # 读取图片1的像素
        pixel2 = image2.load()[x, y]  # 读取图片2的像素 RGBA既在原有RGB的的基础上加上A（透明度）  例如[252,232,255,255]
        if abs(pixel2[0] - pixel1[0]) < threshold and abs(pixel2[1] - pixel1[1]) < threshold and \
                abs(pixel2[2] - pixel1[2]) < threshold:  # 如果像素小于阈值则判断这一个像素一样
            return True
        else:
            return False

    def get_screenshot(self):  # 获得验证码的截图
        screenshot = self.browser.get_screenshot_as_png()  # 截图用png截取
        screenshot = Image.open(BytesIO(screenshot))  # 用bytes打开图片
        return screenshot

    def get_image(self, n):  # 获取验证码截图
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))  # 截取的图片
        print("获取到验证码")
        if not self.detect_image(captcha):  # 如果截取的验证码在验证码数据库中没有则保存验证码
            os.chdir(r"D:\untitled\cookie池\login\CheckPic")  # 验证码数据库
            captcha.save(str(n) + ".png")
            print("保存成功")
            os.chdir(r"D:\untitled\cookie池")

    def same_image(self, image, model):  # 判断两张图片是否相同
        count = 0  # 如果这个像素点一样 则count加1
        threshold = 0.99  # 图片匹配度的阈值
        for x in range(image.width):
            for y in range(image.height):
                # 匹配每个像素点
                if self.is_pixel_equal(image, model, x, y):  # 像素一样则加一
                    count += 1
        result = float(count) / (image.height * image.width)  # 匹配度
        if result > threshold:  # 大于匹配度阈值则相同
            return True
        else:
            return False

    def detect_image(self, image):  # 在验证码数据库中检测
        for model in listdir(r"D:\untitled\cookie池\login\CheckPic"):  # 遍历验证码数据库中的每张验证码
            image_path = r"D:\untitled\cookie池\login\CheckPic\\" + model
            model_image = Image.open(image_path)
            if self.same_image(image, model_image):
                print("验证码库中有此验证码，重新获取验证码。")
                return True


if __name__ == '__main__':
    n = 0
    while True:
        n += 1
        if len(listdir(r"D:\untitled\cookie池\login\CheckPic")) == 24:
            break
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(chrome_options=chrome_options)  # 无头模式
        get = GetCheckPic("账号", "密码", browser)
        get.open()
        get.get_position()
        get.get_image(n)
        browser.close()
    print("验证码已收集完全。")