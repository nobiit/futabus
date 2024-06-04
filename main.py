from time import sleep

import requests

from api import FutaBusApi

if __name__ == '__main__':
    f = FutaBusApi()
    f.fetch_token()
    while True:
        print('Checking...')
        for item in f.list_trips(2024, 6, 9):
            if int(item['raw_departure_time'].split(':')[0]) > 13:
                for seat in f.list_seats(item):
                    if seat['bookStatus'] == 1:
                        continue
                    if seat['chair'] in ['B16']:
                        continue
                    res = requests.post('https://bot.nobidev.com/message', json={
                        'message': 'Phát hiện vé Phương Trang lúc %s, ghế %s' % (item['raw_departure_time'], seat['chair'])
                    })
                    res.raise_for_status()
                    print((item['raw_departure_time'], seat['chair']), res.json())
        print('Done !')
        sleep(30)
