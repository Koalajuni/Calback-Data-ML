# Calback-Data-ML

### 프로젝트 현황도:  

- 데이터 자동 추출 - apache airflow  **(완료)**
- 데이터 변환  **(진행 중)**
- 데이터 적재 BigQuery Warehouse  
- 데이터 전처리 BigQuery
- 머신 러닝 트레이닝 BigQuery/Tensorflow
- 모델 분석 및 하이퍼파라미터 튜닝
- 결과  



## 배경 

<img width="1114" alt="스크린샷 2024-03-25 오후 9 32 24" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/426be9ef-6ecb-45a6-b4a3-27260b7c2a50">


1년간 운영해 온 '캘박'이란 서비스는, 사용자들에게 국내 일정을 정리해 주며 끝내 각 사용자에게 맞는 일정을 추천해 주는 서비스를 만드려고 했다. 하지만, 막상 MVP(Minimum Vialbe Product)을 만들고 검증을 해 본 결과 마켓 핏이 없다는 것을 확인할 수 있었다. 비록 일정 추천 플랫폼을 구축하진 못했지만, 서비스를 운영하면서 수 많은 데이터를 확보할 수 있었다. 앱 이벤트와 사용자 데이터를 매일 단위로 추출했던 No Sql Firebase 서비스, 마케팅을 진행하면서 수 많은 채널을 통해 홍보했던 캘박 웹사이트 링크, 유료 광고를 돌리면서 확보했던 인스타, 페이스북 마케팅 데이터.... 한 가지 아쉬웠던 점은 이 많은 데이터를 통해 제대로 된 제품 분석을 못했던 것이다. (어쩌면 데이터 분석을 미리 했더라면, 더 좋은 제품을 만들었을지도 모른다는 생각을 할 정도로 정돈된 데이터가 중요하다고 생각한다).  

따라서 Calback-Data_ML 리포지토리를 만든 이유는 비즈니스의 문제를 데이터로 풀 수 있다는 것을 직접 확인하기 위해서이다. 단순히 데이터 관련 토이 프로젝트를 만드는 것보다, 1년간 직접 쌓아온 데이터를 활용해서 인사이트를 얻으면 더 의미 있을 것 같다. 이번 프로젝트를 통해 데이터 분석의 전반적인 프로세스를 이해하고, 데이터 추출 -> 가공 -> 분석 -> (시간이 가능하면) 모델까지 적용해 볼 예정이다. 각 파트에서 사용한 프레임워크를 이해하고, 왜 사용했는지와 어떻게 적용했는지를 리드미를 통해 설명하며 프로젝트를 진행할 예정이다. 

## 데이터 엔지니어링 과정 
<img width="950" alt="스크린샷 2024-03-11 오후 8 28 19" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/d365670e-4479-42c3-b479-6ed5c51b2c13">


## 문제

**목적:** 이번 프로젝트의 목표는 캘박앱이 유저에게 어떤 가치를 제공하는지 파악하는 것이다. 

**가설:** 자주 방문하는 유저들의 행동을 통해 앞으로 들어오는 유저들의 재방문 가능성을 측정할 수 있을 것이다. 즉 자주 방문하는 사람들의 행동이 캘박이 집중해야 했던 대표 기능이자 가치일 것이다
조금 더 상세하게 가설을 세우자면, 월 3회 이상 방문한 유저를 추출하고 해당 유저들이 어떤 행동을 했는지를 분석해 볼 것이다. 

## 데이터 설정
캘박을 운영하면서 모든 데이터 처리 과정은 Firebase Firestore와 Google Analytics를 통해서 했다. 정말 편했던 부분은 Firebase를 통해 Event 마다 어떤 유저가 해당 이벤트를 실행헀는지를 알 수 있었고, 또한 코호트 별로 유저 분석이 가능해 편리했다. 하지만 이번 프로젝트에서는 Firebase에 의존하지 않고, 대규모 데이터 엔지니어링 팀의 과정을 체험하기 위해 데이터를 CSV로 옮기고 ETL 과정과 데이터 웨어하우스로 옮기는 파이프라인 과정을 다시 해볼 계획이다. 

