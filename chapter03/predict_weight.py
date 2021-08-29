# -*- coding: utf-8 -*-
"""predict_weight.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cvnCC7NueTj-feGSc_knoq0anFwypny-
"""

# k-최근접 이웃 회귀 - 이웃된 값들의 평균
# 무게를 예측하는 문제를 회귀 라고 함.
# 지도 학습 알고리즘은 크게 분류와 회귀(regression)로 나눈다.
# 분류는 sample을 몇 개의 클래스 중 하나로 분류하는 것을 의미.
# 회귀는 임의의 어떤 숫자를 예측하는 문제
# ex) 내년도 경제성장률을 예측하는 것 등
# 회귀는 정해진 클래스가 없고 임의의 수치를 출력.
import numpy as np

perch_length = np.array([8.4, 13.7, 15.0, 16.2, 17.4, 18.0, 18.7, 19.0, 19.6, 20.0, 21.0,
       21.0, 21.0, 21.3, 22.0, 22.0, 22.0, 22.0, 22.0, 22.5, 22.5, 22.7,
       23.0, 23.5, 24.0, 24.0, 24.6, 25.0, 25.6, 26.5, 27.3, 27.5, 27.5,
       27.5, 28.0, 28.7, 30.0, 32.8, 34.5, 35.0, 36.5, 36.0, 37.0, 37.0,
       39.0, 39.0, 39.0, 40.0, 40.0, 40.0, 40.0, 42.0, 43.0, 43.0, 43.5,
       44.0])
perch_weight = np.array([5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0, 110.0,
       115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0, 130.0,
       150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0, 197.0,
       218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0, 514.0,
       556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0, 820.0,
       850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0, 1000.0,
       1000.0])

import matplotlib.pyplot as plt

plt.scatter(perch_length,perch_weight)
plt.xlabel('length')
plt.ylabel('weight')
plt.show()

from sklearn.model_selection import train_test_split
train_input, test_input, train_target, test_target = train_test_split(perch_length, perch_weight, random_state=42)

# 1차원배열이 아니라 2차원배열로 작업해야한다.
# -1 == len(list)
train_input = train_input.reshape(-1,1)
test_input = test_input.reshape(-1,1)
print(train_input.shape, test_input.shape)

# 결정계수(R^2)
from sklearn.neighbors import KNeighborsRegressor

knr = KNeighborsRegressor()

knr.fit(train_input,train_target)
print(knr.score(test_input,test_target))
# 분류에서는 정확도라고 표현. 회귀에서는 결정계수라고 표현.
# R^2 = 1 - (타깃-예측)^2의 합 / (타깃-타깃평균)^2의 합
# 예측은 타깃에 대해서 예측한 값.(타깃 주변 값의 평균)

# 타깃과 예측의 절댓값 오차를 평균하여 반환
from sklearn.metrics import mean_absolute_error

# test 세트에 대한 예측
test_prediction = knr.predict(test_input)

# 테스트 세트에 대한 평균 절댓값 오차 계산
mae = mean_absolute_error(test_target, test_prediction)
print(mae)
# 결과에서 예측이 평균적으로 19g 정도 타깃값과 다르다는 의미.

# 과대적합, 과소적합

# 과대적합(overfitting) 훈련세트에만 점수가 좋고 테스트 세트에서는 점수가 나쁜 경우
# 훈련세트에만 잘맞는 모델.. 실전에 문제가 생김.

# 과소적합(underfitting) 훈련세트보다 테스트세트 점수가 높거나 두 점수가 모두 낮은 경우
# 즉, 모델이 너무 단순하여 훈련 세트에 적절히 훈련되지 않은 경우. 
# 훈련 세트가 전체 데이터를 대표한다고 가정하므로 이런 문제가 발생하지 않도록해야한다.
print(knr.score(train_input, train_target))
# 과소적합 문제해결 : 모델을 조금 더 복잡하게 만듬.

