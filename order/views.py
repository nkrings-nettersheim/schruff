import datetime
#from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from .models import Order_days, Order_times


def index(request):
    return render(request, 'order/index.html', )


def impressum(request):
    return render(request, 'order/impressum.html', )


def datenschutz(request):
    return render(request, 'order/datenschutz.html', )


def step1(request):
    p = request.GET['p']
    order_days = ''
    if p == '10':
        product_long = 'Reibekuchen'
        order_days = Order_days.objects.filter(reibekuchen=True, order_day__gt=datetime.datetime.now()).order_by('order_day')
    elif p == '20':
        product_long = 'Spießbratenbrötchen'
        order_days = Order_days.objects.filter(spiessbraten=True, order_day__gt=datetime.datetime.now()).order_by('order_day')
    else:
        product_long = 'unbekannt'

    request.session['product_id'] = p
    request.session['product_long'] = product_long

    return render(request, 'order/step1.html', {'order': request.session, 'days': order_days})

def step2(request):
    day = request.POST['bestelltag']
    request.session['order_day'] = day
    day = request.session['order_day']
    day_list = day.split('-')
    day_string = day_list[2] + "." + day_list[1] + "." + day_list[0]
    request.session['order_day_view'] = day_string
    return render(request, 'order/product.html', {'order': request.session})


def collectiontime(request):
    if request.method == "POST":
        if request.session['product_id'] == '10':
            request.session['reibekuchen_count'] = request.POST['reibekuchen_count']
            request.session['apfelkompott'] = request.POST['apfelkompott']
            request.session['lachs'] = request.POST['lachs']
            request.session['bemerkung'] = request.POST['bemerkung']
            order_day = request.session['order_day'].split("-")
            collectiontime_list = Order_times.objects.filter(order_time__date=datetime.date(int(order_day[0]), int(order_day[1]), int(order_day[2])), booked=False)
            return render(request, 'order/collectiontime.html', {'order': request.session, 'times': collectiontime_list})

        elif request.session['product_id'] == '20':
            request.session['broetchen_standard'] = request.POST['broetchen_standard']
            request.session['broetchen_special'] = request.POST['broetchen_special']
            request.session['apfelkompott'] = request.POST['apfelkompott']
            request.session['bemerkung'] = request.POST['bemerkung']
            collectiontime_list = Order_times.objects.filter(booked=False)
            return render(request, 'order/collectiontime.html', {'order': request.session, 'times': collectiontime_list})

        else:
            pass
    else:
        pass


def customer(request):
    if request.method == "POST":
        request.session['collectiontime'] = request.POST['collectiontime']
        #request.session['collectiontime_vi'])
        collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')

        #print(type(request.session['collectiontime']))
        return render(request, 'order/customer.html', {'order': request.session})
    else:
        pass


def complete(request):
    if request.method == "POST":
        request.session['customer_name'] = request.POST['customer_name']
        request.session['callnumber'] = request.POST['callnumber']
        request.session['email'] = request.POST['email']
        print(request.session['collectiontime'])
        collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')
        print(type(collectiontime_view))
        return render(request, 'order/complete.html', {'order': request.session, 'collectiontime_view': collectiontime_view})
    else:
        pass


def thanks(request):
    if request.method == "POST":
        #sending an email to the customer
        #sending an email to the sales part
        #save everything in the database
        #session schließen
        collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')
        return render(request, 'order/thanks.html', {'order': request.session, 'collectiontime_view': collectiontime_view})
    else:
        pass



