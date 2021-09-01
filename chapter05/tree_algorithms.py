# -*- coding: utf-8 -*-
"""tree_algorithms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P_EAfX_25h5B49TvnfHBDpOEV6BabKcL
"""

# 결정 트리
import pandas as pd
wine = pd.read_csv('https://bit.ly/wine_csv_data')
# 0=red, 1=white
print(wine.head())
print("----------------------------------------\n")
# dataframe의 각 열의 데이터 타입과 누락된 데이터가 있는지 확인하는데 유용.
print(wine.info())
print("----------------------------------------\n")

# mean = avg, std = 표준편차, min, 25% = 1사분위수, 50% = 중간값 / 2사분위수, 75% = 3사분위수, max
# 사분위수는 4등분한 퍼센티지
wine.describe()

data = wine[['alcohol','sugar','pH']].to_numpy()
target = wine['class'].to_numpy()

from sklearn.model_selection import train_test_split
# test_size=0.2 란 test set에 20%할당, defualt는 25%
train_input, test_input, train_target, test_target = train_test_split(data,target,test_size=0.2,random_state=42)

print(train_input.shape, test_input.shape)
print("----------------------------------------\n")

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(train_input)
train_scaled = ss.transform(train_input)
test_scaled = ss.transform(test_input)

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(train_scaled, train_target)
print(lr.score(train_scaled, train_target))
print("----------------------------------------\n")
print(lr.score(test_scaled, test_target))
print("----------------------------------------\n")
print(lr.coef_, lr.intercept_)

# decision tree(결정 트리)
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(train_scaled, train_target)
print(dt.score(train_scaled, train_target))
print("----------------------------------------\n")
print(dt.score(test_scaled, test_target))
print("----------------------------------------\n")
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
plt.figure(figsize=(10,7))
plot_tree(dt)
plt.show()

plt.figure(figsize=(10,7))
plot_tree(dt, max_depth=1, filled=True, feature_names=['alcohol', 'sugar', 'pH'])
plt.show()
# sugar 가 기준으로 true=left subtree, false right subtree
# gini = 불순도(impurity) : gini impurity = 1 - (음성클래스비율^2 + 양성클래스비율^2)
# samples = 총 샘플 수
# value = [] 클래스별 샘플, 0 =red(1258), 1=white(3939)

# 가치치기
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(train_scaled,train_target)
print(dt.score(train_scaled,train_target))
print(dt.score(test_scaled,test_target))

plt.figure(figsize=(20,15))
plot_tree(dt, filled=True, feature_names=['alcohol', 'sugar', 'pH'])
plt.show()

# 결정 트리 알고리즘은 표준화 전처리를 할 필요가 없다. 왜냐하면 특성값의 스케일은 결정 트리 알고리즘에 아무런 영향을 미치지 못하므로********
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(train_input, train_target)
# 위에 전처리한 값과 정확하게 같다.
print(dt.score(train_input, train_target))
print(dt.score(test_input, test_target))

# 특성 중요도 - 알코올, 당도, pH 여기서 당도가 가장 중요한 특성이라고 여김.
print(dt.feature_importances_)

plt.figure(figsize=(20,15))
plot_tree(dt, filled=True, feature_names=['alcohol', 'sugar', 'pH'])
plt.show()

# 머신러닝 모델을 종종 블랙박스와 같다고 말함. 실제로 모델의 계수나 절편이 왜 그렇게 학습되었는지 설명하기가 어렵다.
# 이에 비해 결정 트리는 비교적 비전문가에게도 설명하기 쉬운 모델을 만든다. 또한 결정 트리는 많은 앙상블 학습 알고리즘의 기반이 된다.

# 하이퍼파라미터 자동으로 찾기 위한 방법
# 교차 검증과 그리드 서치
# 테스트 세트로 일반화 성능을 올바르게 예측하려면 모델을 만들고 나서 마지막에 딱 한 번만 사용하는 것이 좋다.
# 검증 세트(validation set) : 훈련 세트를 또 나눈다.
# ex) 훈련 세트(60%), 검증 세트(20%), 테스트 세트(20%)
# 보통 20~30%를 테스트 세트와 검증 세트로 떼어 놓는다.
import pandas as pd
wine = pd.read_csv('https://bit.ly/wine_csv_data')
data = wine[['alcohol', 'sugar', 'pH']].to_numpy()
target = wine['class'].to_numpy()

