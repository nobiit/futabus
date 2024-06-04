from datetime import datetime
from json import loads
from re import findall

from requests import Session


class FutaBusApi(Session):
    base_url = 'https://api.futabus.vn'

    def __init__(self, token=None):
        super().__init__()
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        self.headers['Origin'] = 'https://futabus.vn'
        self.headers['Referer'] = 'https://futabus.vn/'
        self.token = token

    def fetch_token(self):
        res = self.get('https://futabus.vn')
        m = findall(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', res.text)
        assert m
        d = loads(m.pop())
        self.token = d['props']['pageProps']['token']

    def request(self, method, url, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        # noinspection HttpUrlsUsage
        if not url.startswith('http://') and not url.startswith('https://'):
            url = self.base_url + '/' + url
        res = super().request(method, url, **kwargs)
        res.raise_for_status()
        return res

    def list_trips(self, year: int, month: int, day: int):
        res = self.post(
            url='search/trips',
            headers={
                'Authorization': 'Bearer %s' % self.token,
                'Clientapp': 'webApp',
            },
            json={
                'channel': 'web_client',
                'size': 200,
                'only_online_trip': True,
                'ticket_count': 1,
                'from_time': int(datetime(year, month, day, 0, 0, 0, 0).timestamp() * 1000),
                'to_time': int(datetime(year, month, day, 23, 59, 59, 999).timestamp() * 1000),
                'route_ids': [
                    2127,  # Nha Trang - BX An Suong
                ]
            }
        )
        # noinspection PyUnresolvedReferences
        return res.json()['data']['items']

    def list_seats(self, trip: dict):
        departure_time = datetime.fromtimestamp(trip['departure_time'] / 1000)
        res = self.get(
            url=f'https://api-busline.vato.vn/api/buslines/futa/booking/seats/{trip['route_id']}/{trip['id']}',
            headers={
                'Token_Type': 'anonymous',
                'X-Access-Token': self.token,
            },
            params={
                'departureDate': departure_time.strftime('%d-%m-%Y'),
                'departureTime': departure_time.strftime('%H-%M'),
                'kind': trip['seat_type_name']
            }
        )
        # noinspection PyUnresolvedReferences
        return res.json()['data']