# 이웃을 줄이면 훈련 세트에 있는 국지적인 패턴에 민감해지고, 이웃의 개수를 늘리면 데이터 전반에 있는 일반적인 패턴을 따름.
# 이웃의 개수를 줄임
knr.n_neighbors = 3

# retraining
knr.fit(train_input, train_target)
print(knr.score(train_input, train_target))
print(knr.score(test_input,test_target))
# 이웃의 개수를 컨트롤 함으로써 과대적합, 과소적합이 발생하지 않게 함.

# 선형 회귀(linear regression)로 훈련 세트 범위 밖의 샘플 예측
print(knr.predict([[50]]))

# 50과 근접한 개수
distances, indexes = knr.kneighbors([[50]])

plt.scatter(train_input, train_target)
plt.scatter(train_input[indexes], train_target[indexes], marker='D')
plt.scatter(50, 1033, marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()

# 이웃 샘플의 타깃의 평균
print(np.mean(train_target[indexes]))
# 즉, 새로운 샘플이 훈련 세트의 범위를 벗어나면 정확한 값을 리턴할 수 없다.. 100cm도 여전히 1033 무게를 리턴하므로,,,,
print(knr.predict([[100]]))

distances, indexes = knr.kneighbors([[100]])

plt.scatter(train_input, train_target)
plt.scatter(train_input[indexes], train_target[indexes], marker='D')
plt.scatter(100,1033, marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()

# linear regression
# 어떤 직선을 학습하는 알고리즘
from sklearn.linear_model import LinearRegression

lr = LinearRegression()

lr.fit(train_input, train_target)

print(lr.predict([[50]]))
# 직선 = y = ax + b (a는 기울기)
print(lr.coef_, lr.intercept_)
# 머신러닝에서 기울기를 계수(coefficient) or weight(가중치) 라고 부름
# 훈련 세트를 저장해서 훈련하는 것을 사례 기반 학습 이라고 함.
# 모델 기반 학습은 최적의 모델 파라미터를 찾아서 학습하는 것.
# model parameter는 머신러닝 알고리즘이 찾은 값이라는 의미.

plt.scatter(train_input, train_target)
# y=a*15+b ~ y=a*50+b 까지 선분을 그은 직선을 구함.
plt.plot([15,50], [15*lr.coef_+lr.intercept_,50*lr.coef_+lr.intercept_])
plt.scatter(50,1241.8, marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()

# 둘다 낮다.. 과소적합 - 그래프 왼쪽 아래...정확도가 매우 낮다..
print(lr.score(train_input, train_target))
print(lr.score(test_input, test_target))

# 다항 회귀 : 다항식을 사용한 선형 회귀를 의미.
# 최적의 곡선 찾기
# y = ax^2+bx+c
train_poly = np.column_stack((train_input**2,train_input))
test_poly = np.column_stack((test_input**2,test_input))
print(train_poly.shape, test_poly.shape)

# 이 모델이.. 2차방정식의 a,b,c를 잘 찾아줘야한다..즉, model parameters
lr = LinearRegression()
lr.fit(train_poly, train_target)

print(lr.predict([[50**2, 50]]))
print(lr.coef_, lr.intercept_)
# y = lr.coef[0]*x^2+lr.coef[1]*x+lr.intercept_ : 즉, 이 그래프를 학습.

# 다항식 그리기.
point = np.arange(15, 50)

plt.scatter(train_input,train_target)

# 15~49까지 2차방정식 그리기.
plt.plot(point, lr.coef_[0]*point**2+lr.coef_[1]*point+lr.intercept_)
plt.scatter(50,1573.98, marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()

# 과소적합이 약간 존재
print(lr.score(train_poly, train_target))
print(lr.score(test_poly, test_target))

# 특성 공학과 규제
# 다중 회귀(multiple regression) : 여러 개의 특성을 사용한 선형 회귀
# 1개 특성일 때, 선형 회귀 모델이 학습하는 것은 직선. 2개면 선형 회귀는 평면을 학습한다.
# 특성이 3개인 경우..즉, 3차원 공간 이상을 그리거나 상상할 수 없다....
# 그래서.. 기존 특성으로 새로운 특성을 만든다. 이걸 특성 공학(feature engineering)이라고 부름
# ex) length*height = newFeature

# pandas는 데이터 분석 library
# dataframe은 판다스의 핵심 데이터구조이다.
# pandas를 사용해 데이터를 인터넷에서 내려받아 데이터프레임에 저장. csv 파일
import pandas as pd
df = pd.read_csv('https://bit.ly/perch_csv_data')
perch_full = df.to_numpy()
# print(perch_full)

train_input, test_input, train_target, test_target = train_test_split(perch_full,perch_weight, random_state=42)
# scikit-learn은 특성을 만들거나 전처리하기 위한 다양한 클래스를 제공 - it's called transformer
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures()
poly.fit([[2,3]])
print(poly.transform([[2,3]]))
# fit(훈련데이터) 메서드는 새롭게 만들 특성 조합을 찾고, transform() 는 실제로 데이터를 변환한다.
# poly.fit()에서 target이 필요하지 않다.. 그리고 transform()은 두 개의 특성으로 6개의 특성을 가진 샘플을 리턴받는다.
# 1은 절편을 위한 항. 그러므로 1을 제거하고 만들어도 된다.
poly = PolynomialFeatures(include_bias=False)
poly.fit([[2,3]])
print(poly.transform([[2,3]]))
# 여기에서 include_bias=False를 지정하지 않아도 사이킷런 모델은 자동으로 특성에 추가된 절편 항을 무시한다.

poly.fit(train_input)
train_poly = poly.transform(train_input)
print(train_poly.shape)
print(poly.get_feature_names())
# 항상 훈련 세트를 기준으로 테스트 세트를 변환하는 습관을 들이는 것이 좋다.
test_poly = poly.transform(test_input)

# 다중 회귀 모델 훈련
# 여러 개의 특성을 사용하여 선형 회귀를 수행
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(train_poly, train_target)
# 이렇게 특성이 늘어난다면 선형 회귀의 능력은 좋아진다.
print(lr.score(train_poly,train_target))
print(lr.score(test_poly,test_target))

poly = PolynomialFeatures(degree=5, include_bias=False)
poly.fit(train_input)
train_poly = poly.transform(train_input)
test_poly = poly.transform(test_input)
print(train_poly.shape)

lr.fit(train_poly, train_target)
print(lr.score(train_poly,train_target))
# 특성의 개수를 크게 늘리면 선형 모델은 훈련 세트에 대해 거의 완벽하게 학습할 수 있다. 
# 하지만 이런 모델은 훈련 세트에 너무 과대적합되므로 테스트 세트에서는 형편없는 점수를 만든다.
print(lr.score(test_poly,test_target))

# 규제(regularization)
# : 머신러닝 모델이 훈련 세트를 너무 과도하게 학습하지 못하도록 훼방하는 것을 말한다. 즉, 모델이 훈련 세트에 과대적합되지 않도록 만드는 것
# 선형 회귀 모델의 경우 특성에 곱해지는 계수(or 기울기)의 크기를 작게 만드는 일.
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
# 훈련 세트로 학습한 변환기를 사용해 테스트 세트까지 변환해야한다.
ss.fit(train_poly)
train_scaled = ss.transform(train_poly)
test_scaled = ss.transform(test_poly)

# 선형 회귀 모델에 규제를 추가한 모델을 릿지(ridge)와 라쏘(lasso)라고 부름.
# 릿지 회귀 : 계수를 제곱한 값을 기준으로 규제를 적용 - 일반적으로 릿지를 좀 더 선호
from sklearn.linear_model import Ridge

ridge = Ridge()
ridge.fit(train_scaled, train_target)
print(ridge.score(train_scaled, train_target))
# test가 정상수치.. 많은 특성을 사용했지만, 훈련 세트에 과대적합되지 않아서.
print(ridge.score(test_scaled,test_target))

# alpha 값으로 규제의 강도를 조절.
# alpha가 크면 규제 강도가 쎄짐. - 계수 값을 더 줄이고 조금 더 과소적합되도록 유도
# alpha가 작으면 규제 강도가 약해지고 과대적합될 가능성이 큼.
# 하이퍼파라미터(hyperparameter)는 머신러닝 모델이 학습할 수 없고 사람이 직접 입력해줘야하는 파라미터
# 적절한 alpha값을 찾는 한 가지 방법은 alpha 값에 대한 R^2값의 그래프를 그려 보는 것이다.
# 즉, 훈련 세트와 테스트 세트의 점수가 가장 가까운 지점이 최적의 alpha 값이 된다.
import matplotlib.pyplot as plt

train_score = []
test_score = []
alpha_list = [0.001, 0.01,0.1,1,10,100]
for alpha in alpha_list:
  ridge = Ridge(alpha=alpha)
  ridge.fit(train_scaled,train_target)
  train_score.append(ridge.score(train_scaled,train_target))
  test_score.append(ridge.score(test_scaled,test_target))

# 그래프 왼쪽이 너무 촘촘해질 가능성이 있으므로.. log로 표현. 즉, 0.001을 -3으로 표현.
# blue = train, orange = test
plt.plot(np.log10(alpha_list),train_score)
plt.plot(np.log10(alpha_list),test_score)
plt.xlabel('alpha')
plt.ylabel('R^2')
plt.show()

# alpha=0.1 일때 가장 근접함.
ridge = Ridge(alpha=0.1)
ridge.fit(train_scaled,train_target)
# 훈련과 테스트가 근접함.
print(ridge.score(train_scaled,train_target))
print(ridge.score(test_scaled,test_target))

# 라쏘 회귀 : 계수의 절댓값을 기준으로 규제를 적용.
from sklearn.linear_model import Lasso
lasso = Lasso()
lasso.fit(train_scaled, train_target)
print(lasso.score(train_scaled, train_target))
print(lasso.score(test_scaled, test_target))

train_score = []
test_score = []
alpha_list = [0.001,0.01,0.1,1,10,100]
for alpha in alpha_list:
  # 최적의 계수를 찾기 위해 반복적인 계산을 수행할때, 지정한 반복 횟수가 부족할 때 convergence 에러가 발생 : max_iter=10000 지정. 필요하면 더 늘릴 수 있음.
  lasso = Lasso(alpha=alpha,max_iter=10000)
  lasso.fit(train_scaled,train_target)
  train_score.append(lasso.score(train_scaled,train_target))
  test_score.append(lasso.score(test_scaled,test_target))

# blue=train, orange=test
plt.plot(np.log10(alpha_list),train_score)
plt.plot(np.log10(alpha_list),test_score)
plt.xlabel('alpha')
plt.ylabel('R^2')
plt.show()

lasso = Lasso(alpha=10)
lasso.fit(train_scaled, train_target)
print(lasso.score(train_scaled,train_target))
print(lasso.score(test_scaled,test_target))

# 라쏘모델은 계수 값을 아예 0으로 만들 수 있다.
# 라쏘모델의 계수 = lasso.coef_
# np.sum(true) true==1 False==0 으로 인식해서 더해줌.
print(np.sum(lasso.coef_==0))
# 즉, 55개의 특성중에 사용된 특성은 15개란 의미.
# 이런 특징 덕분에 유용한 특성을 골라내는 용도로도 사용할 수 있다.

# 정리
# 정확도를 높이기 위해 더 많은 특성을 사용(다중 회귀). 이때, 많은 특성을 사용할때 정확도를 높이기 위해 제약하기 위한 도구인 릿지 회귀와 라쏘 회귀 사용