from sklearn.model_selection import train_test_split
train_input, test_input, train_target, test_target = train_test_split(data,target, test_size=0.2, random_state=42)
# to create validation set
sub_input, val_input, sub_target, val_target = train_test_split(train_input, train_target, test_size=0.2, random_state=42)

print(sub_input.shape, val_input.shape)

from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(sub_input, sub_target)
print(dt.score(sub_input, sub_target))
print(dt.score(val_input, val_target))

# 교차 검증(cross validation)
# k-폴드 교차 검증 == k-겹 교차 검증
# 훈련세트를 k부분으로 나누어서 교차 검증하는 것을 의미. ex) k=2 (훈련,검증),(검증,훈련) : 여기서 검증 점수의 평균을 냄.
# 보통 k=5~10 then data upper 80~90%
# defulat k = 5
from sklearn.model_selection import cross_validate
scores = cross_validate(dt, train_input, train_target)
print(scores)
print("----------------------------------------\n")
import numpy as np
print(np.mean(scores['test_score']))

# train_test_split으로 train_input과 test_input을 나누어서 따로 섞을 필요가 없다. 
# 하지만 교차 검증을 할 때 훈련 세트를 섞으려면 분할기(splitter)를 지정해야함.
# defualt splitter = KFold 분할기 위에 코드와 아래 코드와 동일하게 동작
from sklearn.model_selection import StratifiedKFold
scores = cross_validate(dt, train_input, train_target, cv=StratifiedKFold())
print(np.mean(scores['test_score']))

splitter = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_validate(dt, train_input, train_target, cv=splitter)
print(np.mean(scores['test_score']))

# 하이퍼파라미터 튜닝
# AutoML : 하이퍼파라미터 튜닝을 자동으로 수행하는 것
# 그리드 서치(grid search) : GridSearchCB : 하이퍼파라미터 탐색과 교차 검증을 한 번에 수행
from sklearn.model_selection import GridSearchCV
params = {'min_impurity_decrease': [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]}
# default n_jobs = 1, : 병렬 실행에 사용할 cpu 코어 수 지정 : -1은 모든 코어 사용.
gs = GridSearchCV(DecisionTreeClassifier(random_state=42),params,n_jobs=-1)
# fit : 그리드 서치 객체는 결정 트리 모델 min_impurity_decrease 값을 바꿔가며 총 5번 실행한다. GridSearchCV의 cv 매개변수 default는 5이다. 그래서 총 5*5=25 수행
gs.fit(train_input,train_target)

# 5*5=25 모델 중 검증 점수가 가장 높은 모델의 매개변수 조합으로 전체 훈련 세트에서 자동으로 다시 모델을 훈련 : 그 모델 = best_estimator_
dt = gs.best_estimator_
print(dt.score(train_input, train_target))

# 최적의 매개변수
print(gs.best_params_)

# 교차 검증의 평균 점수 : 첫번째값이 가장 크다. 그래서 최적의 매개변수는 0.0001
print(gs.cv_results_['mean_test_score'])

best_index = np.argmax(gs.cv_results_['mean_test_score'])
print(gs.cv_results_['params'][best_index])

# 최적의 하이퍼파라미터 찾아가는 과정 정리
# 1. 먼저 탐색할 매개변수를 지정
# 2. 훈련 세트에서 그리드 서치를 수행하여 최상의 평균 검증 점수가 나오는 매개변수 조합을 찾는다. 이 조합은 그리드 서치 객체에 저장된다.
# 3. 그리도 서치는 최상의 매개변수에서 (교차 검증에 사용한 훈련세트가 아니라) 전체 훈련 세트를 사용해 최종 모델을 훈련한다. 이 모델도 그리드 서치 객체에 저장된다.

# min_impurity_decrease 는 노드를 분할하기 위한 불순도 감소 최소량을 지정
# np.arange() : 실수 가능, range() : only 정수
params = {'min_impurity_decrease': np.arange(0.0001, 0.001, 0.0001),
          'max_depth': range(5, 20, 1),
          'min_samples_split': range(2, 100, 10)}
