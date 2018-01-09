from django.shortcuts import render

# Create your views here.


def index(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request,'king_admin/table_index.html')

    elif request.method == "POST":
        pass

    else:
        pass