목적을 달성하기 위해 필요한 데이터는 대부분 Firebase Database에서 추출할 수 있을 것 같다. 우선 매일 앱의 방문한 유저들의 고유 ID를 추출하고, 그 날에 해당 유저가 어떤 행동을 했는지에 대한 피처를 받아오면 될 것 같다. 현재 이 데이터들은 Firebase Database UserCollection과 MeetingCollection이라는 이름으로 받아 올 수 있으며, 유저의 행동은 앱에서 설정한 Events를 받아오면 될 것으로 보인다. 이 데이터들은 모두 한 CSV 파일로 정리할 예정이다. 

(다음은 Develoopment 버전으로 만들어 놓은 데이터베이스를 보여준다) 
<img width="720" alt="스크린샷 2024-03-13 오후 2 56 22" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/dc90929b-1d73-4ac2-afb8-3b6e1ba316d0">
<img width="1136" alt="스크린샷 2024-03-13 오후 2 57 20" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/1645e053-3ac9-484e-86a7-20b9b7479e19">

프로젝트의 파일 디렉터리는 다음과 같은 구조로 정리했다. 소스코드와 데이터를 분리해서 정리했고, 데이터 작업을 진행할 ETL과 오케스트레이션을 진행항 pipeline을 나눠서 SRC를 정리했다.
데이터가 많아지고, 각 부서별로 필요한 데이터가 많아짐에 따라 각 디렉터리 안에서도 추가로 정리해야 할 것 같긴 하지만, 가독성을 위해 간단하게만 정리했다.

<img width="449" alt="스크린샷 2024-03-14 오전 12 02 57" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/149dbbd7-8505-46cf-8e63-5de35193a654">


# 데이터 ETL
다음은 데이터 Extraction (추출), Transfer (변환), Load(로드) ETL 과정을 보여주는 이미지이다.  
<img width="616" alt="스크린샷 2024-03-11 오후 8 30 47" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/2ef62dea-eb8a-4fff-87ef-5f488aed05f4">

## 추출:
우선 데이터를 CSV 형태로 받아오기 위해 Firebase Realtime Database를 CSV 형태로 추출해야 한다. 자동화 과정에서 사용할 수 있는 여려개의 프레임워크가 있다는 것을 조사했다. 

**Apache NiFi:** 
데이터 흐름을 자동화하기 위한 오픈 소스 프로그램. 가장 대표적인 특징은 UI가 편리하고 데이터 흐름을 잘 모니터링할 수 있다는 강점이 있다.
- Flowfile Controller에서 FlowFile 형태로 데이터 전송
즉, 여러 부서로 자동화가 많은 데이터 같은 경우에 매우 편리할 것으로 판단. 

**Apache Airflow:**
에어비엔비 개발자가 오픈 소스 프로그램으로 시작한 태스크 자동화 시스템. 대표적인 특징으로 효율적인 데이터 오케스트레이션 기능을 보유하고 있다. Data orchestration: 사일로화된 데이터를 하나로 결합해 분석에 용이하게 만들어주는 자동화 방법. Data Streaming Solution로 적합하기 때문에, Data 전처리 과정으로는 사용하지 않을 계획. 
- ETF 파이프라인을 Directed Acyclic Graphs를 통해 반복적인 태스크를 실행하하면서도 순환 실행을 방지해 주는 용도.
(미리 익혀두면 좋을 것 같아서, 간단한 Airflow 코드를 사용해 매일 단위로 CSV를 형성할 수 있는 코드를 작성)

## Apache Airflow 

에어플로우 documentation을 읽고 설치하는 방법을 찾았다.
<img width="574" alt="스크린샷 2024-03-14 오후 9 03 06" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/d6906224-2c68-4c57-b70b-53049f8e10d1">