# 교차 검증 횟수 : 9 * 15 * 10 = 1,350 *5(기본 5-폴드 교차검증) = 6,750
gs = GridSearchCV(DecisionTreeClassifier(random_state=42), params, n_jobs=-1)
gs.fit(train_input, train_target)

print(gs.best_params_)

print(np.max(gs.cv_results_['mean_test_score']))

# random search 사용 조건
# 매개변수의 값을 미리 정하기 어려울 때,
# 너무 많은 매개변수 조건이 있어서 그리드 서치 수행 시간이 오래 걸릴 때,

# 랜덤 값을 주어진 범위에서 고르게 뽑음. uniform : 실수, randint : 정수
from scipy.stats import uniform, randint
rgen = randint(0, 10)
rgen.rvs(10)
print(np.unique(rgen.rvs(1000), return_counts=True))

ugen = uniform(0, 1)
print(ugen.rvs(10))

# 탐색할 매개변수 범위
params = {'min_impurity_decrease': uniform(0.0001, 0.001),
          'max_depth': randint(20, 50),
          'min_samples_split': randint(2, 25),
          'min_samples_leaf': randint(1, 25)
          }

from sklearn.model_selection import RandomizedSearchCV
# 그리드 서치보다 교차 검증 수를 줄이면서 넓은 영역을 효과적으로 탐색 가능
gs = RandomizedSearchCV(DecisionTreeClassifier(random_state=42), params,
                        n_iter=100, n_jobs=-1, random_state=42)
gs.fit(train_input, train_target)

print(gs.best_params_)

print(np.max(gs.cv_results_['mean_test_score']))

dt = gs.best_estimator_
# test set 점수는 검증 세트에 대한 점수보다 조금 작은 것이 일반적
print(dt.score(test_input, test_target))

# 트리의 앙상블(ensemble of tree)
# 정형 데이터(structured data)와 비정형 데이터(unstructured data)
# 정형 : csv file에 저장된 데이터들 즉, 구조화된 데이터
# 비정형 : 데이터베이스나 엑셀로 표현하기 어려운 데이터 ex) 책과같은 텍스트 데이터, 디지털카메라로 찍은 사진, 핸드폰으로 듣는 디지털 음악 등
# structured data를 다루는데 가장 뛰어난 성과를 내는 알고리즘이 ensemble learning이다.
# 이 알고리즘은 대부분 결정 트리를 기반으로 만들어졌다.

# 비정형 데이터에는 신경망 알고리즘을 사용 : 이것으로 사진을 인식하고 텍스트를 이해하는 모델을 만들 수 있다.

# Random Forest
# 결정 트리를 랜덤하게 만들어 결정 트리 숲을 만든다. 그리고 각 결정 트리의 예측을 사용해 최종 예측을 만든다.
# bootstrap sample : ex) 1000개 가방에서 100개씩 샘플을 뽑을 때, 1개를 뽑고 1개를 다시 가방에 넣는 것을 100번 반복.

# 랜덤 포레스트는 랜덤하게 선택한 샘플과 특성을 사용하기 때문에 훈련 세트에 과대적합되는 것을 막아주고 검증 세트와 테스트 세트에서 안정적인 성능을 얻을 수 있다.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
wine = pd.read_csv('https://bit.ly/wine_csv_data')
data = wine[['alcohol', 'sugar', 'pH']].to_numpy()
target = wine['class'].to_numpy()
train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2, random_state=42)
# return_train_score =True : 검증 점수뿐만 아니라 훈련 세트에 대한 점수도 같이 반환
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_jobs=-1, random_state=42)
scores = cross_validate(rf, train_input, train_target, return_train_score=True, n_jobs=-1)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))

# 특성 중요도 : 결정 트리의 큰 장점 중 하나
rf.fit(train_input, train_target)
# 알코올, 당도, pH
print(rf.feature_importances_)

