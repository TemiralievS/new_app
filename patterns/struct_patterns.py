from time import time


class AppRouter:
    """декоратор для добавления связки url-view"""
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """декоратор выводит в терминал название функции и время ее выполнения"""
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):

        def functime(method):

            def timefunc(*args, **kwargs):
                time_before = time()
                func = method(*args, **kwargs)
                time_after = time()
                spend_time = time_after - time_before

                print(f'debug: метод {self.name} отработал за {spend_time:2.2f} мс')
                return func

            return timefunc

        return functime(cls)
