from django.shortcuts import render
from django.contrib.auth.models import User
# def
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import SendMoneyForm
from .forms import RequestMoneyForm
from django.http import JsonResponse
from django.conf import settings
from .models import RequestMoney, TransferMoney
from django.utils import timezone

def convert_currency(amount, base_currency, target_currency):
    # Get the exchange rate from the response
    exchange_rate = settings.EXCHANGE_RATE[base_currency+"_"+target_currency]

    # Convert the amount to the target currency
    converted_amount = amount * exchange_rate

    # Round the converted amount to 2 decimal places
    converted_amount = round(converted_amount, 2)
    return converted_amount

@login_required
def homepage(request):
    return render(request, 'payapp/homepage.html')

@login_required
def send_money(request):
    if request.method == 'GET':
        form = SendMoneyForm()
        return render(request, 'payapp/send_money.html', {'form': form})
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            # get cleaned data from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            amount = form.cleaned_data['amount']
            if amount <= request.user.account.amount:
                request.user.account.amount = request.user.account.amount-amount
                request.user.account.save()
                try:
                    receiving_user=User.objects.get(first_name=first_name, last_name=last_name, email=email)
                except:
                    return render(request, 'payapp/send_money.html', {'form': form,"USER_NOT_FOUND": True})
                receiving_user.account.amount += convert_currency(amount, request.user.account.currency, receiving_user.account.currency)
                receiving_user.account.save()
                TransferMoney.objects.create(from_user=request.user, to_user=receiving_user, amount=amount)
                return render(request, 'payapp/send_money.html', {'form': form,"IS_SUFFICIENT_BALANCE": True})
            else:
                return render(request, 'payapp/send_money.html', {'form': form,"IS_SUFFICIENT_BALANCE": False})


        else:
            return render(request, 'payapp/send_money.html', {'form': form})
@login_required
def request_money(request):
    if request.method == 'GET':
        form = RequestMoneyForm()
        return render(request, 'payapp/request_money.html', {'form': form})
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            # get cleaned data from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            amount = form.cleaned_data['amount']
            # create a new Request object
            requester = request.user
            requestee = User.objects.get(email=email)
            if requester == requestee:
                return render(request, 'payapp/request_money.html', {'form': form,"SAME_USER": True})
            RequestMoney.objects.create(requester=requester, requestee=requestee, amount=amount)

            # create a notification for the requestee
            #message = f"You received a money request for {amount} {requester.account.currency} from {requester.account.get_full_name()}."
            #notifications.objects.create(user=requestee, message=message)

            #messages.success(request, "Your money request has been sent.")
           # return redirect('dashboard')
            return render(request, 'payapp/request_money.html', {'form': form,"REQUESTED": True})

        return render(request, 'payapp/request_money.html', {'form': form})

@csrf_exempt
def convert_currency_view(request, base_currency, target_currency, amount):
    if request.method == 'GET':
        # Get the exchange rate from the response
        try:
            exchange_rate = settings.EXCHANGE_RATE[base_currency+"_"+target_currency]
        except:
            return JsonResponse({'error': 'Invalid base or target currency'}, status=400)
        # Convert the amount to the target currency
        converted_amount = amount * exchange_rate

        # Round the converted amount to 2 decimal places
        converted_amount = round(converted_amount, 2)

        return JsonResponse({'converted_amount': converted_amount})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
def notifications(request):
    claimed_transactions = RequestMoney.objects.filter(requester=request.user).order_by('-created_at')
    requested_transactions = RequestMoney.objects.filter(requestee=request.user, declined_at__isnull=True, accepted_at__isnull=True).order_by('-created_at')   
    received_transactions = TransferMoney.objects.filter(to_user=request.user).order_by('-created_at')
    sent_transactions = TransferMoney.objects.filter(from_user=request.user).order_by('-created_at')
    
    if request.method == 'GET':
        return render(request, 'payapp/notifications.html', {'REQUESTED_TRANSACTIONS': requested_transactions, 'RECEIVED_TRANSACTIONS': received_transactions, 'SENT_TRANSACTIONS': sent_transactions, 'CLAIMED_TRANSACTIONS': claimed_transactions})

    elif request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        accepted = request.POST.get('status')
        transaction = RequestMoney.objects.get(id=transaction_id)
        if accepted == 'Accept' and transaction.amount<transaction.requestee.account.amount:
            transaction.requestee.account.amount -= convert_currency(transaction.amount, transaction.requester.account.currency, transaction.requestee.account.currency)
            transaction.requestee.account.save()
            transaction.requester.account.amount +=transaction.amount
            transaction.requester.account.save()
            transaction.accepted_at = timezone.now()
            transaction.save()
            TransferMoney.objects.create(from_user=transaction.requestee, to_user=transaction.requester, amount=transaction.amount)
            return render(request, 'payapp/notifications.html', {'REQUESTED_TRANSACTIONS': requested_transactions, 'RECEIVED_TRANSACTIONS': received_transactions, 'SENT_TRANSACTIONS': sent_transactions, 'CLAIMED_TRANSACTIONS': claimed_transactions})
        if accepted == 'Accept' and transaction.amount>transaction.requestee.account.amount:
            return render(request, 'payapp/notifications.html', {'REQUESTED_TRANSACTIONS': requested_transactions, 'RECEIVED_TRANSACTIONS': received_transactions, 'SENT_TRANSACTIONS': sent_transactions, 'CLAIMED_TRANSACTIONS': claimed_transactions, "INSUFFICIENT_BALANCE": True})

        else:
            transaction.declined_at = timezone.now()
            transaction.save()
            return render(request, 'payapp/notifications.html', {'REQUESTED_TRANSACTIONS': requested_transactions, 'RECEIVED_TRANSACTIONS': received_transactions, 'SENT_TRANSACTIONS': sent_transactions, 'CLAIMED_TRANSACTIONS': claimed_transactions})
