
# djangomail

[![Build Status](https://travis-ci.com/somenzz/djangomail.svg?branch=master)](https://travis-ci.com/somenzz/djangomail)

将 mail 模块从 Django 中独立出来，做为 Python 发邮件的独立的库，就是 djangomail，使用起来比 smtplib 要方便很多。


## 安装

```shell
pip install djangomail
```


### 配置

发邮件要用户名密码和邮件服务器，对吧，直接写在配置文件里。在我们的程序的目录中，新建 settings.py 

写入以下信息：

```python
EMAIL_USE_LOCALTIME = True
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com' #可以换其他邮箱，注意修改确认端口
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your-username'
EMAIL_HOST_PASSWORD = '********'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### 发送普通文本邮件

只需要导入 send_mail,send_mass_mail，设置下环境变量 `DJANGO_SETTINGS_MODULE`， 这是 Django 读取自定义配置文件的内容所需要的。

示例代码如下：

```python
from djangomail import send_mail,send_mass_mail
import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

receivers = ['somenzz@163.com']

send_mail(
    subject="如何使用 django mail",
    message="djangomail 发送邮件从未如此简单，来自 「Python七号」",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=receivers
)
```

查看下邮箱：

![](https://tva1.sinaimg.cn/large/008i3skNgy1grd95qcxldj30sc0dsglv.jpg)


还可以一次发送不同的邮件给不同的人：

```python
datatuple = (
    ('Subject', 'Message.', 'from@example.com', ['john@example.com']),
    ('Subject', 'Message.', 'from@example.com', ['jane@example.com']),
)
send_mass_mail(datatuple)
```


### 发送带附件的邮件

发送附件需要使用 EmailMessage 类，其实常用的 send_mail,send_mass_mail 函数只对 EmailMessage 少数成员函数的封装。也就是说发送附件，我们需要创建 EmailMessage 对象。

示例代码如下：

```python
from djangomail import EmailMessage

import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

receivers = ['somenzz@163.com']

email = EmailMessage(
    subject='如何使用 djangomail 发送附件',
    body='这里有附件',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to = receivers,
    reply_to=['897665600@qq.com']
)
email.attach_file("/Users/aaron/Documents/python-seven.jpg", mimetype="image/jpeg")
email.attach_file("./settings.py")
email.send()

```

检查下邮箱：

![](https://tva1.sinaimg.cn/large/008i3skNgy1grda7uakxij30vw0i874m.jpg)


### 发送多彩的 html 邮件

html 可以显示丰富多彩的内容，这里以发送一个含图片的 html 为例。

需要用到标准库里的 email 模块，添加图片信息，示例代码如下：

```python
from djangomail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


subject = 'djangomail 发送带图片的 html 邮件'

body_html = '''
<html>
    <body>
    <p>「Python七号」每周分享一个小技巧 </p>
        <img src="cid:qrcode.jpg" />
    </body>
</html>
'''


msg = EmailMultiAlternatives(
    subject,
    body_html,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=['somenzz@163.com']
)

msg.mixed_subtype = 'related'
msg.attach_alternative(body_html, "text/html")
img_dir = 'images/'
image = 'qrcode.jpg'
file_path = os.path.join(img_dir, image)
with open(file_path, 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<{name}>'.format(name=image))
    img.add_header('Content-Disposition', 'inline', filename=image)
msg.attach(img)

msg.send()
```

检查下邮箱，发现图片直接显示在了邮件内容中：

![](https://tva1.sinaimg.cn/large/008i3skNgy1grdb1hawpyj31d60s8dhw.jpg)


### 扩展

其实不止发送邮件，通过实现自己的 Backend，就可以将消息发送到任何平台。

django 自己的 global_settings 其实已经有以下配置：

```python
EMAIL_BACKEND = 'djangomail.mail.backends.smtp.EmailBackend'
```

只要我们按照 EmailBackend 的格式编写自己的 Backend 就可以实现自定义的消息发送，比如说发送到微信。

然后修改 settings.py 文件，将 EMAIL_BACKEND 配置为自己的 Backend 即可。 

EmailBackend 继承自类 BaseEmailBackend，假如我们编写自己的 MyBackend，只需要继承 BaseEmailBackend 实现它的 send_messages 方法即可：

```python
def send_messages(self, email_messages):
    """
    Send one or more EmailMessage objects and return the number of email
    messages sent.
    """
    raise NotImplementedError(
        "subclasses of BaseEmailBackend must override send_messages() method"
    )
```

有个 [server酱](https://mp.weixin.qq.com/s/ibBaPbMg202XMEaG-zifVA) 可以发送到微信，你可以自己扩展下，我这里就不展开了。


### 报错自动发送邮件

当某个函数报错，也就是抛出异常时，如果发送异常相关的堆栈信息邮件给运维人员，则可以大大提升处理效率。

当然了，可以指定某些异常，只有抛出这类异常时才发邮件，也可以将不同的异常发给不同的人。

这里我已经做好了一个装饰器：somedecorators

##### 安装

```sh
pip install somedecorators
```

##### 使用

```python
from somedecorators import email_on_exception
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

@email_on_exception(['somenzz@163.com'])
def myfunc():
    1/0

myfunc()
```

检查一下邮箱：

![](https://tva1.sinaimg.cn/large/008i3skNgy1grdbaqr7ooj31e60n43zx.jpg)

##### 监控指定的异常

```python

from somedecorators import email_on_exception
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class Exception1(Exception):
    pass

class Exception2(Exception):
    pass

class Exception3(Exception):
    pass

@email_on_exception(['somenzz@163.com'],traced_exceptions = Exception2)
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3

myfunc(2)

```
上述代码只有在 raise Exception2 时才会发送邮件：

![](https://tva1.sinaimg.cn/large/008i3skNgy1grdbh8d2foj31de0l2myd.jpg)

##### 不同的异常发给不同的人


```python
@email_on_exception(['somenzz@163.com'],traced_exceptions = Exception2)
@email_on_exception(['others@163.com'],traced_exceptions = (Exception1, Exception3))
def myfunc(args):
    if args == 1:
        raise Exception1
    elif args == 2:
        raise Exception2
    else:
        raise Exception3
```

是不是非常方便？

##### 其他装饰器

**timeit**

耗时统计装饰器，单位是秒，保留 4 位小数

使用方法：

```python
from somedecorators import timeit
@timeit()
def test_timeit():
    time.sleep(1)

#test_timeit cost 1.0026 seconds

@timeit(logger = your_logger)
def test_timeit():
    time.sleep(1)
```

**retry**

重试装饰器。

当被装饰的函数调用抛出指定的异常时，函数会被重新调用。

直到达到指定的最大调用次数才重新抛出指定的异常，可以指定时间间隔，默认 5 秒后重试。

traced_exceptions 为监控的异常，可以为 None（默认）、异常类、或者一个异常类的列表或元组 tuple。

traced_exceptions 如果为 None，则监控所有的异常；如果指定了异常类，则若函数调用抛出指定的异常时，重新调用函数，直至成功返回结果。

未出现监控的异常时，如果指定定了 reraised_exception 则抛出 reraised_exception，否则抛出原来的异常。

```python
from somedecorators import retry 

@retry(
    times=2,
    wait_seconds=1,
    traced_exceptions=myException,
    reraised_exception=CustomException,
)
def test_retry():
    # time.sleep(1)
    raise myException


test_retry()
```

### 其他实用三方库

- [dbinterface](https://github.com/somenzz/dbinterface): 数据库统一读、写、导出文件接口，适用于数据仓库等多数据库系统应用。支持 db2、mysql，postgres。

- [transferfile](https://github.com/somenzz/transferfile): 文件上传、下载接口，适用于文件分发系统。支持 ftp、sftp、scp、rsync。


### 联系我

公众号「Python七号」

微信号「somenzz」
