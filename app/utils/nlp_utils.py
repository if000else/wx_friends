# coding=utf-8
'''
  Created by lyy on 2019-04-20
'''

__author__ = 'lyy'

from aip import AipNlp

""" 这里是我的 APPID AK SK ，大家在使用的时候记得更改成自己的"""
APP_ID = '16068652'
API_KEY = '7hASMno7HeMcTAIE7pknvBBB'
SECRET_KEY = '03qKj0ktezB7MyQfI4UX3RkGFbF1dmSp'


client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def analyze_text(text):
    res = client.sentimentClassify(text.strip())
    return res['items'][0]['sentiment']


if __name__ == '__main__':
    analyze_text('不是因为有希望才坚持，而是因为坚持才有希望。')
