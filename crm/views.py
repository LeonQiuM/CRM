from django.shortcuts import render


# Create your views here.

def index(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, 'index.html')

    elif request.method == "POST":
        pass

    else:
        pass


def customer_list(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request,'sales/customers.html')

    elif request.method == "POST":
        pass

    else:
        pass