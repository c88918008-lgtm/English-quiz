import streamlit as st
import random

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="잠길고 영어 퀴즈", page_icon="📚", layout="centered")

# ==========================================
# 2. 문제 데이터 (선생님 수정 공간)
# ==========================================
# 💡 [어휘 데이터 수정 방법]
# "단어": {"answer": "정답", "wrong": ["오답1", "오답2", "오답3"]} 형태로 작성해주세요.
VOCAB_DATA = [
    {"word": "comprehend", "answer": "이해하다", "wrong": ["타협하다", "경쟁하다", "포함하다"]},
    {"word": "inevitable", "answer": "불가피한", "wrong": ["우연한", "일시적인", "복잡한"]},
    {"word": "sustain", "answer": "유지하다, 지탱하다", "wrong": ["의심하다", "파괴하다", "무시하다"]},
    {"word": "consequence", "answer": "결과, 중요성", "wrong": ["원인", "우연", "과정"]},
    {"word": "evaluate", "answer": "평가하다", "wrong": ["진화하다", "탈출하다", "설득하다"]},
    {"word": "perspective", "answer": "관점, 시각", "wrong": ["편견", "환상", "장애물"]},
    {"word": "implement", "answer": "실행하다", "wrong": ["방해하다", "상상하다", "포기하다"]},
    {"word": "distinguish", "answer": "구별하다", "wrong": ["결합하다", "소멸시키다", "강조하다"]},
    {"word": "attribute", "answer": "~의 탓으로 돌리다", "wrong": ["분배하다", "기여하다", "칭찬하다"]},
    {"word": "vulnerable", "answer": "취약한, 상처받기 쉬운", "wrong": ["강력한", "면역력이 있는", "단호한"]}
]

# 💡 [구문 데이터 수정 방법]
# "korean": 학생에게 보여줄 해석, "answer": 정답 문장(구두점 생략 추천)
SYNTAX_DATA = [
    {
        "grammar": "관계대명사 주격",
        "korean": "저기에서 피아노를 치고 있는 소년은 내 동생이다.",
        "answer": "The boy who is playing the piano there is my brother",
        "words": ["playing", "brother", "is", "The", "the", "who", "boy", "piano", "my", "there", "is"]
    },
    {
        "grammar": "분사구문",
        "korean": "무엇을 해야 할지 몰라서, 나는 그녀에게 도움을 요청했다.",
        "answer": "Not knowing what to do I asked her for help",
        "words": ["I", "what", "knowing", "for", "her", "Not", "do", "asked", "to", "help"]
    },
    {
        "grammar": "가정법 과거",
        "korean": "내가 충분한 돈이 있다면, 그 차를 살 텐데.",
        "answer": "If I had enough money I could buy the car",
        "words": ["money", "buy", "I", "enough", "If", "had", "car", "could", "the", "I"]
    }
]

# ==========================================
# 3. 세션 상태(Session State) 초기화
# ==========================================
# 버튼을 눌러도 점수와 문제 번호가 날아가지 않도록 상태를 저장합니다.
if 'v_index' not in st.session_state: st.session_state.v_index = 0
if 'v_score' not in st.session_state: st.session_state.v_score = 0
if 'v_answered' not in st.session_state: st.session_state.v_answered = False

if 's_index' not in st.session_state: st.session_state.s_index = 0
if 's_score' not in st.session_state: st.session_state.s_score = 0
if 's_answered' not in st.session_state: st.session_state.s_answered = False

# ==========================================
# 4. 메인 화면 및 사이드바 UI
# ==========================================
st.title("🏫 잠길고 2학년 영어 I")
st.header("오늘의 퀴즈 챌린지 🔥")

# 사이드바 구성
st.sidebar.title("📚 학습 메뉴")
mode = st.sidebar.radio("학습 모드를 선택하세요:", ["어휘 퀴즈 (단어장)", "구문 퀴즈 (문장 배열)"])
st.sidebar.divider()
st.sidebar.write("👨‍🏫 **출제 범위:** 2022 개정 영어 I")

