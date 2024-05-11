import requests
from bs4 import BeautifulSoup

from utils import params, cookies, headers # from curlconvertor


# 1. create a new campaign -> get the campaign id: /campaigns/{camp_id}
# 2. PUT request to camp_id and udpate the campaign

def campaign_id_generator():
    "Generate a new campaign id based on qrgeneratorhub"
    while True:
        res = requests.post('https://qrcodegeneratorhub.com/qr/my/campaigns', params=params, cookies=cookies, headers=headers)
        if res.status_code != 200:
            raise Exception(f'Failed to generate campaign ID. Status code: {res.status_code}')
        yield res.url.split('campaigns')[1].split('?')[0].replace('/', '')


def update_campaign(camp_id: str):
    data = {
        '_method': 'put',
        'spec[color]': '#4869df'
        # 'campaign[name]': text,
    }

    res = requests.post(f'https://qrcodegeneratorhub.com/qr/my/campaigns/{camp_id}',
                        data=data,
                        cookies=cookies,
                        headers=headers)
    # if res.status_code != 200:
    #     raise Exception(f'Failed to update campaign. Status code: {res.status_code} {res.text}')
    print(res.status_code, res.text)
    return

update_campaign(4419800811)
# if __name__ == '__main__':
#     camp_ids = campaign_id_generator()
#     for i in range(1, 101): # the first pattern
#         for j in range(1, 5): # the second pattern
#             def leading_zeros(num, max_len=3):
#                 return "0" * (max_len - len(str(num)))

#             text = f'DXB {leading_zeros(i)}{str(i)} {leading_zeros(j)}{str(j)}'
#             camp_id = next(camp_ids)
#             print(f'ID generated: {camp_id}')

#             update_campaign(camp_id, text)
#             print(f'Campaign updated. Text: {text}')