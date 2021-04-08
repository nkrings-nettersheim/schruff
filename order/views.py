import datetime
#from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from .forms import ProductsForm, CustomerForm
from .models import Order_days, Order_times, Order, Content_text


def index(request):
    return render(request, 'order/index.html', )


def impressum(request):
    content = Content_text.objects.get(content_kurz='Impressum')
    return render(request, 'order/impressum.html', {'content': content})


def datenschutz(request):
    content = Content_text.objects.get(content_kurz='Datenschutz')
    return render(request, 'order/datenschutz.html',  {'content': content})


def collectiondate(request):
    p = request.GET['p']
    order_days = ''
    time_now = datetime.datetime.now().strftime('%H')
    if p == '10':
        product_long = 'Reibekuchen'
        if int(time_now) < settings.LOT_REIBEKUCHEN:
            order_days = Order_days.objects.filter(reibekuchen=True, order_day__gte=datetime.datetime.now()).order_by('order_day')[:3]
        else:
            order_days = Order_days.objects.filter(reibekuchen=True, order_day__gt=datetime.datetime.now()).order_by(
                'order_day')[:3]

    elif p == '20':
        product_long = 'Spießbratenbrötchen'
        if int(time_now) < settings.LOT_SPIESSBRATEN:
            order_days = Order_days.objects.filter(spiessbraten=True, order_day__gte=datetime.datetime.now()).order_by('order_day')[:3]
        else:
            order_days = Order_days.objects.filter(spiessbraten=True, order_day__gt=datetime.datetime.now()).order_by('order_day')[:3]

    else:
        return render(request, 'order/index.html')

    request.session['product_id'] = p
    request.session['product_long'] = product_long

    return render(request, 'order/collectiondate.html', {'order': request.session, 'days': order_days})

def product(request):
    if request.session['product_id']:

        if request.method == "POST":
            day = request.POST['bestelltag']
            request.session['order_day'] = day
            day = request.session['order_day']
            day_list = day.split('-')
            day_string = day_list[2] + "." + day_list[1] + "." + day_list[0]
            request.session['order_day_view'] = day_string
            request.session['EUR_REIBEKUCHEN'] = settings.EUR_REIBEKUCHEN
            request.session['EUR_APFELKOMPOTT'] = settings.EUR_APFELKOMPOTT
            request.session['EUR_LACHS'] = settings.EUR_LACHS
            request.session['EUR_SPIESSBRATEN_STANDARD'] = settings.EUR_SPIESSBRATEN_STANDARD
            request.session['EUR_SPIESSBRATEN_SPECIAL'] = settings.EUR_SPIESSBRATEN_SPECIAL
            request.session['EUR_KARTOFFELSALAT'] = settings.EUR_KARTOFFELSALAT
            form = ProductsForm()
            return render(request, 'order/product.html', {'form': form, 'order': request.session})
        else:
            return render(request, 'order/index.html')
    else:
        return render(request, 'order/index.html')


def collectiontime(request):
    if request.session['product_id']:
        if request.method == "POST":
            if request.session['product_id'] == '10':
                request.session['reibekuchen_count'] = request.POST['reibekuchen_count']
                request.session['apfelkompott_count'] = request.POST['apfelkompott_count']
                request.session['lachs_count'] = request.POST['lachs_count']
                request.session['wishes'] = request.POST['wishes']
                order_day = request.session['order_day'].split("-")
                collectiontime_list = Order_times.objects.filter(order_time__date=datetime.date(int(order_day[0]), int(order_day[1]), int(order_day[2])), booked=False)
                return render(request, 'order/collectiontime.html', {'order': request.session, 'times': collectiontime_list})

            elif request.session['product_id'] == '20':
                request.session['broetchen_standard_count'] = request.POST['broetchen_standard_count']
                request.session['broetchen_special_count'] = request.POST['broetchen_special_count']
                request.session['kartoffelsalat_count'] = request.POST['kartoffelsalat_count']
                request.session['wishes'] = request.POST['wishes']
                order_day = request.session['order_day'].split("-")
                collectiontime_list = Order_times.objects.filter(order_time__date=datetime.date(int(order_day[0]), int(order_day[1]), int(order_day[2])), booked=False)
                return render(request, 'order/collectiontime.html', {'order': request.session, 'times': collectiontime_list})

            else:
                return render(request, 'order/index.html')
        else:
            return render(request, 'order/index.html')
    else:
        return render(request, 'order/index.html')


def customer(request):
    if request.session['product_id']:
        if request.method == "POST":
            request.session['collectiontime'] = request.POST['collectiontime']

            #collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')
            form = CustomerForm()
            return render(request, 'order/customer.html', {'form': form, 'order': request.session})
        else:
            return render(request, 'order/index.html')
    else:
        return render(request, 'order/index.html')


