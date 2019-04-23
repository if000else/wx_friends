import os

import itchat

from app.utils.draw_utils import draw_friends_num, draw_friends_location, draw_friends_signature_emotion, \
    draw_friends_avatars
from app.utils.nlp_utils import analyze_text


# 初始化itchat
def init():
    # hotReload(热加载),短时间内不需要再次扫码登陆
    itchat.auto_login(hotReload=True)


# 获取好友信息
def get_friends():
    # 获取微信好友的信息,返回的是json格式的信息
    friends = itchat.get_friends(update=True)[0:]
    # print(friends)
    return friends


# 对好友数进行分析
def analyze_friends_num(friends):
    # 初始化性别的变量(男、女、其他，其他表示的是注册时没有填写性别信息的)
    male = female = others = 0
    # 循环得到的全部好友
    # 在好友的信息中有Sex标签,发现规律是当其值为1是表示男生,2表示女生,0表示没有填写的
    for i in friends[1:]:
        sex = i['Sex']
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            others += 1
    # 总人数
    total = len(friends[2:])
    print("总人数为", total, "其中男性", male, "人，女性", female, "人，男女比为", round((male / female), 2), ":1")

    # 画出分布图
    draw_friends_num(total, male, female, others)


# 分析好友的地域分布
def analyze_friends_location(friends):
    province = {}
    city = {}
    for i in friends[1:]:
        if i['Province'] == '':
            i['Province'] = '其他'
        if i['City'] == '':
            i['City'] = '其他'

        province[i['Province']] = province.get(i['Province'], 0) + 1
        city[i['City']] = city.get(i['City'], 0) + 1
    sorted_province = sorted(province.items(), key=lambda item: item[1], reverse=True)
    sorted_city = sorted(city.items(), key=lambda item: item[1], reverse=True)

    # 画出分布图
    draw_friends_location(sorted_province[0:5], sorted_city[0:15])


# 分析好友的签名
def analyze_friends_signature(friends):
    positive = 0
    negative = 0
    others = 0

    print('签名情感分析中，请稍后......')
    for index, item in enumerate(friends[1:]):
        text = item['Signature']
        if text != '':
            try:
                print('正在分析第', index, '条签名：', text, '他的作者是：', item['NickName'], '你给他的备注是：', item['RemarkName'])
                res = analyze_text(text)
                if res == 0:
                    negative = negative + 1
                if res == 1:
                    others = others + 1
                if res == 2:
                    positive = positive + 1
            except:
                continue

    # 画出分布图
    draw_friends_signature_emotion(negative, positive, others)


# 获取好友头像
def get_friends_avatar(friends):
    for index, item in enumerate(friends):
        print("正在下载第 %d 张头像" % index)
        img = itchat.get_head_img(userName=item["UserName"])
        file_image = open(os.getcwd() + "/app/temp/" + item["UserName"] + ".jpg", 'wb')
        file_image.write(img)
        file_image.close()

    # 拼接头像
    draw_friends_avatars()


if __name__ == '__main__':
    init()
    friends = get_friends()
    # get_friends_avatar(friends)
    analyze_friends_num(friends)
    # analyze_friends_location(friends)
    # analyze_friends_signature(friends)
