from twilio.rest import Client
from datetime import datetime

account_sid = os.environ('twilio_account_sid')
auth_token = os.environ('twilio_auth_token')
client = Client(account_sid, auth_token)

def send_sms(sendTo, items):
    message = 'Hi '+ str(sendTo).capitalize() +',\n The following items in your fridge are going to/have already expired: \n' + ''.join(items)
    message += 'Head to FridgeGerald.me for to know about recipes to consume these products!'
    print(message)
    mobileNumber = sendTo.phone_number
    message = client.messages \
                    .create(
                        body=message,
                        from_='+12026013748',
                        to=mobileNumber
                    )

    print(message.sid)


if __name__ == "__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FridgeGerald.settings")
    import django
    django.setup()
    from fridgeManager.models import Fridge,FridgeFoodItem,UserProfile
    # Loop through all fridges
    for fridge in Fridge.objects.all():
    # Get user's name and phone number
        user = fridge.user
        userDetails = UserProfile.objects.get(user = user)
        # Loop through all the items
        expiringInTwoDays = []
        for item in fridge.fridgefooditem_set.all().order_by('-best_before'):
            expiresIn = (item.best_before - datetime.now().date()).days
            if(expiresIn < 0):
                itemString = str(item.food.name) + ' has already expired, please discard it.'
            elif(expiresIn <= 1):
                itemString = str(item.food.name) + ' is expiring '
                if(expiresIn == 0):
                    itemString += 'today.'
                elif(expiresIn == 1):
                    itemString += 'tomorrow.'
            
            if(expiresIn <= 1):
                expiringInTwoDays.append('-' + itemString + '\n')
        
        if(len(expiringInTwoDays) != 0):
            send_sms(userDetails, expiringInTwoDays)

