import shutil
from os import walk

import requests
from bs4 import BeautifulSoup
from utils import cookies, headers

def qrcode_generator():
    "Yield (id, name) of all qr codes in the account."
    for page_num in range(1, 21):
        params = {"page": page_num}
        res = requests.get("https://qrcodegeneratorhub.com/qr/my/campaigns", params=params, cookies=cookies, headers=headers)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text, 'html.parser')
        campaigns = soup.find_all("tr")[1:] # first element contains filters
        for c in campaigns:
            id_ = c['data-clickable-url-value'].replace('/qr/my/campaigns/', '')
            name = c.find(class_='d-none d-md-inline-block ml-1').get_text()
            yield (id_, name)

def update_color(code):
    data = {
        '_method': 'put',
        'spec[color_type]': 'pure',
        'spec[color_pure]': '#000000',
        'spec[color]': '#4869df',
        'spec[color_direction]': 'radial',
        'spec[color1]': '#000000',
        'spec[color2]': '#9b9b9b',
        'spec[color_background]': 'white',
        'spec[color_apply_to_eye]': [
            '0',
            '1',
        ],
        'spec[color_eye_outer]': '#000000',
        'spec[color_eye_inner]': '#000000',
    }
    res = requests.post(f'https://qrcodegeneratorhub.com/qr/my/qr_codes/{code}', cookies=cookies, headers=headers, data=data)
    assert res.status_code == 200

def download_qr(campaign_page_html, filename):
    soup = BeautifulSoup(campaign_page_html, 'html.parser')
    download_url = soup.find(class_="card-footer").find("form")["action"]
    code = download_url.replace("/qr/downloads?code=", "").split("&")[0]
    update_color(code)
    print(f"Color updated: {code}")
    data = {
        'simple': '0',
        'size': '4',
        'type': 'jpg',
        'button': '',
    }
    
    res = requests.post('https://qrcodegeneratorhub.com' + download_url, data=data,
                        headers=headers, cookies=cookies, stream=True)
    assert res.status_code == 200
    with open(filename, 'wb+') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)


qr_codes = qrcode_generator()
s = requests.session()
for id_, name in qr_codes:
    res = requests.get(f"https://qrcodegeneratorhub.com/qr/my/campaigns/{id_}", cookies=cookies, headers=headers)
    print(f'Downloading: ({id_}, {name})')
    assert id_ in res.url
    filenames = [f.replace('.jpg', '') for f in next(walk('files/'), (None, None, []))[2]]
    if name in filenames:
        print(f'Skipping: f{name}')
        continue
    download_qr(res.text, f'files/{name}.jpg')
    print(f'QR code downloaded: {name}.jpg')