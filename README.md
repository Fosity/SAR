# SAR
简单实现堡垒机

client-sar
  实现从host主机中获取实时CPU、memory状态数据。
  调试阶段 配置文件中DEUG 为True。
  实际运行 时请把DEUG调为False。
service-sar
  1.提供api，从client端接受数据。
  2.api采用验证功能："md5(key|time)|time"的方式进行验证，并且维护一个全局列表，防止盗取密码登录
  3.client接受数据，保留时间默认10分钟。
  4.基于flot-charts，生成动态状态图
  5.参考Paramiko https://github.com/paramiko/paramiko/blob/master/demos/interactive.py 在与主机连接时，添加操作记录。实现
  6.实现任务处理功能：前端提交任务，服务器接受任务，再通过