# OOB(out of bag) 샘플 : 부트스트랩 샘플에 포함되지 않고 남는 샘플
# 이 남는 샘플을 사용하여 부트스트랩 샘플로 훈련한 결정 트리를 평가할 수 있다. 마치 검증 세트 역할을 할 수 있다.
rf = RandomForestClassifier(oob_score=True, n_jobs=-1, random_state=42)
rf.fit(train_input, train_target)
print(rf.oob_score_)

# extra tree
# random forest 와 비슷하게 동작.
# 차이점 : 부트스트랩 샘플 사용 안함. 노드 분할할 때 무작위 분할, 
# 엑스트라 트리가 사용하는 결정 트리가 splitter='random'
# 랜덤 노드 분할하므로 빠른 속도가 장점
from sklearn.ensemble import ExtraTreesClassifier
et = ExtraTreesClassifier(n_jobs=-1, random_state=42)
scores = cross_validate(et, train_input, train_target, return_train_score=True, n_jobs=-1)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))
# 특성 중요도
et.fit(train_input,train_target)
print(et.feature_importances_)

# gradient boosting (기울기 높이기?)
# 결정 트리를 계속 추가하면서 가장 낮은 곳을 찾아 이동한다.
# 깊이가 얕은 결정 트리를 사용하여 이전 트리의 오차를 보완하는 방식으로 앙상블 하는 방법
# 과대적합에 강하고 일반적으로 높은 일반화 성능을 기대한다.
from sklearn.ensemble import GradientBoostingClassifier
# subsample=1.0 : 훈련 세트의 비율
gb = GradientBoostingClassifier(random_state=42)
scores = cross_validate(gb, train_input, train_target, return_train_score=True, n_jobs=-1)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))

# 학습률 증가, 트리의 개수 늘리기 => 성능 향상
gb = GradientBoostingClassifier(n_estimators=500, learning_rate=0.2, random_state=42)
scores = cross_validate(gb, train_input, train_target, return_train_score=True, n_jobs=-1)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))

gb.fit(train_input, train_target)
print(gb.feature_importances_)

# Histogram-based Gradient Boosting
# 정형 데이터를 다루는 머신러닝 알고리즘 중에 가장 인기가 높다.
# 입력 특성을 256개 구간으로 나눔. 따라서 노드를 분할할 때 최적의 분할을 매우 빠르게 찾을 수 있음
# 256개 구간 중 누락된 값을 위해서 하나를 사용함. 따라서 입력에 누락된 특성이 존재하더라도 따로 전처리할 필요 없음
# 성능을 높이려면 max_iter 매개변수를 사용
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
hgb = HistGradientBoostingClassifier(random_state=42)
scores = cross_validate(hgb, train_input, train_target, return_train_score=True)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))

# permutation_importance()
# 특성을 하나씩 랜덤하게 섞어서 모델의 성능이 변화하는지를 관찰하여 어떤 특성이 중요한지를 계산
from sklearn.inspection import permutation_importance
hgb.fit(train_input, train_target)
result = permutation_importance(hgb, train_input, train_target, n_repeats=10, n_jobs=-1, random_state=42)
# importances : 특성 중요도, importances_mean : 평균, importances_std : 표준편차
print(result.importances_mean)

result = permutation_importance(hgb, test_input, test_target, n_repeats=10, n_jobs=-1, random_state=42)
print(result.importances_mean)

# 이렇게 분석을 해서 모델을 실전에 투입했을 때, 어느 특성에 더 관심을 가질지 예상할 수 있다.

# test set 에서 성능
print(hgb.score(test_input,test_target))

# XGBoost, LightGBM(빠르고 최신 기술을 많이 적용하고 있음) 라이브러리에서도 히스토그램 기반 그레이디언트 부스팅을 사용할 수있음.
# https://xgboost.readthedocs.io/en/latest/
from xgboost import XGBClassifier
xgb = XGBClassifier(tree_method='hist',random_state=42)
scores = cross_validate(xgb, train_input, train_target, return_train_score=True)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))

# https://lightgbm.readthedocs.io/en/latest/
from lightgbm import LGBMClassifier
lgb = LGBMClassifier(random_state=42)
scores = cross_validate(lgb, train_input, train_target, return_train_score=True, n_jobs=-1)
print(np.mean(scores['train_score']), np.mean(scores['test_score']))