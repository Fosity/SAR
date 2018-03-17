# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email_test_smt_163.send_mail_163.config123 import mailto_list,mail_host,mail_pass,mail_postfix,mail_user


class Sendmail(object):
    def __init__(self, ):
        self.me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
        self.msg = MIMEMultipart()  # 创建对象
        self.msg['From'] = self.me
        self.mail_to_list=set(mailto_list)
        self.msg['To'] = ";".join(self.mail_to_list)  # 将收件人列表以‘；’分隔
        self.connect()

    def connect(self):
        self.server = smtplib.SMTP_SSL(mail_host,465)
        # self.server.connect(mail_host)  # 连接服务器
        self.server.login(mail_user, mail_pass)  # 登录操作

    def attach_text(self, header, content):
        self.msg['Subject'] = header
        self.content = content
        self.msg.attach(MIMEText(self.content, _subtype='plain'))  # 把内容加入对象中

    def attach_attachment(self, up_path, file_type):
        filename = up_path.rsplit('\\', maxsplit=1)[1]
        file_extensions = up_path.rsplit('.', maxsplit=1)[1]
        print(filename,file_extensions)
        with open(up_path, 'rb') as f:
            mime = MIMEBase(file_type, file_extensions, filename=filename)
            # 加上必要的头信息
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')

            # 把附件的内容读出来
            mime.set_payload(f.read())
            encode_base64(mime)
            self.msg.attach(mime)

    def send(self):
        try:
            self.server.sendmail(self.me, self.mail_to_list, self.msg.as_string())
        except Exception as e:
            print(str(e))
            return False

header = '关于今年年终奖的事情'
content = """
    关于今年年终奖的事情,本公司决定于。
"""
up_path = r'F:\test\python_test\email_test_smt_163\shou.png'
file_type = 'image'
send_email=Sendmail()
send_email.attach_text(header,content)
send_email.attach_attachment(up_path,file_type)
send_email.send()