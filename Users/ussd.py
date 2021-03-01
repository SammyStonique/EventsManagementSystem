from django.http import request
response = ''
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == '':
        response = "CON What ent type would you want to attend \n"
        response += "1. Public \n"
        response += "2. Invites Only"
    elif text == '1':
        response = "CON Choose account information you want to view \n "
        response += "1. Account number \n"
        response += "2. Account balance"
    elif text == "1*1":
        accountNumber = "ACC1001"
        response = "END Your account number is " + accountNumber
    elif text == "1*2":
        accountBalance = "KES 10,000"
        response = "END Your account balance is " + accountBalance
    elif text == "2":
        response = "END Your phone number is " + phone_number
    
        return response