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
        "🎵 백색소음"
    ])

# --- 메인 타이틀 ---
st.title("📚 스터디 매니저")

# --- 메뉴별 페이지 라우팅 ---
if menu == "📝 스터디 플래너":
    st.header("📝 스터디 플래너")
    st.info("과목, 과제, 시간 관리 기능을 여기에 구현합니다.")

elif menu == "⏱️ 뽀모도로 타이머":
    st.header("⏱️ 뽀모도로 타이머")
    st.info("25분 집중 / 5분 휴식 타이머를 여기에 구현합니다.")

elif menu == "🧠 플래시카드 기능":
    st.header("🧠 플래시카드")
    st.info("질문과 답변으로 구성된 카드 학습 기능을 여기에 구현합니다.")

elif menu == "📊 리포트 보기":
    st.header("📊 리포트 보기")
    st.info("공부 시간 통계와 과목별 분석을 여기에 표시합니다.")

elif menu == "📈 성적 분석":
    st.header("📈 성적 분석")
    st.info("시험 점수 기록 및 추이 분석을 여기에 구현합니다.")

elif menu == "🎵 백색소음":
    st.header("🎵 백색소음 플레이어")
    st.write("공부할 때 집중을 도와주는 자연의 소리를 재생합니다.")

    sound_option = st.selectbox("소리 선택", ["🌊 파도 소리", "🌧️ 빗소리", "🌲 숲 소리", "📻 화이트 노이즈"])
    if sound_option == "🌊 파도 소리":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    elif sound_option == "🌧️ 빗소리":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
    elif sound_option == "🌲 숲 소리":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3")
    elif sound_option == "📻 화이트 노이즈":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3")
