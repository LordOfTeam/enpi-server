import datetime

from flask_restful import Resource
from flask_mail import Message
from flask import current_app

from enpi_srv.controllers.parsers import ApplyTicketFormParser
from enpi_srv import mail


class MailApplyFormContentMixin(object):

    def get_content(self, **kwargs):
        text = '''
        Hi All,
           活动时间：{0}
           预算：   {1}元
           人数:    {2}人
           场地面积: {3}平米
           城市区域: {4}
           行政区：  {5}
           姓名:    {6}
           电话:    {7}   
        Best Regards
        上海恩湃广告
        '''.format(
            kwargs.get('start_dt'),
            kwargs.get('budget'),
            kwargs.get('people'),
            kwargs.get('area'),
            kwargs.get('city'),
            kwargs.get('city_area'),
            kwargs.get('cn_name'),
            kwargs.get('phone')
        )
        return text

    def get_subject(self):
        dt_str = datetime.datetime.now().strftime('%Y-%m-%d')
        return "[发布需求]您有新的发布需求，请查收{}".format(dt_str)


class TicketFormView(
    MailApplyFormContentMixin,
    ApplyTicketFormParser,
    Resource):
    """
    POST http://127.0.0.1:5000/core/apply apply_json:='{'start_dt':'2019-3-27', 'budget':200000, 'people':20, 'area':'上海市', 'city_area':'虹口区', 'cn_name':'顾鲍尔', 'phone':13999999999}'
    {
    'start_dt':xxx    # 活动时间
    'budget':xxx      # 预算
    'people':xxx      # 人数
    'area':xx         # 场地面积
    'city':xxx        # 城市区域
    'city_area':xx    # 行政区
    'cn_name':xx      # 姓名
    'phone':xxx       # 电话
    """

    def post(self):
        request_data = self.post_ticket_form.parse_args()
        apply_json = request_data.get('apply_json')
        msg = Message(
            body=self.get_content(**apply_json),
            recipients=current_app.config['MAIL_RECIPIENTS'],
            subject=self.get_subject()
        )
        mail.send(msg)
        return apply_json


class SMSSecurityCode(Resource):
    def get(self):
        return {'status': 'ok'}