# ==========================================
# 5. 어휘 퀴즈 로직 (Vocabulary Mode)
# ==========================================
if mode == "어휘 퀴즈 (단어장)":
    st.subheader("📝 어휘 퀴즈 모드")
    
    # 모든 문제를 다 풀었을 때
    if st.session_state.v_index >= len(VOCAB_DATA):
        st.success(f"🎉 퀴즈 완료! 최종 점수: {st.session_state.v_score} / {len(VOCAB_DATA)}")
        if st.button("다시 처음부터 풀기"):
            st.session_state.v_index = 0
            st.session_state.v_score = 0
            st.session_state.v_answered = False
            st.rerun()
            
    # 문제 진행 중일 때
    else:
        q_data = VOCAB_DATA[st.session_state.v_index]
        
        # 보기 섞기 (문제가 바뀔 때만 한 번 섞도록 캐싱 처리)
        options_key = f"v_opts_{st.session_state.v_index}"
        if options_key not in st.session_state:
            opts = q_data["wrong"] + [q_data["answer"]]
            random.shuffle(opts)
            st.session_state[options_key] = opts
            
        options = st.session_state[options_key]
        
        st.write(f"**문제 {st.session_state.v_index + 1} / {len(VOCAB_DATA)}**")
        st.info(f"### Q. '{q_data['word']}'의 올바른 뜻은?")
        
        # 정답 확인 전 (문제 풀이)
        if not st.session_state.v_answered:
            user_choice = st.radio("보기를 선택하세요:", options, index=None)
            
            if st.button("정답 확인"):
                if user_choice:
                    st.session_state.v_answered = True
                    st.session_state.v_user_choice = user_choice
                    st.rerun()
                else:
                    st.warning("보기를 선택해주세요!")
                    
        # 정답 확인 후 (결과 및 다음 문제로 넘어가기)
        else:
            # 선택한 보기 비활성화된 상태로 보여주기용 
            st.radio("보기를 선택하세요:", options, index=options.index(st.session_state.v_user_choice), disabled=True)
            
            if st.session_state.v_user_choice == q_data['answer']:
                st.success("정답입니다! 훌륭해요! 👏")
                if 'v_scored_current' not in st.session_state:
                    st.session_state.v_score += 1
                    st.session_state.v_scored_current = True
            else:
                st.error(f"아쉽네요! 정답은 '{q_data['answer']}'입니다. 🥲")
                st.session_state.v_scored_current = True # 오답이어도 중복채점 방지
                
            if st.button("다음 문제"):
                st.session_state.v_index += 1
                st.session_state.v_answered = False
                if 'v_scored_current' in st.session_state:
                    del st.session_state['v_scored_current']
                st.rerun()
                
        st.write(f"현재 점수: {st.session_state.v_score}점")

# ==========================================
# 6. 구문 퀴즈 로직 (Syntax/Scramble Mode)
# ==========================================
elif mode == "구문 퀴즈 (문장 배열)":
    st.subheader("🧩 구문 퀴즈 (문장 배열)")
    
    if st.session_state.s_index >= len(SYNTAX_DATA):
        st.success(f"🎉 모든 구문을 마스터했습니다! 최종 점수: {st.session_state.s_score} / {len(SYNTAX_DATA)}")
        if st.button("다시 처음부터 풀기"):
            st.session_state.s_index = 0
            st.session_state.s_score = 0
            st.session_state.s_answered = False
            st.rerun()
            
    else:
        q_data = SYNTAX_DATA[st.session_state.s_index]
        
        # 단어 무작위 섞기 (문제가 바뀔 때만)
        words_key = f"s_words_{st.session_state.s_index}"
        if words_key not in st.session_state:
            shuffled_words = q_data["words"].copy()
            random.shuffle(shuffled_words)
            st.session_state[words_key] = shuffled_words
            
        shuffled = st.session_state[words_key]
        
        st.write(f"**문제 {st.session_state.s_index + 1} / {len(SYNTAX_DATA)}** (핵심 구문: {q_data['grammar']})")
        st.info(f"**해석:** {q_data['korean']}")
        
        st.write("▼ 아래 단어들을 올바른 순서로 배열하세요.")
        # 보기 좋게 단어들을 버튼 형태로 나열 (클릭 기능 없이 시각적 효과)
        st.write(" ".join([f"`{w}`" for w in shuffled]))
        
        if not st.session_state.s_answered:
            user_input = st.text_input("완성된 문장을 입력하세요 (대소문자 구분 없음, 마침표 제외):")
            
            if st.button("정답 확인"):
                if user_input:
                    st.session_state.s_answered = True
                    st.session_state.s_user_input = user_input
                    st.rerun()
                else:
                    st.warning("문장을 입력해주세요!")
        else:
            st.text_input("완성된 문장을 입력하세요:", value=st.session_state.s_user_input, disabled=True)
            
            # 띄어쓰기 2개 이상, 대소문자 등을 정규화하여 비교
            clean_user = " ".join(st.session_state.s_user_input.lower().strip().split())
            clean_answer = " ".join(q_data['answer'].lower().strip().split())
            
            if clean_user == clean_answer:
                st.success("완벽합니다! 정답이에요! ✨")
                # 풍선 효과!
                st.balloons()
                if 's_scored_current' not in st.session_state:
                    st.session_state.s_score += 1
                    st.session_state.s_scored_current = True
            else:
                st.error("아쉽습니다. 다시 한번 어순을 확인해보세요!")
                st.write(f"✅ **정답:** {q_data['answer']}")
                st.session_state.s_scored_current = True
                
            if st.button("다음 문제"):
                st.session_state.s_index += 1
                st.session_state.s_answered = False
                if 's_scored_current' in st.session_state:
                    del st.session_state['s_scored_current']
                st.rerun()
                
        st.write(f"현재 점수: {st.session_state.s_score}점")
