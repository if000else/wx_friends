# coding=utf-8
'''
  Created by lyy on 2019-04-20
'''
import math

from PIL import Image
from pyecharts import Bar, configure, Pie
import os
import photomosaic as pm

# 将这行代码置于首部，设置全局图表主题
configure(global_theme='vintage')

__author__ = 'lyy'

path = os.getcwd() + '/app/output/'


# 好友数量柱状图
def draw_friends_num(total, male, female, others):
    attr = ["男", "女", "其他"]
    value = [male, female, others]
    pie = Pie(title="微信好友人数分布", subtitle=str("好友总数：" + str(total)))
    pie.add("", attr, value, is_label_show=True)
    pie.render(path=path + 'friends_num.png')


# 好友地域分布图
def draw_friends_location(province, city):
    attr_city = []
    val_city = []

    for i in city:
        attr_city.append(i[0])
        val_city.append(i[1])

    attr_province = []
    val_province = []
    for i in province:
        attr_province.append(i[0])
        val_province.append(i[1])

    bar = Bar("微信好友市级分布直方图")
    bar.add("", attr_city, val_city, is_stack=True, is_label_show=True)
    bar.render(path=path + 'friends_location_city.png')

    pie = Pie("微信好友省级分布饼状图")
    pie.add("", attr_province, val_province, is_label_show=True)
    pie.render(path=path + 'friends_location_province.png')


# 好友签名情感分析图
def draw_friends_signature_emotion(negative, positive, others):
    attr = ['消极', '积极', '中性']
    val = [negative, positive, others]
    pie = Pie("微信好友情绪分析饼状图")
    pie.add("", attr, val, is_label_show=True)
    pie.render(path=path + 'friends_signature_emotion.png')


# 利用好友头像生成蒙太奇马赛克图片
def draw_friends_mosaic_image():
    # 读取基准图，即要生成的蒙太奇马赛克图片的原始图
    image = pm.imread(os.getcwd() + '/assets/cxk.jpg')
    # 定义图片库
    pool = pm.make_pool(os.getcwd() + '/temp/*.jpg')
    # 制作50*50的拼图马赛克,(50, 50)是指每一行和每一列使用图片库中的图像的个数
    mosaic = pm.basic_mosaic(image, pool, (50, 50))
    # 保存制作好的图片
    pm.imsave(os.getcwd() + '/output/friends_mosaic_image.jpg', mosaic)


# 拼接头像
def draw_friends_avatars():
    path = os.getcwd() + '/temp/'
    # 获取文件夹内头像个数
    length = len(os.listdir(path))
    # 设置画布大小
    image_size = 2560
    # 设置每个头像大小
    each_size = math.ceil(2560 / math.floor(math.sqrt(length)))
    # 计算所需各行列的头像数量
    x_lines = math.ceil(math.sqrt(length))
    y_lines = math.ceil(math.sqrt(length))
    image = Image.new('RGB', (each_size * x_lines, each_size * y_lines))
    x = 0
    y = 0
    for (root, dirs, files) in os.walk(path):
        for pic_name in files:
            # 增加头像读取不出来的异常处理
            try:
                with Image.open(path + pic_name) as img:
                    img = img.resize((each_size, each_size))
                    image.paste(img, (x * each_size, y * each_size))
                    x += 1
                    if x == x_lines:
                        x = 0
                        y += 1
            except IOError:
                print("头像读取失败")

    image.save(os.getcwd()+"/output/friends_avators.png")
    print('微信好友头像拼接完成!')


if __name__ == '__main__':
    # draw_friends_mosaic_image()
    draw_friends_avatars()
