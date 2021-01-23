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
# Endpoint? 같은 URL들에 대해서도 다른 요청을 하게끔 구별하게 해주는 항목
# 이미지 요청 Endpoint: https://live.staticflickr.com/{server-id}/{id}_{secret}.jpg

api_key = '15241ba8b471eeceb0a1cb78a1d8cb43'
api_secret = '98ff9eb8a2214843'
image_request_url = 'https://live.staticflickr.com/'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# 이미지 정보 가져오기
def getPhotoRef(text, start_page_num, last_page_num, photo_num):
    # text = input("키워드를 입력하세요: ")

    print(f'Flickr에서 {text}를 검색하여 다운로드합니다. ( {start_page_num} ~ {last_page_num} 페이지. 페이지당 {photo_num}장 )')

    # 1부터 4페이지까지
    # 5 부분을 수정하면 됩니다. ex ) 101, 151 등등..
    for i in range(start_page_num, last_page_num+1, 1):
        photos_ref = flickr.photos.search(
            text=text,  # 검색 키워드
            sort='relevance',   # 관련 이미지로 불러오겠다.
            per_page=photo_num,   # 페이지당 500개
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
        response = requests.get(url, timeout=20)
        img = Image.open(BytesIO(response.content))

        # if not os.path.isdir(f'{keyword}/{page_idx}'):
        #     os.makedirs(f'{keyword}/{page_idx}')
        #
        # img.save(os.path.join(f'{keyword}/{page_idx}/', f'{idx}.jpg'))


        if not os.path.isdir(f'{keyword}'):
            os.makedirs(f'{keyword}')
        img.save(os.path.join(f'{keyword}', f'{page_idx}_{idx}.jpg'))

if __name__ == "__main__":
    """
    파라미터 설명
    start_page_num : 다운받을 시작 페이지
    last_page_num : 다운받을 마지막 페이지
    photo_num : 한 페이지당 다운받을 사진의 갯수
    """

    # getPhotoRef(text="animal", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="appliance", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="art", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="clothes", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="family", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="flower", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="food", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="furniture", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="indoor", start_page_num=1, last_page_num=50, photo_num=100)
    # getPhotoRef(text="insect", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="instrument", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="korea", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="outdoor", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="people", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="scenery", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="season", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="selfie", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="sign", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="sports", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="transportation", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="travel", start_page_num=1, last_page_num=50, photo_num=100)
    getPhotoRef(text="vintage", start_page_num=1, last_page_num=50, photo_num=100)

