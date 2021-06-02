
# djangomail

[![Build Status](https://travis-ci.com/somenzz/djangomail.svg?branch=master)](https://travis-ci.com/somenzz/djangomail)

将 mail 模块从 Django 中独立出来，做为 Python 发邮件的独立的库，就是 djangomail，使用起来比 smtplib 要方便很多。


## 安装

```shell
pip install djangomail
```

## 使用

在项目目录新建 setting.py，内容如下：

```python

# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = True

EMAIL_BACKEND = 'djangomail.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com' #可以换其他邮箱
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your-username'
EMAIL_HOST_PASSWORD = '********'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


```

然后就可以愉快的发邮件了：

```python
from djangomail import send_mail,send_mass_mail
import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

receivers = ['somexxxx@163.com','8976xxxxx@qq.com']

# 使用方法同 Django

## 发送普通邮件
send_mail(
    subject="邮件主题",
    message="邮件内容",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=receivers
)

## 发送 html 邮件

send_mail(
    subject="邮件主题",
    message="邮件内容",
    html_message= '''<h1>邮件内容</h1>
<h2>副标题</h2>
<p>段落</p>''',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=receivers
)

## 一次发送不同的邮件
message1 = ('Subject here', 'Here is the message', settings.DEFAULT_FROM_EMAIL,receivers)
message2 = ('Another Subject', 'Here is another message', settings.DEFAULT_FROM_EMAIL,receivers)
send_mass_mail((message1, message2), fail_silently=False)



```

## 相关的装饰器

当某个函数抛出指定的异常时，发送异常相关的堆栈信息邮件给运维人员，可以大大提升处理效率。

这里有一个非常好用的装饰器 [`email_on_exception`](https://github.com/somenzz/somedecorators#email_on_exception)

使用方法：

```python
from somedecorators import email_on_exception 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

@email_on_exception(['somenzz@163.com'])
def myfunc():
    1/0

myfunc()
```
