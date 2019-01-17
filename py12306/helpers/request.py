# -*- coding=utf-8 -*-
from requests.exceptions import *

from py12306.helpers.func import *
from requests_html import HTMLSession, HTMLResponse


class Request(HTMLSession):
    """
    请求处理类
    """
    # session = {}

    # def __init__(self, mock_browser=True, session=None):
    # super().__init__(mock_browser=mock_browser)
    # self.session = session if session else HTMLSession()
    pass

    def save_to_file(self, url, path):
        response = self.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return response

    @staticmethod
    def _handle_response(response, **kwargs) -> HTMLResponse:
        """
        扩充 response
        :param response:
        :param kwargs:
        :return:
        """
        response = HTMLSession._handle_response(response, **kwargs)
        expand_class(response, 'json', Request.json)
        return response

    def json(self, default={}):
        """
        重写 json 方法，拦截错误
        :return:
        """
        from py12306.app import Dict
        try:
            result = self.old_json()
            return Dict(result)
        except:
            return Dict(default)

    def request(self, *args, **kwargs):  # 拦截所有错误
        try:
            return super().request(*args, **kwargs)
        except RequestException as e:
            if e.response:
                response = e.response
            else:
                response = HTMLResponse(HTMLSession)
                response.status_code = 500
                expand_class(response, 'json', Request.json)
            return response
