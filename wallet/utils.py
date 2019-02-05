import time
import requests
import hashlib
import os


RESPONSE_CODES = {
    '1000': 'Pending',
    '01': 'Successfull',
    '0002': 'Missing Username Information',
    '0003': 'Missing Password Information',
    '0004': 'Missing Date Information',
    '0005': 'Invalid Password',
    '0006': 'User Does not have an intouchPay Account',
    '0007': 'No such user',
    '0008': 'Failed to Authenticate',
    '2100': 'Amount should be greater than 0',
    '2200': 'Amount below minimum',
    '2300': 'Amount above maximum',
    '2400':'Duplicate Transaciton ID',
    '2500':'Route Not Found',
    '2600': 'Operation Not Allowed',
    '2700':'Failed to Complete Transaction',
    '527': 'Failed Due to Insufficient Funds',
    '515': 'Mobile number not registered on mobile money',
    '682': 'Insufficient balance or Number not registered on mobile money',
    '100': 'General Failure',
    '1200': 'Invalid Number',
    '1100': 'Number not supported on this Mobile money network',
    '1005': 'INSUFFICIENT FUNDS ON MOBILE MONEY ACCOUNT',
    '1101': 'Service ID not Recognized',
    '1102' : 'Invalid Mobile Phone Number',
    '1103': 'Payment Above Allowed Maximum',
    '1104': 'Payment Below Allowed Minimum',
    '1105': 'Network Not Supported',
    '1106': 'Operation Not Permitted',
    '1107': 'Payment Account Not Configured',

    ########### CUSTOM CODES MADE BY ME
    '9000': 'Phone number not correct.  \n (Phone number format: 078XXXXXXX and Must be MTN carrier)',
    '9001': 'Money amount not in range (100 - 200,000)',
    '9002': 'You dont have enough balance to make this transaction',
    '9003': 'Withdrawn money not in range of 10,000 and 200,000'
}


def processPayment(phone_number, amount):
    
    if len(phone_number) != 10 or not phone_number.startswith('078'):
        return '9000' #False

    if abs(int(amount)) not in range(100, 200000):
        return '9001'

    #if isinstance(12,int)

    #Preparing Data
    amount = abs(int(amount))
    username = 'regalo.trust'
    phone_number = int('25' + phone_number)
    epoch_time = int(time.time())
    transaction_id =int(str(epoch_time) + str(phone_number))
    timestamp = time.strftime('%Y%m%d%H%M%S') 
    partnerpassword = os.environ.get('partnerpassword', '') 
    accountno = os.environ.get("account_no", '')

    print("partnerpassword:", partnerpassword)
    print("accountno:", accountno)
    
    password = hashlib.sha256((username+accountno+partnerpassword+timestamp).encode('utf-8')).hexdigest()
    
    data = {
        'username':username,
        'timestamp': timestamp,
        'amount': amount,
        'password':password,
        'mobilephone': phone_number,
        'requesttransactionid': transaction_id
    }

    response=requests.post('https://www.intouchpay.co.rw/api/requestpayment/', data=data)

    print("###########: fsfsafsa", response.text)

    if response.json().get('responsecode') == '1000':  #transaction is pending
        return ('1000', response.json().get('requesttransactionid'))  #which is transaction id
    else:
        return response.json().get('responsecode')




def sendPayments(phone_number, amount, available_balance):

    if len(phone_number) != 10 or not phone_number.startswith('078'):
        return 'Phone number not valid, Double check Your Phone Number' #False

    if abs(int(amount)) not in range(100, 1000000):
        return 'Amount not Allowed'

    if (abs(int(amount)) > (int(available_balance) - 200)):
        return 'You dont have enough balance for this transaction!'    

    #Preparing Data
    username = 'regalo.trust'
    timestamp = time.strftime('%Y%m%d%H%M%S')
    amount = abs(int(amount))
    reason = " "
    phone_number = int('25' + phone_number)
    epoch_time = int(time.time())
    transaction_id =int(str(epoch_time) + str(phone_number))
     
    partnerpassword = os.environ.get('partnerpassword', '') 
    accountno = os.environ.get("account_no", '')
    #timestamp2=datetime.now(pytz.timezone('UTC')).__format__('%Y%m%d%H%M%S')

    
    
    password = hashlib.sha256((username+accountno+partnerpassword+timestamp).encode('utf-8')).hexdigest()
    
    data = {
        'username':username,
        'timestamp': timestamp,
        'amount': amount,
        'reason': reason,
        'password':password,
        'name': 'deposit',
        "withdrawcharge":1,
        'mobilephone': phone_number,
        "sid":1,
        'requesttransactionid': transaction_id
    }




    response=requests.post('https://www.intouchpay.co.rw/api/requestdeposit/', data=data)
    print("########## withdraw response: ",response.json())


    if response.json().get('responsecode') == '2001':  #transaction succeded
        return ('2001', response.json())  #which is transaction id
    else:
        return response.json().get('message')