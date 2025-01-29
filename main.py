from time import sleep

import requests

from api import FutaBusApi
from utils import send_mail
from socket import gethostname

if __name__ == '__main__':
    f = FutaBusApi()
    send_mail('Đã bắt đầu ở máy %s' % gethostname())
    while True:
        try:
            while True:
                print('Checking...')
                for i in range(2):
                    for item in f.list_trips(2025, 2, 2 + i):
                        if int(item['raw_departure_time'].split(':')[0]) > 13:
                            for seat in f.list_seats(item):
                                if seat['bookStatus'] == 1:
                                    continue
                                # if seat['chair'] in ['B16']:
                                #     continue
                                message = 'Phát hiện vé Phương Trang lúc %s, ghế %s' % (item['raw_departure_time'], seat['chair'])
                                print(message)
                                send_mail(message)
                                # res = requests.post('https://bot.nobidev.com/message', json={
                                #     'message': message,
                                # })
                                # res.raise_for_status()
                                # print((item['raw_departure_time'], seat['chair']), res.json())
                print('Done !')
                sleep(10)
        except requests.HTTPError as ex:
            if ex.response.status_code == 401:
                print('Renewing ...')
                f.fetch_token()
                continue
            raise ex
