import streamlit as st

st.set_page_config(page_title="스터디 매니저", layout="wide")

# --- 사이드바 메뉴 ---
menu = st.sidebar.radio("📂 메뉴 선택", [
    "스터디 플래너",
    "뽀모도로 타이머",
    "플래시카드 기능",
    "리포트 보기",
    "성적 분석",
    "백색소음 🎵"
])

# --- 상단 공통 타이틀 ---
st.title("📚 스터디 매니저")

# --- 메뉴별 페이지 라우팅 ---
if menu == "스터디 플래너":
    st.header("📝 스터디 플래너")
    # 플래너 기능 구현 예정

elif menu == "뽀모도로 타이머":
    st.header("⏱️ 뽀모도로 타이머")
    # 타이머 기능 구현 예정

elif menu == "플래시카드 기능":
    st.header("🧠 플래시카드")
    # 플래시카드 기능 구현 예정

elif menu == "리포트 보기":
    st.header("📊 리포트 보기")
    # 공부 시간 통계 그래프 등

elif menu == "성적 분석":
    st.header("📈 성적 분석")
    # 점수 입력 및 그래프 기능

elif menu == "백색소음 🎵":
    st.header("🎵 백색소음 플레이어")
    st.write("공부할 때 집중을 도와주는 자연의 소리를 재생합니다.")

    sound_option = st.selectbox("소리 선택", ["파도 소리 🌊", "빗소리 🌧️", "숲 소리 🌲", "화이트 노이즈 📻"])

    if sound_option == "파도 소리 🌊":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    elif sound_option == "빗소리 🌧️":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", format="audio/mp3")
    elif sound_option == "숲 소리 🌲":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3", format="audio/mp3")
    elif sound_option == "화이트 노이즈 📻":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3", format="audio/mp3")
