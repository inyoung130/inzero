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


# 테마 색상 선택
st.sidebar.markdown("---")
st.sidebar.markdown("🎨 **테마 색상 설정**")

theme_color = st.sidebar.color_picker("배경 색 선택", "#F0F2F6")  # 기본 배경색은 Streamlit 기본값

# CSS로 배경색 적용
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {theme_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("---")
st.markdown("🗑️ **전체 기록 초기화**")
if st.button("초기화 실행"):
    for key in ["tasks", "grades", "flashcards"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("✅ 모든 기록이 초기화되었습니다. 페이지를 새로고침 해주세요.")

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

    import time

    # 초기 세션 상태 설정
    if "pomo_phase" not in st.session_state:
        st.session_state.pomo_phase = "Pomodoro"
        st.session_state.time_left = 25 * 60
        st.session_state.running = False
        st.session_state.pomo_count = 0

    # 시간 계산
    minutes = st.session_state.time_left // 60
    seconds = st.session_state.time_left % 60
    time_display = f"{minutes:02d}:{seconds:02d}"

    # 단계 및 타이머 출력
    st.markdown(f"### 🔄 현재 단계: **{st.session_state.pomo_phase}**")
    st.markdown(
        f"<h1 style='text-align: center; font-size: 80px; color: #FF4B4B'>{time_display}</h1>",
        unsafe_allow_html=True
    )

    # 버튼 UI 구성
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
        st.metric("✅ 완료 세션", st.session_state.pomo_count)

    # 타이머 작동
    if st.session_state.running:
        if st.session_state.time_left > 0:
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()
        else:
            # 타이머 완료 시 단계 전환
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
            st.rerun()

# ---------------- 플래시카드 기능 ----------------
import random

if menu == "🧠 플래시카드 기능":
    st.header("🧠 플래시카드 학습")

    # 상태 초기화
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = {}
    if "current_category" not in st.session_state:
        st.session_state.current_category = "기본"
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    # 카테고리 선택 또는 추가
    categories = list(st.session_state.flashcards.keys())
    if "기본" not in categories:
        categories.insert(0, "기본")

    selected_category = st.selectbox("📁 카테고리 선택", categories + ["➕ 새 카테고리 추가"])
    if selected_category == "➕ 새 카테고리 추가":
        new_category = st.text_input("새 카테고리 이름")
        if st.button("📂 카테고리 생성") and new_category:
            st.session_state.flashcards[new_category] = []
            st.session_state.current_category = new_category
            st.success(f"'{new_category}' 카테고리가 생성되었습니다.")
    else:
        st.session_state.current_category = selected_category
        if selected_category not in st.session_state.flashcards:
            st.session_state.flashcards[selected_category] = []

    # 카드 추가
    st.markdown("### ➕ 플래시카드 추가")
    with st.form("add_card_form"):
        question = st.text_input("앞면 (질문)")
        answer = st.text_input("뒷면 (답변)")
        submitted = st.form_submit_button("➕ 추가")
        if submitted and question.strip() and answer.strip():
            st.session_state.flashcards[st.session_state.current_category].append({
                "question": question.strip(),
                "answer": answer.strip()
            })
            st.success("✅ 카드가 추가되었습니다.")

    st.markdown("---")

    # 카드 리스트
    cards = st.session_state.flashcards.get(st.session_state.current_category, [])

    if cards:
        # 카드 셔플 여부
        if st.checkbox("🔀 카드 순서 섞기", key="shuffle_cards"):
            random.shuffle(cards)

        # 현재 카드
        card = cards[st.session_state.current_index]
        st.subheader(f"📌 카드 {st.session_state.current_index + 1} / {len(cards)}")
        st.markdown(f"**앞면:** {card['question']}")

        if st.session_state.show_answer:
            st.markdown(f"✅ **뒷면:** {card['answer']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👀 정답 보기"):
                st.session_state.show_answer = True
        with col2:
            if st.button("➡️ 다음 카드"):
                st.session_state.current_index = (st.session_state.current_index + 1) % len(cards)
                st.session_state.show_answer = False
        with col3:
            if st.button("🗑️ 카드 삭제"):
                deleted = cards.pop(st.session_state.current_index)
                st.success(f"'{deleted['question']}' 카드가 삭제되었습니다.")
                st.session_state.current_index = 0
                st.session_state.show_answer = False
    else:
        st.info("아직 이 카테고리에 카드가 없습니다. 위에서 추가해보세요.")

# ---------------- 리포트 보기 ----------------
if menu == "📊 리포트 보기":
    st.header("📊 학습 리포트")

    if "tasks" not in st.session_state or not st.session_state.tasks:
        st.info("아직 학습 기록이 없습니다. 스터디 플래너에서 과제를 추가하고 공부해보세요.")
    else:
        # duration 있는 과제만 필터링
        report_data = []
        for task in st.session_state.tasks:
            if task["duration"]:
                try:
                    h = int(task["duration"].split("시간")[0].strip())
                    m = int(task["duration"].split("시간")[1].split("분")[0].strip())
                    s = int(task["duration"].split("분")[1].split("초")[0].strip())
                    total_seconds = h * 3600 + m * 60 + s
                except:
                    total_seconds = 0

                report_data.append({
                    "과목": task["subject"],
                    "과제명": task["task"],
                    "소요 시간": task["duration"],
                    "초": total_seconds
                })

        if report_data:
            df = pd.DataFrame(report_data)

            st.subheader("✅ 과목별 누적 공부 시간 (분 단위)")
            subject_summary = df.groupby("과목")["초"].sum().sort_values(ascending=False)
            st.bar_chart(subject_summary // 60)

            st.subheader("📋 전체 과제 요약")
            st.dataframe(df[["과목", "과제명", "소요 시간"]])

            st.subheader("🏆 가장 오래 공부한 과제 Top 3")
            top3 = df.sort_values(by="초", ascending=False).head(3).reset_index(drop=True)
            for i, row in top3.iterrows():
                st.markdown(f"**{i+1}위. {row['과목']} - {row['과제명']}**  \n🕒 {row['소요 시간']}")

        else:
            st.warning("기록된 공부 시간이 있는 과제가 없습니다.")

# ---------------- 성적 분석 ----------------
if menu == "📈 성적 분석":
    st.header("📈 성적 분석")

    if "grades" not in st.session_state:
        st.session_state.grades = []

    st.subheader("➕ 성적 입력")
    with st.form("grade_form"):
        subject = st.selectbox("과목", ["국어", "수학", "영어", "사회", "과학", "한국사", "기타"])
        test_name = st.text_input("시험 이름 (예: 1차 중간고사)")
        score = st.number_input("실제 점수 (0 ~ 100)", min_value=0, max_value=100, step=1)
        goal = st.number_input("목표 점수 (0 ~ 100)", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("✅ 저장")
        if submitted and test_name.strip():
            st.session_state.grades.append({
                "과목": subject,
                "시험": test_name.strip(),
                "점수": score,
                "목표": goal,
                "차이": score - goal
            })
            st.success(f"'{subject}'의 '{test_name}' 점수 {score}점 (목표 {goal}점)이 저장되었습니다.")

    st.markdown("---")

    # 분석 영역
    if st.session_state.grades:
        df = pd.DataFrame(st.session_state.grades)

        st.subheader("📊 과목별 평균 점수")
        st.bar_chart(df.groupby("과목")["점수"].mean().sort_values(ascending=False))

        st.subheader("📈 시험별 점수 입력 내역")
        st.dataframe(df[["과목", "시험", "점수", "목표", "차이"]])

        st.subheader("📉 목표 점수 대비 차이")
        chart_data = df[["시험", "차이"]].set_index("시험")
        st.bar_chart(chart_data)

        st.subheader("📌 점수 미달 시험")
        under_goal = df[df["차이"] < 0]
        if not under_goal.empty:
            st.warning("다음 시험들은 목표 점수에 미달했습니다:")
            for _, row in under_goal.iterrows():
                st.markdown(f"- ❌ **{row['과목']} - {row['시험']}**: 목표보다 {abs(row['차이'])}점 낮음")
        else:
            st.success("🎉 모든 시험에서 목표를 달성했어요!")

        st.subheader("🏅 최고 점수 Top 3")
        top3 = df.sort_values(by="점수", ascending=False).head(3).reset_index(drop=True)
        for i, row in top3.iterrows():
            st.markdown(f"**{i+1}위. {row['과목']} - {row['시험']}**: {row['점수']}점 (목표 {row['목표']})")
    else:
        st.info("아직 성적이 등록되지 않았습니다.")


# ---------------- 기타 메뉴 ----------------


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
