import logging
import os
import datetime
#from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from .forms import ProductsForm, CustomerForm
from .models import Order_days, Order_times, Order, Content_text

BASE_DIR = settings.BASE_DIR

logger = logging.getLogger(__name__)


def index(request):
    if 'priduct_id' in request.session:
        del request.session['product_id']
    if 'product_long' in request.session:
        del request.session['product_long']
    if 'reibekuchen_count' in request.session:
        del request.session['reibekuchen_count']
    if 'apfelkompott_count' in request.session:
        del request.session['apfelkompott_count']
    if 'lachs_count' in request.session:
        del request.session['lachs_count']
    if 'wishes' in request.session:
        del request.session['wishes']
    if 'broetchen_standard_count' in request.session:
        del request.session['broetchen_standard_count']
    if 'broetchen_special_count' in request.session:
        del request.session['broetchen_special_count']
    if 'kartoffelsalat_count' in request.session:
        del request.session['kartoffelsalat_count']
    if 'customer_name' in request.session:
        del request.session['customer_name']
    if 'callnumber' in request.session:
        del request.session['callnumber']
    if 'email' in request.session:
        del request.session['email']

    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf index.html")
    return render(request, 'order/index.html', )


def impressum(request):
    content = Content_text.objects.get(content_kurz='Impressum')
    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf impressum.html")
    return render(request, 'order/impressum.html', {'content': content})


def datenschutz(request):
    content = Content_text.objects.get(content_kurz='Datenschutz')
    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf datenschutz.html")
    return render(request, 'order/datenschutz.html',  {'content': content})


def collectiondate(request):
    p = request.GET['p']
    order_days = ''
    time_now = datetime.datetime.now().strftime('%H')
    if p == '10':
        product_long = 'Reibekuchen'
        logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Bestellseite Reibekuchen aufgerufen")
        if int(time_now) < settings.LOT_REIBEKUCHEN:
            order_days = Order_days.objects.filter(reibekuchen=True, order_day__gte=datetime.datetime.now()).order_by('order_day')[:2]
        else:
            order_days = Order_days.objects.filter(reibekuchen=True, order_day__gt=datetime.datetime.now()).order_by('order_day')[:2]

    elif p == '20':
        product_long = 'Spießbratenbrötchen'
        logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Bestellseite Spießbratenbrötchen aufgerufen")
        if int(time_now) < settings.LOT_SPIESSBRATEN:
            order_days = Order_days.objects.filter(spiessbraten=True, order_day__gte=datetime.datetime.now()).order_by('order_day')[:2]
        else:
            order_days = Order_days.objects.filter(spiessbraten=True, order_day__gt=datetime.datetime.now()).order_by('order_day')[:2]

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
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Produktbestellseite aufgerufen")
            return render(request, 'order/product.html', {'form': form, 'order': request.session})
        else:
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; Aufruf product Seite mit GET")
            return render(request, 'order/index.html')
    else:
        logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; Aufruf product Seite ohne product_id")
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
                collectiontime_list = Order_times.objects.filter(order_time__date=datetime.date(int(order_day[0]), int(order_day[1]), int(order_day[2])), booked=False).order_by('order_time')
                logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; R: {request.session['reibekuchen_count']};"
                            f"A: {request.session['apfelkompott_count']};L: {request.session['lachs_count']}")
                return render(request, 'order/collectiontime.html', {'order': request.session, 'times': collectiontime_list})

            elif request.session['product_id'] == '20':
                request.session['broetchen_standard_count'] = request.POST['broetchen_standard_count']
                request.session['broetchen_special_count'] = request.POST['broetchen_special_count']
                request.session['kartoffelsalat_count'] = request.POST['kartoffelsalat_count']
                request.session['wishes'] = request.POST['wishes']
                order_day = request.session['order_day'].split("-")
                collectiontime_list = Order_times.objects.filter(order_time__date=datetime.date(int(order_day[0]), int(order_day[1]), int(order_day[2])), booked=False).order_by('order_time')
                logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; B: {request.session['broetchen_standard_count']};"
                            f"S: {request.session['broetchen_special_count']};"
                            f"K: {request.session['kartoffelsalat_count']}")
                return render(request, 'order/collectiontime.html', {'order': request.session,
                                                                     'times': collectiontime_list})

            else:
                logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf collectiontime Seite mit falscher product_id")
                return render(request, 'order/index.html')
        else:
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf collectiontime Seite mit GET")
            return render(request, 'order/index.html')
    else:
        logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf collectiontime Seite ohne product_id")
        return render(request, 'order/index.html')


