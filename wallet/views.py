import json
import logging
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView


#from django.http import JsonResponse
from accounts.models import Churches
from wallet.models import Abatuye, Ikofi
from django.http import Http404, JsonResponse
from wallet.forms import AbatuyeForm, KubikuzaForm
from django.utils.text import slugify
from wallet.utils import processPayment, sendPayments, RESPONSE_CODES
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test


logger = logging.getLogger(__name__)

class ChurchesList(ListView):
    model = Churches
    template_name = 'wallet/churches.html'
    context_object_name = 'churches'

    def get_queryset(self):
        return Churches.objects.filter(groups__name__in=['churches'])
    


class HomePageView(TemplateView):
    template_name = "wallet/index.html"


class pendingPayment(TemplateView):
    template_name = 'wallet/pending.html'



class ContactUsView(TemplateView):
    template_name = "wallet/contact-us.html"


class sentmoney(TemplateView):
    template_name = 'wallet/sentmoney.html'


#church_slug must be a slug of a church u gave it when u was saving it 
def gutura(request, church_slug):

    #First thing first, deslugfy the Church_slug
    church_name = church_slug.replace('-', ' ')

    if request.method == 'POST':
        print("##########  Sent data: ",request.POST )
        form = AbatuyeForm(request.POST)
        
        if form.is_valid():
            
            print('########## Form is validated now: ', form.cleaned_data)

            #get cleaned
            phone_number = form.cleaned_data.get('phone_number')
            amount = form.cleaned_data.get('amount')
            
            #pending payment
            transaction = processPayment(phone_number, amount)

            #use isinstance(transaction, tuple), but test before moving to production
            if type(transaction) is tuple and transaction[0] == '1000':
                print('###### Transaction response code: ', transaction[0])
                print('###### Transaction request id: ', transaction[1])
                model_instance = form.save(commit=False)
                church = Churches.objects.get(slug=church_slug)
                
                model_instance.successful = False

                fees = int((abs(int(amount)) * 3)/100)

                model_instance.amount = abs(int(amount)) - fees
                model_instance.transaction_id = transaction[1] #get transaction id
                model_instance.to_church = church
                
                model_instance.save()
                return redirect(reverse('pendingPayment'))

            #GET the response code
            intouch_errors = RESPONSE_CODES.get(transaction)
            return render(request, 'wallet/sending-payment-error.html', {'cause':intouch_errors})
    
    else:
        form = AbatuyeForm()


        try:
            church = Churches.objects.get(slug=church_slug)
        except Churches.DoesNotExist:
            raise Http404("Church not Yet exist!")
    return render(request,'wallet/gutura-form.html', {'form':form, 'church':church_name})    

@csrf_exempt
def paymentcompletion(request):
    #Here the dummy data
    '''
    data = {
        'requesttransactionid':''4522233',
        'transactionid':'6004994884',
        'responsecode' :'01',
        'status':'Successfull',
        'statusdesc':'Successfully Processed Transaction',
        'referenceno':'312333883'
            }
    '''
    if request.method == 'POST':

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        response_code = body['jsonpayload']['responsecode']
        response_id = body['jsonpayload']['requesttransactionid']

        if response_code == '01':
            gutura = Abatuye.objects.get(transaction_id=response_id)
            gutura.successful = True
            gutura.save()

            #update Ikofi model
            ch = gutura.to_church
            am = gutura.amount
            ikofi = Ikofi.objects.get(church=ch)
            ikofi.amount = ikofi.amount + am
            ikofi.save()
            
            #Response Data
            data = {
                'message': 'success',
                'success': True,
                'request_id': response_id
            }

            return JsonResponse(data)
        return JsonResponse({'status':'failed'})

    else:
         return JsonResponse({'status':'you did not send a post method'})


@login_required(login_url='login')
def kubikuza(request):

    if request.method == 'POST':
        print("##########  Sent data: ",request.POST )
        form = KubikuzaForm(request.POST)
        
        if form.is_valid():
            
            print('########## Form is validated now: ', form.cleaned_data)

            #get cleaned
            phone_number = form.cleaned_data.get('phone_number')
            amount = form.cleaned_data.get('amount')
            
            #check if he/she have the amount
            available_balance = Ikofi.objects.get(church=request.user)
            available_balance = available_balance.amount

            transaction = sendPayments(phone_number, amount, available_balance)

            #use isinstance(transaction, tuple), but test before moving to production
            if isinstance(transaction, tuple ) and transaction[1].get('responsecode') == '2001':
                
                model_instance = form.save(commit=False)
                church = request.user
                
                model_instance.success = True
                model_instance.amount = abs(int(amount))
                model_instance.transaction_id = transaction[1].get("requesttransactionid") #get transaction id
                model_instance.church = church
                model_instance.phone_number = phone_number
                
                model_instance.save()

                ikofi = Ikofi.objects.get(church=church)
                ikofi.amount = ikofi.amount - (int(amount)+ 200)
                ikofi.save()


                return redirect(reverse('sentPayment'))

            #GET the response code
            #intouch_errors = RESPONSE_CODES.get(transaction)
            return render(request, 'wallet/sending-payment-error.html', {'cause':transaction})
    
    else:
        form = KubikuzaForm()

    return render(request, 'wallet/kubikuza-form.html', {'form':form})


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def dash(request):
    
    ikofi = Ikofi.objects.all()
    return render(request, 'wallet/dash.html', {'obj': ikofi})

@login_required(login_url='login')
def overview(request):
    
    try:
        abatuye = Abatuye.objects.filter(to_church=request.user).filter(successful=True).reverse()[:5]
        amount = Ikofi.objects.get(church=request.user)

    except Exception as e:
        print('you dont have a')
        return HttpResponse('There is some error on server. return back')

    return render(request, 'wallet/overview.html', {'abatuye': abatuye, 'amount':amount})


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def delete_(request, church_slug):
    church_to_del = Churches.objects.filter(slug=church_slug).first()
    return render(request, 'wallet/delete_.html', {'church':church_to_del})

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def delete_church(request, church_slug):
    church = Churches.objects.get(slug=church_slug)
    church.delete()
    print('church deleted')
    return redirect('/dash/')