class GetReq:

    @staticmethod
    def parsing_input_data(data: str):
        data_dict = {}
        if data:
            data_list = data.split('&')
            for elem in data_list:
                data_key, data_value = elem.split('=')
                data_dict[data_key] = data_value
        return data_dict

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetReq.parsing_input_data(query_string)
        return request_params


class PostReq:

    @staticmethod
    def parsing_input_data(data: str):
        data_dict = {}
        if data:
            data_list = data.split('&')
            for elem in data_list:
                data_key, data_value = elem.split('=')
                data_dict[data_key] = data_value
        return data_dict

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0

        data = env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    def parsing_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parsing_input_data(data_str)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parsing_wsgi_input_data(data)
        return data
