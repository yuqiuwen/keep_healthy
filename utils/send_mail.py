import random

from django.core.mail import send_mail
from django.conf import settings

from celery_tasks.main import celery_app
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, JsonResponse, request



def send_mail_code(request, to_email_account):
    """
    发送邮箱验证码
    @param to_email_account: 向目标用户发送邮件
    @return:
    """
    sms_code = '%06d' % random.randint(0, 999999)
    email_title = '邮箱激活'
    email_content = '您的邮箱注册验证码为：{}，该验证码有效时间为2分钟'.format(sms_code)

    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)
    # 将随机的验证存在session表中，方便进行验证
    request.session['rand_code'] = verification_code
    send_res = send_mail(email_title, email_content, settings.EMAIL_FROM, [to_email_account])

    return send_res

def gen_verify_email_url(user):
    """
    生成邮箱激活链接
    @param user: 当前登录用户
    @return: token
    """
    email_verify_url = 'http://' + settings.BACKEND_URL + '/emails/verification'
    s = Ser