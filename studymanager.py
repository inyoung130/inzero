import streamlit as st
from datetime import datetime

# --- 페이지 설정 ---
st.set_page_config(page_title="스터디 매니저", layout="wide")

# --- 오늘의 명언 리스트 ---
quotes = [
    "성공은 우연이 아니다. 노력, 인내, 배움, 공부, 희생, 그리고 무엇보다 자신이 하고 있는 일에 대한 사랑, 하는 법을 배우는 것이다. – 펠레",
    "지식에 대한 투자는 최고의 보상을 가져다 줄 것이다. – 벤자민 프랭클린",
    "많은 실패자들은 포기하기 때문에 성공이 얼마나 가까웠는지 깨닫지 못합니다. – 토마스 에디슨",
    "미루는 것은 쉬운 일을 어렵게 만들고 어려운 일을 더 어렵게 만든다. – 메이슨 쿨리",
    "노력을 대신할 수 있는 것은 없습니다. – 토마스 에디슨",
    "더 이상 상황을 바꿀 수 없을 때 우리는 스스로를 변화시켜야 합니다. – 빅터 프랭클",
    "훌륭한 사람은 레이저 같은 집중력을 가진 평범한 사람입니다. – 브루스 리",
    "진짜 어려움은 극복할 수 있습니다. 정복할 수 없는 것은 상상 속의 것들뿐이다. – 시어도어 N. 베일",
    "탁월함은 기술이 아니다. 태도입니다. – 랄프 마스턴",
    "성적이나 결과는 행동이 아니라 습관입니다. – 아리스토텔레스",
    "미래는 꿈의 아름다움을 믿는 자의 것입니다. – 엘리너 루즈벨트",
    "더 많이 읽을수록 더 많은 것을 알게 될 것이고 더 많이 배울수록 더 많은 곳을 가게 될 것입니다. – 닥터 수스",
    "끝날 때까지 항상 불가능해 보인다 – 넬슨 만델라",
    "성공의 비결은 없습니다. 성공은 준비와 노력, 실패에서 배운 결과입니다. – 콜린 파월",
    "성공으로 가는 엘리베이터는 없습니다. 성공은 계단을 통해서만 도달할 수 있습니다. – 지그 지글러",
    "네 내면에서 ‘그림을 그릴 수 없다’는 소리가 들리면 반드시 그림을 그리십시오. 그러면 그 목소리는 잠잠해질 것입니다. – 빈센트 반 고흐",
    "열심히 하면 할수록 행운도 더 많이 옵니다. – 토마스 제퍼슨",
    "진짜 가치가 있는 곳으로 가는 지름길은 없습니다. – 비벌리 실스",
    "너의 꿈들을 잃지 마라. 무엇이든 성취하기 위해서는 믿음, 비전, 노력, 결단력, 헌신이 필요합니다. – 게일 데버스",
    "제가 하는 가장 큰 후회는 한 단어로 요약할 수 있는데, 그것은 ‘미루기’ 입니다. – 론 쿠퍼"
]

# --- 현재 시간 기준으로 10분 간격 명언 선택 ---
now = datetime.now()
quote_index = (now.hour * 6 + now.minute // 10) % len(quotes)
today_quote = quotes[quote_index]

# --- 사이드바 구성 ---
with st.sidebar:
    st.markdown("### ✨ 오늘의 명언")
    st.markdown(f"> _{today_quote}_")

    st.markdown("---")
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    menu = st.radio("📂 메뉴 선택", [
        "📝 스터디 플래너",
        "⏱️ 뽀모도로 타이머",
        "🧠 플래시카드 기능",
        "📊 리포트 보기",
        "📈 성적 분석",
        "🎶 MUSIC"
    ])

# --- 메인 타이틀 ---
st.title("📚 스터디 매니저")

# --- 메뉴별 페이지 라우팅 ---
if menu == "📝 스터디 플래너":
    st.header("📝 스터디 플래너")
    st.info("과목별 과제, 시간 관리에 효과적👌")
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📝 스터디 플래너", layout="wide")
st.title("📝 스터디 플래너 (타이머 포함)")

NUM_TASKS = 10  # 과제 수

# 세션 상태 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = [{
        "name": "",
        "started": False,
        "start_time": None,
        "end_time": None,
        "duration": ""
    } for _ in range(NUM_TASKS)]

