# CartoonGAN을 활용한 이미지 애니메이션화 웹 서비스

## 프로젝트 설명
CartoonGAN을 활용하여 사용자가 올린 사진을 원하는 애니메이션의 화풍으로 애니메이션화 해주는 웹 서비스를 제공한다.

## 프로젝트 구조
> ## 데이터 수집
- 애니메이션 동영상 : Youtube 동영상 다운로드
- 애니메이션 포스터 : Netflix, Google 크롤링
- 실제 사진 : Flickr API (6개의 카테고리별 1,000장. 총 6,000장)

> ## 데이터 전처리
- 애니메이션 동영상을 2초 단위로 캡처하여 JPG 파일로 저장
- 색채 분석을 위해 한 장면당 6 분할
- CartoonGAN 학습 과정을 위해 한 장면당 5개씩 random crop (OpenCV)
- 애니메이션별로 이미지 5~6,000장

> ## 색채 분석
- CartoonGAN의 성능을 높이기 위해 색채를 활용하면 좋을 것 같아 색채 분석을 시행함
- 애니메이션별로 RGB, HSV 색상 값을 추출한 후, 색상 분포도를 3D plot으로 그림

> ## CartoonGAN 모델링
- GAN, CartoonGAN, Style Transfer, ResNet 논문, 다양한 Normalization 방법 연구
- CartoonGAN 모델링 후 학습을 진행해본 결과, 배치 사이즈가 8을 넘어가게 되면 GPU에 무리가 가서 제대로 동작을 하지 않는 것을 확인함. 배치 사이즈가 작을 때, 정확도를 높이는 방법을 연구
- 기존 논문의 구조에서는 generator는 instance normalization, discriminator는 batch normalization을 사용. 다양한 Normalization의 방법을 연구한 결과, 배치 사이즈가 작은 2, 4 같은 경우에서는 instance, batch normalization보다 group normalization의 성능이 더 좋다는 판단을 하여 학습을 시켜보았지만, 결과가 오히려 좋지 않았음
- 그렇다면 정규화 방법을 2가지 이상을 사용하여 성능을 방법을 연구하던 중, 한 논문에서 group normalization과 weight normalization을 함께 사용하면 batch normalization보다 더 좋은 결과를 낸다는 것을 발견
- GN + WN으로 정규화 방법을 바꾼 결과, 성능이 좀 더 개선된 것을 확인

> ## 웹 서비스 설계 - Front-end / Server / Backend
- 로그인, 회원가입
- 공개 / 개인 갤러리
- 필터 설명 (색채 분석 결과 3D plot)
- 이미지 변환 페이지

## 개발 환경
Windows10, AWS-Ubuntu, MacOS, Netlify, MongoDB

## 개발 언어
Python, HTML5, CSS3, JavaScript

## 개발 라이브러리
Tensorflow, Keras, OpenCV, Matplotlib, BeautifulSoup, Selenium, Node.js, Flask

## 개발 도구
Pycharm, Colab, Visual Studio Code, AWS, Github

## 사용 장비
NVIDIA GPU-RTX 3070
