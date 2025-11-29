import jwt as jwt
import time
from django.utils import timezone

from accounts.models import UserInfo
from accounts.modules.values import token_private_secret
import json
import datetime
from django.http.response import HttpResponse, JsonResponse
import socket


def token_time_pick(overdue_time):
    # 多久之后过期  并且返回时间戳
    now = datetime.datetime.now().replace(microsecond=0)  # 当前时间
    # ago = now - datetime.timedelta(days=30)  # 当前时间往前推30天
    later = now + datetime.timedelta(days=overdue_time)  # 当前时间往后推30天
    return later


def token_time_compare(token):
    de_code = jwt.decode(token, token_private_secret, algorithms=["HS256"])
    now_time = int(time.time())
    token_time = de_code['overdue_time']
    return now_time - token_time


def contrast_time(create_time):
    # 返回时间差，时间戳
    now = timezone.now()
    now_stamp = time.mktime(now.timetuple())
    create_stamp = time.mktime(create_time.timetuple())
    return now_stamp - create_stamp


def token_user_id(token):
    de_code = jwt.decode(token, token_private_secret, algorithms=["HS256"])
    return de_code['user_id']


def has_key(json_obj, key):
    if key in json_obj:
        return True
    else:
        return False


def token_check(token):
    print(token_time_compare(token))


def query_share_count(request):
    # 查询vip时间以及提问题的次数
    body_json = json.loads(request.body)
    token = body_json.get('token')
    app_name = body_json.get('app_name')
    rest_count = 0
    vip_time = '暂无'
    nick_name = '无'
    contact_ad = '无'
    user_id = token_user_id(token)
    try:
        rest_count = RestCount.objects.filter(user_id=user_id)[0].rest_count
    except:
        print("没分享次数结果，返回0：" + user_id)
        pass
    try:
        vip_time = UserInfo.objects.filter(user_id=user_id, app_name=app_name)[0].vip_time
        nick_name = UserInfo.objects.filter(user_id=user_id, app_name=app_name)[0].nick_name
        contact_ad = UserInfo.objects.filter(user_id=user_id, app_name=app_name)[0].contact_ad
        if contrast_time(vip_time) > 0:
            vip_time = "无"
        else:
            vip_time = vip_time.strftime("%Y-%m-%d")
    except:
        print("vip查询失败，难道这用户还没创建就查询：" + user_id)
        pass
    return HttpResponse(
        json.dumps({'code': 0, 'rest_count': rest_count, 'vip_time': vip_time, 'nick_name': nick_name,
                    'contact_ad': contact_ad}))


def udp_listen(request):
    # 创建 UDP 套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定监听地址和端口号
    listen_addr = ('192.168.0.106', 7777)

    udp_socket.bind(listen_addr)

    # 循环监听数据包
    while True:
        # 接收数据包
        data, addr = udp_socket.recvfrom(1024)
        # v1, v2, v3, v4, v5, v6, v7 = struct.unpack('iiiiiii', addr)
        # print("数据v1:", v1)
        # print("数据v2:", v2)
        # print("数据v3:", v3)
        # print("数据v4:", v4)
        # print("数据v5:", v5)
        # print("数据v6:", v6)
        # print("数据v7:", v7)
        # 解析数据包
        data_str = data.decode('utf-8')
        data_list = data_str.split(',')
        # 数组已经是正确的结果了
        #  删除这里的时候记得删除导入的struct和socket
        print(data_str)
        print(data_list)
        # 处理数据
        # ...
    # 关闭套接字
    udp_socket.close()