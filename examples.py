from djangomail import send_mail,send_mass_mail
import settings
#import os
#os.environ.setdefault("SETTINGS_MODULE", "settings") 可以不写，这个是默认值

receivers = ['somexxxx@163.com','8976xxxxx@qq.com']
# 使用方法同 Django

## 发送普通邮件
send_mail(
    subject="邮件主题",
    message="邮件内容",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=receivers,
)

## 发送 html 邮件

send_mail(
    subject="邮件主题",
    message="邮件内容",
    html_message= '''<h1>邮件内容</h1>
<h2>副标题</h2>
<p>段落</p>''',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=receivers,
)

## 一次发送不同的邮件
message1 = ('Subject here', 'Here is the message', settings.DEFAULT_FROM_EMAIL,receivers,)
message2 = ('Another Subject', 'Here is another message', settings.DEFAULT_FROM_EMAIL,receivers,)
send_mass_mail((message1, message2), fail_silently=False)

