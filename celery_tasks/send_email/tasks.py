import random
import smtplib
import traceback

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from celery_tasks.main import celery_app
from logger import logger

# 异步任务


@celery_app.task(name='send_sms_code')
def send_mail_code(email, user, code):
    """
    发送邮箱验证码
    @param to_email_account: 向目标用户发送邮件
    @return:
    """
    try:

        email_title = '注册验证码'

        html_content = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
                <div style="width: 900px;margin:20px">
                    <div style="background-color: #6cc2b4; padding: 10px;color: whitesmoke">
                        <h2 style="padding:0 20px">AnimaCare</h2>
                    </div>
                    <div style="padding: 10px 40px">
                        <p>Hey {user}!</p>
                        <p>Your verification code for this registration is:</p>
                        <div style="display: flex; align-items: center">
                            <h2 style="padding-left: 20px ">{code}</h2>
                
                        </div>
            
                        <br>
                        <p style="color: #a0a0a9; font-size: 14px">This email is sent by the system, no need to reply</p>
                    </div>
            
                </div>
            </body>
            </html>
            """

        # 将随机的验证存在session表中，方便进行验证
        # request.session['rand_code'] = verification_code
        send_res = send_mail(subject=email_title,
                             message="",
                             from_email=settings.EMAIL_FROM,
                             recipient_list=[email],
                             html_message=html_content)

        print('send_res----', send_res)
        return send_res
    except smtplib.SMTPException as e:
        raise e
    except Exception as e:
        logger.error(traceback.format_exc(limit=3))
        raise e