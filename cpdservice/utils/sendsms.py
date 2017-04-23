from pprint import pprint
import requests

#from settings import sid, token

def SendSMS(sms_from, sms_to, sms_body):

    sid = "ulinkbioenergy"
    token = "264639ffed7c9be57f32dd6e0ddb654cba330f8a"
    return requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Sms/send.json'.format(sid=sid),
        auth=(sid, token),
        data={
            'From': sms_from,
            'To': sms_to,
            'Body': sms_body,
            'Priority': 'High'
        })

if __name__ == '__main__':
    # 'From' doesn't matter; For transactional, this will be replaced with your SenderId;
    # For promotional, this will be ignored by the SMS gateway
    # Incase you are wondering who Dr. Rajasekhar is http://en.wikipedia.org/wiki/Dr._Rajasekhar_(actor)
    r = SendSMS(
        sms_from='02230038191',  # sms_from='8808891988',
        sms_to='8007153711', # sms_to='9052161119'
        sms_body = 'Your verification code for the AgroStar Mobile Application is: 1234')
    print r.status_code
    pprint(r.json())

