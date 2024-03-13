# Calback-Data-ML (진행 중) 

**배경**

1년간 운영해 온 '캘박'이란 서비스는, 사용자들에게 국내 일정을 정리해 주며 끝내 각 사용자에게 맞는 일정을 추천해 주는 서비스를 만드려고 했다. 하지만, 막상 MVP(Minimum Vialbe Product)을 만들고 검증을 해 본 결과 마켓 핏이 없다는 것을 확인할 수 있었다. 비록 일정 추천 플랫폼을 구축하진 못했지만, 서비스를 운영하면서 수 많은 데이터를 확보할 수 있었다. 앱 이벤트와 사용자 데이터를 매일 단위로 추출했던 No Sql Firebase 서비스, 마케팅을 진행하면서 수 많은 채널을 통해 홍보했던 캘박 웹사이트 링크, 유료 광고를 돌리면서 확보했던 인스타, 페이스북 마케팅 데이터.... 한 가지 아쉬웠던 점은 이 많은 데이터를 통해 제대로 된 제품 분석을 못했던 것이다. (어쩌면 데이터 분석을 미리 했더라면, 더 좋은 제품을 만들었을지도 모른다는 생각을 할 정도로 정돈된 데이터가 중요하다고 생각한다).  

따라서 Calback-Data_ML 리포지토리를 만든 이유는 비즈니스의 문제를 데이터로 풀 수 있다는 것을 직접 확인하기 위해서이다. 단순히 데이터 관련 토이 프로젝트를 만드는 것보다, 1년간 직접 쌓아온 데이터를 활용해서 인사이트를 얻으면 더 의미 있을 것 같다. 이번 프로젝트를 통해 데이터 분석의 전반적인 프로세스를 이해하고, 데이터 추출 -> 가공 -> 분석 -> (시간이 가능하면) 모델까지 적용해 볼 예정이다. 각 파트에서 사용한 프레임워크를 이해하고, 왜 사용했는지와 어떻게 적용했는지를 리드미를 통해 설명하며 프로젝트를 진행할 예정이다. 

# 데이터 엔지니어링 과정 
<img width="950" alt="스크린샷 2024-03-11 오후 8 28 19" src="https://github.com/Koalajuni/Calback-Data-ML/assets/98198915/d365670e-4479-42c3-b479-6ed5c51b2c13">


**문제**

**목적:** 이번 프로젝트의 목적은 데이터로 캘박이 어떤 가치를 제공하는지 파악하는 것이다. 

**가설:** 자주 방문하는 유저들의 행동을 통해 앞으로 들어오는 유저들의 재방문 가능성을 측정할 수 있을 것이다. 즉 자주 방문하는 사람들의 행동이 캘박이 집중해야 했던 대표 기능이자 가치일 것이다
조금 더 상세하게 가설을 세우자면, 월 3회 이상 방문한 유저를 추출하고 해당 유저들이 어떤 행동을 했는지를 분석해 볼 것이다. 

**데이터 설정**
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

**추출:**
우선 데이터를 CSV 형태로 받아오기 위해 Firebase Realtime Database를 CSV 형태로 추출해야 한다. 자동화 과정에서 사용할 수 있는 여려개의 프레임워크가 있다는 것을 조사했다. 
**Apache NiFi:** 
데이터 흐름을 자동화하기 위한 오픈 소스 프로그램. 가장 대표적인 특징은 UI가 편리하고 데이터 흐름을 잘 모니터링할 수 있다는 강점이 있다.
- Flowfile Controller에서 FlowFile 형태로 데이터 전송
즉, 여러 부서로 자동화가 많은 데이터 같은 경우에 매우 편리할 것으로 판단. 

**Apache Airflow:**
에어비엔비 개발자가 오픈 소스 프로그램으로 시작한 태스크 자동화 시스템. 대표적인 특징으로 효율적인 데이터 오케스트레이션 기능을 보유하고 있다. Data orchestration: 사일로화된 데이터를 하나로 결합해 분석에 용이하게 만들어주는 자동화 방법. Data Streaming Solution로 적합하기 때문에, Data 전처리 과정으로는 사용하지 않을 계획. 
- ETF 파이프라인을 Directed Acyclic Graphs를 통해 반복적인 태스크를 실행하하면서도 순환 실행을 방지해 주는 용도.
(미리 익혀두면 좋을 것 같아서, 간단한 Airflow 코드를 사용해 매일 단위로 CSV를 형성할 수 있는 코드를 작성)



  



**웨어하우스 선택 로직:**

데이터웨하우스는 구글의 BigQuery(BQ)를 선택했다. BQ를 선택한 대표적인 이유는 플러터, 파이어베이스, 구글 애널리틱스 추후 텐서플로우와 같은 프레임워크를 연동해서 사용하기 용이하게 위해서였다. 스타트업으로써 빠르게 저렴한 가격으로 데이터 파이프라인을 구축하고 머신 러닝 모델링까지 하기 좋은 웨어하우스인 것 같으나, 만약 캘박이 더 큰 플랫폼으로 성장하고 데이터양이 기하급수적으로 늘어난다고 했을 시, AWS 데이터베이스를 사용하면서 더 정교한 큐리를 사용할 수 있는 Amazon RedShift나 다양한 클라우드 서비스를 통합으로 사용할 수 있는 Snowflake을 사용했을 것 같다.     