def complete(request):
    if request.session['product_id']:
        if request.method == "POST":
            request.session['customer_name'] = request.POST['customer_name']
            request.session['callnumber'] = request.POST['callnumber']
            request.session['email'] = request.POST['email']
            collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')
            #to charge the price
            price = 0.0
            if ('reibekuchen_count' in request.session):
                price = price + int(request.session['reibekuchen_count']) * float(request.session['EUR_REIBEKUCHEN'])
            if ('apfelkompott_count' in request.session):
                price = price + int(request.session['apfelkompott_count']) * float(request.session['EUR_APFELKOMPOTT'])
            if ('lachs_count' in request.session):
                price = price + int(request.session['lachs_count']) * float(request.session['EUR_LACHS'])
            if ('broetchen_standard_count' in request.session):
                price = price + int(request.session['broetchen_standard_count']) * float(request.session['EUR_SPIESSBRATEN_STANDARD'])
            if ('broetchen_special_count' in request.session):
                price = price + int(request.session['broetchen_special_count']) * float(request.session['EUR_SPIESSBRATEN_SPECIAL'])
            if ('kartoffelsalat_count' in request.session):
                price = price + int(request.session['kartoffelsalat_count']) * float(request.session['EUR_KARTOFFELSALAT'])

            request.session['price'] = price
            return render(request, 'order/complete.html', {'order': request.session, 'collectiontime_view': collectiontime_view})
        else:
            return render(request, 'order/index.html')
    else:
        return render(request, 'order/index.html')


def thanks(request):
    if request.session['product_id']:
        if request.method == "POST":
            mail_content_seller = ""
            mail_content_customer = ""

            if request.session['product_id'] == '10':

                mail_content_seller = (f"Hallo,\n\n \
Hier ist die Bestellung für {request.session['customer_name']}. Er möchte:\n\n \
Anzahl Reibekuchen : {request.session['reibekuchen_count']}\n \
Anzahl Apfelkompott: {request.session['apfelkompott_count']}\n \
Anzahl Lachs       : {request.session['lachs_count']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Gruß Dein Bestelltool")

                mail_content_customer = (f"Hallo,\n\n \
Hier die Infos zu Deiner Bestellung bei der Gaststätte Schruff:\n\n \
Anzahl Reibekuchen : {request.session['reibekuchen_count']}\n \
Anzahl Apfelkompott: {request.session['apfelkompott_count']}\n \
Anzahl Lachs       : {request.session['lachs_count']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Bezahlt wird vor Ort an der Theke!\n\n \
Vielen Dank für Deine Bestellung!!!\n\n \
Gruß Dein Bestelltool")

                order_long_string = (f"Reibekuchen:{request.session['reibekuchen_count']};"
                                     f"Apfelkompott:{request.session['apfelkompott_count']};"
                                     f"Lachs:{request.session['lachs_count']};"
                                     f"Wünsche:{request.session['wishes']};"
                                     )

            elif request.session['product_id'] == '20':

                mail_content_seller = (f"Hallo,\n\n \
Hier ist die Bestellung für {request.session['customer_name']}. Er möchte:\n\n \
Spießbratenbrötchen (Standard) : {request.session['broetchen_standard_count']}\n \
Spießbratenbrötchen (Spezial) : {request.session['broetchen_special_count']}\n \
Anzahl Kartoffelsalat: {request.session['kartoffelsalat_count']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Gruß Dein Bestelltool")

                mail_content_customer = (f"Hallo,\n\n \
Hier die Infos zu Deiner Bestellung bei der Gaststätte Schruff:\n\n \
Spießbratenbrötchen (Standard) : {request.session['broetchen_standard_count']}\n \
Spießbratenbrötchen (Spezial) : {request.session['broetchen_special_count']}\n \
Anzahl Kartoffelsalat: {request.session['kartoffelsalat_count']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Bezahlt wird vor Ort an der Theke!\n\n \
Vielen Dank für Deine Bestellung!!!\n\n \
Gruß Dein Bestelltool")

                order_long_string = (f"Spießbraten (Standard):{request.session['broetchen_standard_count']};"
                                     f"Spießbraten (Spezial):{request.session['broetchen_special_count']};"
                                     f"Kartoffelsalat:{request.session['kartoffelsalat_count']};"
                                     f"Wünsche:{request.session['wishes']};"
                                     )

            else:
                pass

            send_mail(
                'Bestellung',
                mail_content_seller,
                settings.EMAIL_FROM,
                [settings.EMAIL_TO_SELLER],
                fail_silently=False,
            )

            send_mail(
                'Bestellung bei der Gaststätte Schruff',
                mail_content_customer,
                settings.EMAIL_FROM,
                [request.session['email']],
                fail_silently=False,
            )


            #save everything in the database
            order = Order(name=request.session['customer_name'],
                          callnumber=request.session['customer_name'],
                          email=request.session['email'],
                          order_day=request.session['order_day'],
                          order_time=request.session['collectiontime'],
                          order_long=order_long_string,
                          wishes=request.session['email']
                          )

            order.save()

            #booked time setzen
            ct = get_object_or_404(Order_times, order_time=request.session['collectiontime'])
            ct.booked = True
            ct.save(update_fields=['booked'])

            collectiontime_view = datetime.datetime.strptime(request.session['collectiontime'], '%Y-%m-%d %H:%M:%S')

    #!!! Attention !!! the next line must be uncomment
            request.session['product_id'] = ""


            return render(request, 'order/thanks.html', {'collectiontime_view': collectiontime_view})
        else:
            return render(request, 'order/index.html')
    else:
        return render(request, 'order/index.html')



