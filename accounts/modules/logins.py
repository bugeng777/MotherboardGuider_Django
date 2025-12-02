import json
import uuid

from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserInfo, CAPTCHA, RestCount
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from accounts.modules.tools import ProduceCode
from django.db.utils import IntegrityError
from accounts.modules.utils import contrast_time
from accounts.modules.values import email_arr, token_private_secret, default_rest_count
import jwt as jwt
from django.http.response import HttpResponse, JsonResponse
import time
import datetime

@csrf_exempt
def register(request):
    body_json = json.loads(request.body)
    nick_name = body_json.get('nick_name')
    contact_ad = body_json.get('contact_ad')
    pwd = body_json.get('pwd')
    app_name = body_json.get('app_name')
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = uuid.uuid1()

    try:
        userHistory = UserInfo.objects.filter(contact_ad=contact_ad)
        if len(userHistory) == 0:
            #     没有有历史记录就插入
            register_result = UserInfo.objects.create(
                user_id=user_id,
                contact_ad=contact_ad,
                nick_name=nick_name,
                pwd=pwd,
                user_avatar='',
                app_name=app_name,
                create_time=create_time
            )
            print("注册了")
            return HttpResponse(json.dumps({'code': 0, 'data': '注册成功!'}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'data': '已存在账号，请直接登录或者输入别的账号'}))
    except IntegrityError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求错误，请检查参数'}))

@csrf_exempt
def login_check(request):
    body_json = json.loads(request.body)
    contact_ad = body_json.get('contact_ad')
    pwd = body_json.get('pwd')
    now_time = int(time.time())
    try:
        userHistory = UserInfo.objects.filter(contact_ad=contact_ad, pwd=pwd)
        if len(userHistory) != 0:
            #     登录成功返回token
            encoded = jwt.encode({"user_id": userHistory[0].user_id, "overdue_time": now_time}, token_private_secret,
                                 algorithm="HS256")
            return HttpResponse(
                json.dumps({'code': 0, 'data': '登录成功!', 'token': encoded, 'contact_ad': contact_ad}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'data': '账号或密码错误'}))
    except IntegrityError:
        return HttpResponse(json.dumps({'code': 1, 'data': '请求错误，请检查参数'}))

@csrf_exempt
def pwd_miss_email_send(request):
    # 找回密码发送验证码
    try:
        body_json = json.loads(request.body)
        contact_ad = body_json.get('contact_ad')
        app_name = body_json.get('app_name')
        a_c = ProduceCode.auth_code(option='num')
        CAPTCHA.objects.create(
            create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            contact_ad=contact_ad,
            target_type='ChangePwd',
            code=a_c,
        )
        if not contact_ad:
            return HttpResponse(json.dumps({'code': 1, 'data': '发送失败,请输入邮箱'}))
        email_ad = email_arr[app_name]['email_ad']
        email_pwd = email_arr[app_name]['pwd']
        app_name_cn = email_arr[app_name]['app_name_cn']
        now_time = int(time.time())
        con = smtplib.SMTP_SSL('smtp.163.com', 465)
        con.login(email_ad, email_pwd)
        msg = MIMEMultipart()
        subject = Header('找回密码', 'utf-8').encode()
        msg['Subject'] = subject
        msg['From'] = email_ad + ' <' + email_ad + '>'
        msg['To'] = contact_ad
        pwd_miss_code = jwt.encode({"contact_ad": contact_ad, "overdue_time": now_time}, token_private_secret,
                                   algorithm="HS256")
        # 添加html内容
        content = f"""
        <h2>{app_name_cn}</h2>
        <p>您正在找回密码</p>
        <p>验证码: {a_c}</p>
        <img src='https://www.chatmato.cn/someRes/znlt_img_res/logo.png'> <p>智星喵聊</p>
         <p>验证码仅在五分钟内有效，为了您的信息安全，请不要随意转发他人</p>

        """
        html = MIMEText(content, 'html', 'utf-8')
        msg.attach(html)
        # 发送邮件
        con.sendmail(email_ad, contact_ad, msg.as_string())
        con.quit()
        return HttpResponse(json.dumps({'code': 0, 'data': '发送成功'}))
    except:
        return HttpResponse(json.dumps({'code': 1, 'data': '发送失败'}))
        pass

@csrf_exempt
def change_pwd_check(request):
    try:
        body_json = json.loads(request.body)
        contact_ad = body_json.get('contact_ad')
        reinput_pwd = body_json.get('reinput_pwd')
        pwd = body_json.get('pwd')
        verfi_word = body_json.get('verfi_word')

        if reinput_pwd != pwd:
            return HttpResponse(json.dumps({'code': 1, 'data': '请确认密码是否相同'}))
        cp = CAPTCHA.objects.filter(contact_ad=contact_ad).order_by('-create_time')
        if len(pwd) == 0:
            return HttpResponse(json.dumps({'code': 1, 'data': '请正确输入密码'}))
        if len(verfi_word) != 6:
            return HttpResponse(json.dumps({'code': 1, 'data': '请输入正确的验证码'}))
        if len(cp) > 0:
            t_o = cp[0]
            print("时间差:", contrast_time(t_o.create_time))
            if t_o.code == verfi_word and contrast_time(t_o.create_time) < 300:
                # 验证码是对的，还要验证时间对不对
                u_i = UserInfo.objects.get(contact_ad=contact_ad)
                u_i.pwd = pwd
                u_i.save()
                return HttpResponse(json.dumps({'code': 0, 'data': '修改完成'}))
            else:
                return HttpResponse(json.dumps({'code': 1, 'data': '超时了，请重新发送验证码'}))
        else:
            return HttpResponse(json.dumps({'code': 1, 'data': '超时或无验证码接收'}))
    except:
        return HttpResponse(json.dumps({'code': 1, 'data': '无法修改，服务器内部错误，请联系管理员'}))
        pass


def generate_short_uuid():
    random_uuid = str(uuid.uuid4())
    parts = random_uuid.split("-")
    return parts[0] + parts[1]


def create_temporary_user(request):
    body_json = json.loads(request.body)
    app_name = body_json.get('app_name')
    try:
        user_id = uuid.uuid1()
        pwd_random = generate_short_uuid()
        print("pwd", pwd_random)
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        register_temporary_result = UserInfo.objects.create(
            user_id=user_id,
            nick_name='',
            user_avatar='',
            app_name=app_name,
            contact_ad='',
            pwd=pwd_random,
            create_time=create_time
        )
        RestCount.objects.create(
            user_id=user_id, app_name=app_name, rest_count=default_rest_count
        )
        now_time = int(time.time())
        encoded = jwt.encode({"user_id": str(user_id), "overdue_time": now_time}, token_private_secret,
                             algorithm="HS256")
        return JsonResponse({'code': 0, 'data': 'Login successful.', 'token': encoded, 'contact_ad': '',
                             'nick_name': '', 'user_id': user_id}, status=200)
    except IntegrityError:
        return JsonResponse({'code': 1, 'data': 'Request error. Please check the parameters.'}, status=403)