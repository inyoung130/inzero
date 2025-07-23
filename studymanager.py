import streamlit as st
from datetime import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="스터디 매니저", layout="wide")
st.title("📚 스터디 매니저")

# 명언 출력
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
]
now = datetime.now()
quote_index = (now.hour * 6 + now.minute // 10) % len(quotes)
today_quote = quotes[quote_index]

# 사이드바
import streamlit as st
from datetime import datetime
import pandas as pd

# 사이드바: 명언 + 메뉴 선택
with st.sidebar:
    st.markdown("### ✨ 오늘의 명언")
    st.markdown(f"> _{today_quote}_")
    st.markdown("---")

menu = st.radio("📂 메뉴 선택", [
    "📝 스터디 플래너",
    "⏱️ 뽀모도로 타이머",
    "🧠 플래시카드 기능",
    "📊 리포트 보기",
    "📈 성적 분석",
    "🎶 MUSIC"   # 이 이름을 코드 내부 if 조건문과 정확히 맞춰야 함 
])

# ---------------- 스터디 플래너 ----------------
if menu == "📝 스터디 플래너":
    st.header("📝 스터디 플래너")

    # 과제 리스트 초기화
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # 과제 추가 폼
    with st.form("study_planner_form"):
        subject = st.selectbox("과목 선택", ["국어", "수학", "영어", "사회", "과학", "한국사", "직접 추가"])
        if subject == "직접 추가":
            subject = st.text_input("직접 입력한 과목명", key="custom_subject")
        task_name = st.text_input("과제명 입력")
        submitted = st.form_submit_button("✅ 과제 추가")
        if submitted and task_name.strip() and subject.strip():
            st.session_state.tasks.append({
                "subject": subject.strip(),
                "task": task_name.strip(),
                "start_time": None,
                "end_time": None,
                "duration": "",
                "started": False
            })
            st.success(f"'{subject}' 과목의 '{task_name}' 과제를 추가했습니다.")

    # 과제 목록 + 타이머 + 삭제
    st.subheader("📋 과제 목록 (타이머 포함)")
    if st.session_state.tasks:
        delete_index = None
        for i, task in enumerate(st.session_state.tasks):
            with st.expander(f"{task['subject']} - {task['task']}"):
                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    if task["duration"]:
                        st.info(f"⏱️ 소요 시간: {task['duration']}")
                    elif task["started"]:
                        st.warning("⏳ 진행 중...")

                with col2:
                    if not task["started"]:
                        if st.button("▶ 시작", key=f"start_{i}"):
                            task["start_time"] = datetime.now()
                            task["started"] = True
                            task["end_time"] = None
                            task["duration"] = ""
                            st.success("공부 시작!")
                    else:
                        if st.button("⏹ 종료", key=f"stop_{i}"):
                            end_time = datetime.now()
                            start_time = task["start_time"]
                            duration = end_time - start_time
                            total_sec = int(duration.total_seconds())
                            h = total_sec // 3600
                            m = (total_sec % 3600) // 60
                            s = total_sec % 60
                            formatted = f"{h}시간 {m}분 {s}초"
                            task["end_time"] = end_time
                            task["duration"] = formatted
                            task["started"] = False
                            st.success(f"공부 종료 - {formatted}")

                with col3:
                    if st.button("🗑️ 삭제", key=f"delete_{i}"):
                        delete_index = i

        if delete_index is not None:
            deleted = st.session_state.tasks.pop(delete_index)
            st.success(f"'{deleted['subject']}' 과목의 '{deleted['task']}' 과제를 삭제했습니다.")
    else:
        st.info("과제가 아직 없습니다. 먼저 추가해보세요!")

    # 공부 요약 테이블
    st.markdown("---")
    st.subheader("📊 오늘의 공부 요약")

    summary_data = [
        {
            "과목": task["subject"],
            "과제명": task["task"],
            "소요 시간": task["duration"] if task["duration"] else ("진행 중" if task["started"] else "")
        }
        for task in st.session_state.tasks
    ]

    if summary_data:
        df = pd.DataFrame(summary_data)
        st.dataframe(df)
    else:
        st.write("아직 등록된 과제가 없습니다.")



# ---------------- 기타 메뉴 ----------------
if menu == "⏱️ 뽀모도로 타이머":
    st.header("⏱️ 뽀모도로 타이머")
    st.info("이 기능은 곧 추가될 예정입니다.")

elif menu == "🧠 플래시카드 기능":
    st.header("🧠 플래시카드 기능")
    st.info("이 기능은 곧 추가될 예정입니다.")

elif menu == "📊 리포트 보기":
    st.header("📊 리포트 보기")
    st.info("이 기능은 곧 추가될 예정입니다.")

elif menu == "📈 성적 분석":
    st.header("📈 성적 분석")
    st.info("이 기능은 곧 추가될 예정입니다.")

elif menu == "🎶 MUSIC":
    st.header("🎶 MUSIC 플레이어")
    music = st.selectbox("🎼 클래식 곡 선택", [
        "🎵 Slow Motion – Bensound",
        "🎵 Better Days – Bensound",
        "🎵 Tenderness – Bensound",
        "🎵 Mozart - Piano Sonata",
        "🎵 Chopin - Nocturne"
    ])
    if "Slow Motion" in music:
        st.audio("https://www.bensound.com/bensound-music/bensound-slowmotion.mp3")
    elif "Better Days" in music:
        st.audio("https://www.bensound.com/bensound-music/bensound-betterdays.mp3")
    elif "Tenderness" in music:
        st.audio("https://www.bensound.com/bensound-music/bensound-tenderness.mp3")
    elif "Mozart" in music:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3")
    elif "Chopin" in music:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3")
