# 정규화 방식 변경
- 논문 "How Does Batch Normalization Help Optimization? - Shibani Santurkar, Dimitris Tsipras"에 따르면
- BN이 interval covariance shift와 상관이 없다고 주장함

- 대안법
## 1.
- weight normalization + group normalization
- -> batch의 크기가 작을 경우(2, 4, 8) BN보다 성능이 좋음
- 출처 : 논문 "Group Normalization - Yuxin Wu, Kaiming He"

## 2.
- instance normalization
- gan에서 BN을 대체하여 사용
- 실시간 생성에 효과적

## 3.
- switchable normalization
- 이미지 분류, 객체 탐지에서 BN보다 우수

## 4.
- spectral normalization
- GAN의 훈련을 향상시키기 위해 판별자의 lipschitz 상수를 제한한다.
- 최소한의 조정으로 GAN의 학습을 개선함
