import flickrapi
from PIL import Image
import requests
from io import BytesIO
from datauri import DataURI
import json
import os

# 필요한 모듈
"""
pillow - pip install pillow
requests
BytesIO
datauri - pip install python-datauri
"""

# Endpoint:  https://www.flickr.com/services/rest/
# 이미지 요청 Endpoint: https://live.staticflickr.com/{server-id}/{id}_{secret}.jpg

api_key = '15241ba8b471eeceb0a1cb78a1d8cb43'
api_secret = '98ff9eb8a2214843'
image_request_url = 'https://live.staticflickr.com/'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# 이미지 정보 가져오기
def getPhotoRef():
    text = input("키워드를 입력하세요: ")

    print(f'Flickr에서 {text} 를 검색하여 다운로드합니다. ( 1 ~ 100 페이지. 페이지당 500장 )')

    # 1부터 4페이지까지
    # 5 부분을 수정하면 됩니다. ex ) 101, 151 등등..
    for i in range(1, 2):
        photos_ref = flickr.photos.search(
            text=text,  # 검색 키워드
            sort='relevance',   # 관련 이미지로 불러오겠다.
            per_page=500,   # 페이지당 500개
            page=i,   # i 번째 페이지
        )

        photos = photos_ref['photos']['photo']
        photos_set = []

        for photo in photos:
            photo_ref = {
                'id': photo['id'],
                'secret': photo['secret'],
                'server': photo['server'],
            }

            photos_set.append(photo_ref)

        # 이미지 다운로드
        imageDownload(text, i, photos_set)

# 로컬에 이미지 다운로드하기
def imageDownload(keyword, page_idx, photos_set):

    if not os.path.isdir(keyword):
        os.makedirs(keyword)

    for idx, photo in enumerate(photos_set):
        url = f'https://live.staticflickr.com/{photo["server"]}/{photo["id"]}_{photo["secret"]}.jpg'
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        if not os.path.isdir(f'{keyword}/{page_idx}'):
            os.makedirs(f'{keyword}/{page_idx}')

        img.save(os.path.join(f'{keyword}/{page_idx}/', f'{idx}.jpg'))

if __name__ == "__main__":
    getPhotoRef()