태스크가 많아지기 전까지는 standalone를 사용해도 괜찮다고 나와 있다. 따로 찾아보니 프로젝트가 크지 않을 때는, SequentialExecutor 통해서 airflow를 태스크를 실행해도 괜찮지만, 데이터가 많아지고, 프로그램이 복잡해지면서 분산 적업이나 다른 프레임워크와 사용할 수 없기 때문에 추천하지 않는다고 한다. 
조금 더 찾아보니, 나중에는 CeleryExecutor나 KubernetesExecutor 같은 프레임워크를 사용할 수 있다고 한다. 문제는 Executor 중에서 Local은 병렬처리가 안되고 클러스터 형식으로 작업을 나눌 수 없다는 것이다. 각 Executor 별로 장단점 그리고 언제 사용하는지에 대한 아주 좋은 글이 있어 참고했으며, 추후에도 내가 참고할 수 있게 링크를 첨부했다: https://magpienote.tistory.com/225. 

src/pipeline/firebase_to_csv_dag.py 파일을 통해 firebase to csv라는 DAG 객체를 만드는 스크립트를 작성했다. 처음에 코드를 작성하면서 DAG함수와 default_args dict을 만들기 때문에 자동화가 여기서 진행되는 줄 알았지만, 다큐멘터리를 확인해본 결과 단순 객체를 만드는 스크립트라고 명시되어 있었다. Directed Acyclic Graph라는 이름을 갖고 있기 때문에, 코테 준비하면서 배운 Graph 자료구조가 떠올랐다. 여기서 유추해볼 수 있었던 부분은 DAG 객체 안에서 여러가지 태스크가 있을텐데 이런 태스크들이 그래프 안에 있는 노드라고 생각하면 될 것 같고, 우리가 그 순서와 방향을 정해준다는 느낌을 받았다. 캘박 데이터로 따지면, 해볼 수 있을 만한 몇가지 태스크는 매일 로그인한 유저들의 데이터를 추출하고, 이후 meetingsCollection과 events를 추출해 하나의 csv 파일로 담는 스케줄링을 진행할 수 있을 것 같다. 

또한 여기서 느낀 점은 데이터 태스크가 많아지고, 스케줄링을 많이 할 수록 모든 작업이 정상적으로 작동되는지 모니터링하고 디버깅 해주는 작업이 정말 중요할 것 같다는 생각이다. 특히 데이터가 정말 많을 경우 문제가 생길 수 있기 때문에 태스크 디자인할 때 유의해야 할 것으로 보인다. 위에 예시에서 만약 userCollection을 먼저 처리하지 않고, Event나 meetingsCollection을 추출하게 되면 나중에 데이터를 전환하거나, 자동으로 처리할 때 큰 문제가 생길 수 있겠다는 생각이 들었다. 실수를 하지 않기 위해 airflow best practices를 자주 참고해야겠다. 실무에서는 어떤 에러들이 많은지 조금 더 확인하기 위해 찾아보니 Buzz님께서 친절하게 알려주신 블로그가 있어 링크를 첨부했다: https://medium.com/29cm/29cm-apache-airflow-%EC%9A%B4%EC%98%81%EA%B8%B0-da6b5535f7a6 
위에 블로그에서도 Queue 무한 대기 문제가 있었으며, CelerExecutor와 Scheduler 사이에 통신 에러 때문에 일어났다고 적혀있다. 버전 업그레이드 이후 해결 됐다고 하지만, 이러한 문제를 미리 대비하기 위해 디버깅이 중요성을 보여주는 것 같다. 

## 버그 1
firebase_to_csv function이 잘 돌아가는지 확인하기 위해 실행시켜본 결과, raw data 디렉터리로 유저들의 정보가 담겨진 csv 파일이 잘 만들어졌다. 
코드는 정상적으로 작동이 됐지만, DAG를 실행해 본 결과 다음과 같은 버그가 생겼다. 

<img width="1173" alt="스크린샷 2024-03-17 오후 4 45 05" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/f92b3682-b489-4b0e-b5dd-60080de74c52">