def customer(request):
    if request.session['product_id']:
        if request.method == "POST":
            request.session['collectiontime'] = request.POST['collectiontime']
            form = CustomerForm()
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; "
                        f"Aufruf customer Seite mit {request.session['collectiontime']} als Abholzeit")
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
            #if ('reibekuchen_count' in request.session):
            if 'reibekuchen_count' in request.session and request.session['reibekuchen_count'] != '':
                    price = price + int(request.session['reibekuchen_count']) * float(request.session['EUR_REIBEKUCHEN'])
            if 'apfelkompott_count' in request.session and request.session['apfelkompott_count'] != '':
                price = price + int(request.session['apfelkompott_count']) * float(request.session['EUR_APFELKOMPOTT'])
            if 'lachs_count' in request.session and request.session['lachs_count'] != '':
                price = price + int(request.session['lachs_count']) * float(request.session['EUR_LACHS'])
            if 'broetchen_standard_count' in request.session and request.session['broetchen_standard_count'] != '':
                price = price + int(request.session['broetchen_standard_count']) * float(request.session['EUR_SPIESSBRATEN_STANDARD'])
            if 'broetchen_special_count' in request.session and request.session['broetchen_special_count'] != '':
                price = price + int(request.session['broetchen_special_count']) * float(request.session['EUR_SPIESSBRATEN_SPECIAL'])
            if 'kartoffelsalat_count' in request.session and request.session['kartoffelsalat_count'] != '':
                price = price + int(request.session['kartoffelsalat_count']) * float(request.session['EUR_KARTOFFELSALAT'])

            request.session['price'] = '%.2f' %round(price, 2)
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; "
                        f"Zusammenstellung für {request.session['customer_name']} zum Preis von {request.session['price']} €")

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
                logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; "
                            f"E-Mail versenden Reibekuchenbestellung für {request.session['customer_name']}")
                mail_content_seller = (f"Hallo,\n\n \
Hier ist die Bestellung für {request.session['customer_name']}. Er möchte:\n\n \
Portion mit Apfelkompott/Brot: {request.session['apfelkompott_count']}\n \
Portion mit Lachs/Brot       : {request.session['lachs_count']}\n \
Anzahl Einzel Reibekuchen    : {request.session['reibekuchen_count']}\n \
Preis (ohne weitere Wünsche) : {request.session['price']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Gruß Dein Bestelltool")

                mail_content_customer = (f"Hallo,\n\n \
Hier die Infos zu Deiner Bestellung bei der Gaststätte Schruff:\n\n \
Portion Reibekuchen (3 Stück) mit Apfelkompott und Brot       : {request.session['apfelkompott_count']}\n \
Portion Reibekuchen (3 Stück) mit Lachs/Meerrettich und Brot  : {request.session['lachs_count']}\n \
Anzahl Einzel Reibekuchen    : {request.session['reibekuchen_count']}\n \
Preis (ohne weitere Wünsche) : {request.session['price']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Bezahlt wird vor Ort an der Theke!\n\n \
Vielen Dank für Deine Bestellung!!!\n\n \
Gruß \nBrigitte")

                order_long_string = (f"Reibekuchen:{request.session['reibekuchen_count']};"
                                     f"Apfelkompott:{request.session['apfelkompott_count']};"
                                     f"Lachs:{request.session['lachs_count']};"
                                     f"Wünsche:{request.session['wishes']};"
                                     )

            elif request.session['product_id'] == '20':
                logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; "
                            f"E-Mail versenden Spießbratenbrötchen für {request.session['customer_name']}")
                mail_content_seller = (f"Hallo,\n\n \
Hier ist die Bestellung für {request.session['customer_name']}. Er möchte:\n\n \
Spießbratenbrötchen (Standard) : {request.session['broetchen_standard_count']}\n \
Spießbratenbrötchen (Spezial) : {request.session['broetchen_special_count']}\n \
Anzahl Kartoffelsalat: {request.session['kartoffelsalat_count']}\n \
Preis (ohne weitere Wünsche) : {request.session['price']}\n \
weitere Wünsche    : {request.session['wishes']}\n\n \
Rufnummer          : {request.session['callnumber']}\n \
E-Mail Adresse     : {request.session['email']}\n\n \
Abholtag           : {request.session['order_day_view']}\n \
Abholzeit          : {request.session['collectiontime']}\n\n \
Gruß Dein Bestelltool")

                mail_content_customer = (f"Hallo,\n\n \
Hier die Infos zu Deiner Bestellung bei der Gaststätte Schruff:\n\n \
Spießbratenbrötchen (Standard): {request.session['broetchen_standard_count']}\n \
Spießbratenbrötchen (Spezial) : {request.session['broetchen_special_count']}\n \
Anzahl Kartoffelsalat         : {request.session['kartoffelsalat_count']}\n \
Preis (ohne weitere Wünsche)  : {request.session['price']}\n \
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
                          callnumber=request.session['callnumber'],
                          email=request.session['email'],
                          order_day=request.session['order_day'],
                          order_time=request.session['collectiontime'],
                          order_long=order_long_string,
                          price=request.session['price'],
                          wishes=request.session['email'],
                          session=request.session.session_key,
                          session_time=datetime.datetime.now()
                          )

            order.save()
            logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; "
                        f"Daten in Datenbank für {request.session['customer_name']} gespeichert")

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



# **************************************************************************************************
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-23s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': BASE_DIR + '/order.log',
            'maxBytes': 1024*1024*1,
            'backupCount': 10,
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'order': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'django.security.*': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
})
