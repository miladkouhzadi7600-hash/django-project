from django.http import HttpResponse


def home(request):
    return HttpResponse('سلام! به صفحه اصلی پروژه جنگو خوش آمدید.')
