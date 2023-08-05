from datetime import date
from temiraliev_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.struct_patterns import AppRouter, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, CreateView,\
    BaseSerializer, ListView

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
routes = {}


@AppRouter(routes=routes, url='/')
class Index:
    """ главная страница с категориями """
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=site.categories)


@AppRouter(routes=routes, url='/about/')
class About:
    """ о проекте """

    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRouter(routes=routes, url='/therapy-programs/')
class TherapyPrograms:
    """ расписание """
    @Debug(name='TherapyPrograms')
    def __call__(self, request):
        return '200 OK', render('therapy-programs.html', date=date.today())


@AppRouter(routes=routes, url='/therapy-course-list/')
class TherapyCourseList:
    """ список курсов """
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('therapy-course-list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Курсы не добавлены'


@AppRouter(routes=routes, url='/create-course/')
class CreateCourse:
    """ создание курсов """
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('therapy-course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Курсы не добавлены'


@AppRouter(routes=routes, url='/create-category/')
class CreateCategory:
    """ создание категорий """
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')
            category = None

            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)

        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRouter(routes=routes, url='/category-list/')
class CategoryList:
    """ Список категорий """
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


@AppRouter(routes=routes, url='/copy-course/')
class CopyCourse:
    """Скопировать курс"""
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('therapy-course-list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'Курсы не добавлены'


@AppRouter(routes=routes, url='/client-list/')
class ClientListView(ListView):
    queryset = site.clients
    template_name = 'client-list.html'


@AppRouter(routes=routes, url='/create-client/')
class ClientCreateView(CreateView):
    template_name = 'create-client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('client', name)
        site.clients.append(new_obj)


@AppRouter(routes=routes, url='/add-client/')
class AddClientByCourseCreateView(CreateView):
    template_name = 'add-client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_client(client_name)
        course.add_client(client)


@AppRouter(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()


@AppRouter(routes=routes, url='/contacts/')
class Contacts:
    """ обратная связь """

    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