에러 문구를 확인해 본 결과 export_to_csv 함수에서 output_csv_path 패러미터가 안 읽혀진다는 것을 볼 수 있었다. firebase_to_csv에서는 잘 작동 됐기 때문에,  DAG가 실행되는 방식에서 버그가 일어나고 있다는 것을 인지할 수 있었다.
DAG에서 Export Task Operator를 확인해 보니, python_callable = export_to_csv만 실행하고, 패러미터를 추가하지 않은 것을 확인할 수 있었고, 아래 op_kwargs= {path}로 수정한 후 정상적으로 DAG가 작동되는 것을 볼 수 있었다.

<img width="782" alt="스크린샷 2024-03-17 오후 4 56 40" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/c51fc7da-2713-43a4-9038-2f908f019fd7">


왜 이런 실수를 했을까 고민을 한 후 다음과 같은 이유를 깨달을 수 있었다. 

(1) DAG Bash Operator, DAG Python Operator에 Documentation에서 op_kwargs 변수를 확인하지 못했던 실수.

(2) DAG 코드에서 디버깅을 추가하지 못했던 실수 

익숙하지 않더라도 차근차근히 읽다보면 충분히 만회할 수 있던 실수인 것 같아서, 다음에는 조금 더 꼼꼼히 프로젝트를 진행해야겠다는 다짐을 했다. 
심지어 문서에서는 @task decorator를 사용하는 것을 권장했었는데, 이 버그를 겪고 나서야 왜 이 방법이 나은지 알 수 있었다. @task로 코드를 작성하면 파이썬에서 사용하는 형식 def export_to_csv(ds=None, **kwargs)으로 코드를 작성할 수 있기 때문이다. 하지만 Task가 많아지면 지저분해 보일 수 있다는 것이 문제일 것 같다. 

## 에어플로우 실행결과 

airflow webserver를 통해 태스크들이 잘 작동되고 있는지 확인할 수 있었다. 

<img width="1392" alt="스크린샷 2024-03-25 오후 9 08 46" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/72a058e2-55ba-4b47-8857-6d39956d0500">

폴더 디렉터리를 확인해 본 결과, 3만개가 넘는 row의 데이터가 있는 output.csv파일이 성공적으로 잘 작동되는 것을 볼 수 있다. 

<img width="578" alt="스크린샷 2024-03-25 오후 9 16 17" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/05b2f41e-355c-4809-a74e-39690e26f740">


**웨어하우스 선택 로직:**

데이터웨하우스는 구글의 BigQuery(BQ)를 선택했다. BQ를 선택한 대표적인 이유는 플러터, 파이어베이스, 구글 애널리틱스 추후 텐서플로우와 같은 프레임워크를 연동해서 사용하기 용이하게 위해서였다. 스타트업으로써 빠르게 저렴한 가격으로 데이터 파이프라인을 구축하고 머신 러닝 모델링까지 하기 좋은 웨어하우스인 것 같으나, 만약 캘박이 더 큰 플랫폼으로 성장하고 데이터양이 기하급수적으로 늘어난다고 했을 시, AWS 데이터베이스를 사용하면서 더 정교한 큐리를 사용할 수 있는 Amazon RedShift나 다양한 클라우드 서비스를 통합으로 사용할 수 있는 Snowflake을 사용했을 것 같다.     

# 데이터 변환 Transformation (진행 중) 

이제 데이터 웨하우스에 있는 수 많은 데이터를 원하는 형식으로 전환하는 적업을 할 예정이다. 
생각보다 많은 시간을 계획하는 데만 사용해 머리가 아팠지만, 여기서 데이터를 잘못 전환하면 나중에 더 힘들어질 수 있기 때문에 최대한 로지컬하게 데이터를 정리해 봤다. 아래는 지금 추출한 데이터를 정리한 도형이다. 나중에 모델링 하거나 BI 만들 때 편리할 수 있게 정리했으며, 날짜별로 특정 사용자가 진행한 행동을 나타날 수 있는 테이블로 전환할 계획이다. 

![IMG_22696B80EE14-1](https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/922a29a2-d8e4-4917-ada4-08e725045b01 )

<img src="[https://github.com/favicon.ico](https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/922a29a2-d8e4-4917-ada4-08e725045b01)https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/922a29a2-d8e4-4917-ada4-08e725045b01" width="100">