# 각 과제에 대해 입력 및 타이머 구현
for i in range(NUM_TASKS):
    st.markdown(f"### 📚 과제 {i + 1}")
    col1, col2 = st.columns([4, 1])

    # 과제명 입력
    with col1:
        task_name = st.text_input("과제 이름", value=st.session_state.tasks[i]["name"], key=f"task_name_{i}")
        st.session_state.tasks[i]["name"] = task_name

    # 타이머 시작 버튼
    if not st.session_state.tasks[i]["started"]:
        if col2.button("▶ 시작", key=f"start_{i}") and task_name.strip() != "":
            st.session_state.tasks[i]["start_time"] = datetime.now()
            st.session_state.tasks[i]["started"] = True
            st.session_state.tasks[i]["end_time"] = None
            st.session_state.tasks[i]["duration"] = ""
            st.success(f"{task_name} 시작!")

    # 타이머 종료 버튼
    if st.session_state.tasks[i]["started"]:
        if col2.button("⏹ 종료", key=f"stop_{i}"):
            end_time = datetime.now()
            start_time = st.session_state.tasks[i]["start_time"]
            duration = end_time - start_time
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            formatted = f"{hours}시간 {minutes}분 {seconds}초"

            st.session_state.tasks[i]["end_time"] = end_time
            st.session_state.tasks[i]["duration"] = formatted
            st.session_state.tasks[i]["started"] = False
            st.success(f"{task_name} 종료 - 소요 시간: {formatted}")

    # 상태 출력
    if st.session_state.tasks[i]["duration"]:
        st.info(f"⏱️ 소요 시간: {st.session_state.tasks[i]['duration']}")
    elif st.session_state.tasks[i]["started"]:
        st.warning("⏳ 진행 중...")

# --- 요약 테이블 ---
st.markdown("---")
st.subheader("📋 오늘의 과제 요약")

summary = []
for task in st.session_state.tasks:
    if task["name"].strip():
        summary.append({
            "과제명": task["name"],
            "소요 시간": task["duration"] if task["duration"] else ("진행 중" if task["started"] else "")
        })

if summary:
    import pandas as pd
    df = pd.DataFrame(summary)
    st.dataframe(df)
else:
    st.write("과제를 입력하고 타이머를 사용해보세요.")


elif menu == "⏱️ 뽀모도로 타이머":
    st.header("⏱️ 뽀모도로 타이머")
    st.info("25분 집중 / 5분 휴식 타이머")

elif menu == "🧠 플래시카드 기능":
    st.header("🧠 플래시카드")
    st.info("카드 학습 기능")

elif menu == "📊 리포트 보기":
    st.header("📊 리포트 보기")
    st.info("공부 시간 통계와 과목별 분석")

elif menu == "📈 성적 분석":
    st.header("📈 성적 분석")
    st.info("시험 점수 기록 및 분석")

elif menu == "🎶 MUSIC":
    st.header("🎶 MUSIC 플레이어")
    st.info("잔잔한 클래식 음악으로 집중력UP 성적UP")

    classical_choice = st.selectbox("🎼 클래식 곡 선택", [
        "🎵 Slow Motion – Bensound",
        "🎵 Better Days – Bensound",
        "🎵 Tenderness – Bensound",
        "🎵 Mozart - Piano Sonata",
        "🎵 Chopin - Nocturne"
    ])

    if "Slow Motion" in classical_choice:
        st.audio("https://www.bensound.com/bensound-music/bensound-slowmotion.mp3")
    elif "Better Days" in classical_choice:
        st.audio("https://www.bensound.com/bensound-music/bensound-betterdays.mp3")
    elif "Tenderness" in classical_choice:
        st.audio("https://www.bensound.com/bensound-music/bensound-tenderness.mp3")
    elif "Mozart" in classical_choice:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3")
    elif "Chopin" in classical_choice:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3")
