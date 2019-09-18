# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC9f4a82594a7168acc47b2506ccc927d1'
auth_token = '13820f6ceac5c85c875218a33c0e76db'
client = Client(account_sid, auth_token)

# phone = input("Please enter your phone number with area code using no spaces: ")
# phoneadj = '+1' + phone
# print (phoneadj)
# message = input("Please enter the message you'd like to send:")
# print (message)



message = client.messages \
    .create(
         body= 'OMFG IT WORKED!',
         from_='+18705222095',
         to= '+17853411918'
     )

print(message.sid)