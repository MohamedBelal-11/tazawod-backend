from twilio.rest import Client #type: ignore

account_sid = 'AC91a909b98c7035d13ace54504bc8c1ab'
auth_token = '14d91342e56b286eec729b8240be07bf'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your Twilio code is 1238432',
  to='whatsapp:+201283410254'
)

print(message.sid)