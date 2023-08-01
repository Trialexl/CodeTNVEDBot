import requests
from aiogram import Bot, Dispatcher,types, executor
from config import TokenAPI,siteURL
import json



bot = Bot(token=TokenAPI)
dp = Dispatcher(bot)
      
@dp.message_handler()
async def GetGroupCode(message: types.Message):
    
    text = message.text
    headers = {
                'Content-Type': 'application/json'
            }
    data =json.dumps({
            "text": text,
            "qty": 3
        })
    response = requests.request("POST",siteURL, data=data,headers = headers)
    
    json_data = response.json()
    text_our = json_data['Our']
    probability_our = '{:.3f}'.format(float(text_our[0]['Probability'])*100)
    if text_our[0]['valid']:
        till =''
    else:
        till = text_our[0]['till']
    Ourid = text_our[0]['id']
    Ourlabel = text_our[0]['label']
    text_our_template1st = f'{Ourid}:{Ourlabel} \nВероятность: {probability_our} {till}'

    text_OuterService = json_data['OuterService']
    if len(text_OuterService) != 0:
        code = text_OuterService[0]['CODE']
        name = text_OuterService[0]['KR_NAIM']
        probability = text_OuterService[0]['probability']
        text_OuterService_template1st = f'\n\n\nСторонний сервис: {code}: {name}\nВероятность: {probability}'
    else:
        text_OuterService_template1st = ''
    await message.reply(text=text_our_template1st+text_OuterService_template1st)

if __name__=='__main__':
    executor.start_polling(dp)