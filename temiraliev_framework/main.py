from quopri import decodestring
from temiraliev_framework.framework_requests import GetReq, PostReq


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostReq().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Входящий POST-запрос: {Framework.decode_value(data)}')

        if method == 'GET':
            request_params = GetReq().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Входящие GET-параметры:'
                  f' {Framework.decode_value(request_params)}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        decode_data = {}
        for key_data, value_data in data.items():
            ref_value = bytes(value_data.replace('%', '=').replace("+", " "), 'UTF-8')
            decode_str_value = decodestring(ref_value).decode('UTF-8')
            decode_data[key_data] = decode_str_value
        return decode_data
