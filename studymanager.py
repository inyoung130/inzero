import streamlit as st
from datetime import datetime
import pandas as pd
import random

# 오늘의 명언 리스트 (필요시 전체 20개까지 확장 가능)
quotes = [
    "성공은 우연이 아니다. 노력과 인내의 결과다. – 펠레",
    "지식에 대한 투자는 최고의 보상을 가져다 준다. – 벤자민 프랭클린",
    "노력을 대신할 수 있는 것은 없습니다. – 토마스 에디슨",
    "탁월함은 기술이 아니다. 태도입니다. – 랄프 마스턴",
    "끝날 때까지 항상 불가능해 보인다 – 넬슨 만델라"
]

# 오늘의 명언 랜덤 선택
today_quote = random.choice(quotes)

# 사이드바 설정
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
        "🎶 MUSIC"
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

# ---------------- 뽀모도로 타이머 ----------------
if menu == "⏱️ 뽀모도로 타이머":
    st.header("⏱️ 뽀모도로 타이머")

    import time  # 타이머 작동용

    # 상태 초기화
    if "pomo_phase" not in st.session_state:
        st.session_state.pomo_phase = "Pomodoro"
        st.session_state.time_left = 25 * 60
        st.session_state.running = False
        st.session_state.pomo_count = 0

    # 남은 시간 계산
    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60
    time_display = f"{minutes:02d}:{seconds:02d}"

    # 현재 단계 표시
    st.markdown(f"### 🔄 현재 단계: **{st.session_state.pomo_phase}**")

    # ⏳ 타이머 크게 표시
    st.markdown(
        f"<h1 style='text-align: center; font-size: 80px;'>{time_display}</h1>",
        unsafe_allow_html=True
    )

    # 버튼 정렬
    col1, col2, col3 = st.columns(3)
    with col1:
        if not st.session_state.running:
            if st.button("▶ 시작"):
                st.session_state.running = True
        else:
            if st.button("⏹ 정지"):
                st.session_state.running = False

    with col2:
        if st.button("🔄 초기화"):
            st.session_state.pomo_phase = "Pomodoro"
            st.session_state.time_left = 25 * 60
            st.session_state.running = False
            st.session_state.pomo_count = 0

    with col3:
        st.write(f"✔️ 완료 세션: `{st.session_state.pomo_count}`")

    # 타이머 작동
    if st.session_state.running:
        if st.session_state.time_left > 0:
            st.session_state.time_left -= 1
            time.sleep(1)
            st.experimental_rerun()
        else:
            # 타이머 종료 → 다음 단계로 전환
            if st.session_state.pomo_phase == "Pomodoro":
                st.session_state.pomo_count += 1
                if st.session_state.pomo_count % 4 == 0:
                    st.session_state.pomo_phase = "Long Break"
                    st.session_state.time_left = 15 * 60
                else:
                    st.session_state.pomo_phase = "Short Break"
                    st.session_state.time_left = 5 * 60
            else:
                st.session_state.pomo_phase = "Pomodoro"
                st.session_state.time_left = 25 * 60

            st.session_state.running = False
            st.experimental_rerun()


# ---------------- 기타 메뉴 ----------------

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
