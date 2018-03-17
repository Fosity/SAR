# -*- coding: utf-8 -*-  
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

######################### 配 置 #########################
mailto_list = ['fosity44686011@163.com']  # 收件人(列表)
mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user = "fosity44686011@163.com"  # 用户名
mail_pass = "xupan446860117"  # 密码
mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com


################## 发送 文本内容 ##################
# def send_mail(to_list, sub, content):
#     me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
#     msg = MIMEText(content, _subtype='plain')
#     msg['Subject'] = sub
#     msg['From'] = me
#     msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
#     try:
#         server = smtplib.SMTP()
#         server.connect(mail_host)  # 连接服务器
#         server.login(mail_user, mail_pass)  # 登录操作
#         server.sendmail(me, to_list, msg.as_string())
#         server.close()
#         return True
#     except Exception as e:
#         print(str(e))
#         return False
#
#
# header = '关于今年年终奖的事情'
# content = """
#     关于今年年终奖的事情,本公司决定于。
# """
# for i in range(1):  # 发送1封，上面的列表是几个人，这个就填几
#     if send_mail(mailto_list, header, content):  # 邮件主题和邮件内容
#         # 这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
#         print("done!")
#     else:
#         print("failed!")


############# 发送 附件 #######################
def send_mail(to_list, sub, content, up_path, file_type):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEMultipart()  # 创建对象
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔

    msg.attach(MIMEText(content, _subtype='plain'))  # 把内容加入对象中
    filename = up_path.rsplit('\\', maxsplit=1)[1]
    file_extensions = up_path.rsplit('.', maxsplit=1)[1]
    print(file_extensions,filename)
    with open(up_path, 'rb') as f:
        mime = MIMEBase(file_type, file_extensions, filename=filename)
        # 加上必要的头信息
        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')

        # 把附件的内容读出来
        mime.set_payload(f.read())
        encode_base64(mime)
        msg.attach(mime)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


header = '关于今年年终奖的事情'
content = """
    关于今年年终奖的事情,本公司决定于。
"""
up_path = r'F:\test\python_test\email_test_smt_163\shou.png'
file_type = 'image'
for i in range(1):  # 发送1封，上面的列表是几个人，这个就填几
    if send_mail(mailto_list, header, content, up_path, file_type):  # 邮件主题和邮件内容
        # 这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
        print("done!")
    else:
        print("failed!")
