from datetime import date
from views import Index, About, Contacts, TherapyCourseList, TherapyPrograms, \
    CategoryList, CreateCategory, CreateCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/therapy-programs/': TherapyPrograms(),
    '/therapy-course-list/': TherapyCourseList(),
    '/category-list/': CategoryList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
}
