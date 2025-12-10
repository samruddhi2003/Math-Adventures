import time
import streamlit as st

from src.puzzle_generator import PuzzleGenerator
from src.tracker import PerformanceTracker
from src.adaptive_engine import AdaptiveEngine

# Dancing animal GIFs (fox, panda, cat, dog)
DANCING_CARTOONS = [
    "https://media.giphy.com/media/3oriO7A7bt1wsEP4cw/giphy.gif",  # dancing fox
    "https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/giphy.gif",  # dancing panda
    "https://media.giphy.com/media/3oEduSbSGpGaRX2Vri/giphy.gif",  # dancing cat
    "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",   # dancing dog
]


def init_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.name = ""
        st.session_state.generator = PuzzleGenerator()
        st.session_state.tracker = PerformanceTracker()
        st.session_state.engine = AdaptiveEngine(initial_level="easy")
        st.session_state.current_puzzle = None
        st.session_state.question_index = 0
        st.session_state.max_questions = 10
        st.session_state.start_time = None
        st.session_state.last_feedback = ""
        st.session_state.finished = False
        st.session_state.started = False

        # Rewards & cartoon state
        st.session_state.coins = 0
        st.session_state.streak = 0
        st.session_state.best_streak = 0
        st.session_state.hero_mood = "neutral"  # "happy", "thinking", "sad", "neutral"
        st.session_state.cartoon_index = 0      # which dancing gif to show


def start_new_puzzle():
    """Create a new puzzle based on the current difficulty."""
    engine = st.session_state.engine
    gen = st.session_state.generator

    level = engine.current_level
    puzzle = gen.generate(level)

    st.session_state.current_puzzle = puzzle
    st.session_state.question_index += 1
    st.session_state.start_time = time.perf_counter()
    st.session_state.last_feedback = ""
    st.session_state.hero_mood = "thinking"  # thinking while solving


def apply_custom_styles():
    """Inject custom CSS for a red gradient UI with ALL text black."""
    st.markdown(
        """
        <style>

        /* ---------- GLOBAL BACKGROUND (RED GRADIENT) ---------- */
        .stApp {
            background: radial-gradient(circle at top left,
                #ff9a9e 0%,
                #ff6a00 35%,
                #ff4e50 70%,
                #f9d423 100%) !important;
            background-attachment: fixed;
        }

        /* ---------- MAKE ALL BASE TEXT BLACK ---------- */
        body, p, div, span, label, h1, h2, h3, h4 {
            color: #000000 !important;
        }

        .stMarkdown, .stText, .stCaption, .stRadio label,
        .stSelectbox label, .stSlider label {
            color: #000000 !important;
        }

        /* ---------- CARD CONTAINER ---------- */
        .card {
            padding: 1.3rem 1.5rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.92);
            color: #000000 !important;
            backdrop-filter: blur(12px);
            box-shadow: 0 14px 35px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.8);
        }

        /* ---------- BADGES ---------- */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 650;
            background: linear-gradient(135deg, #ff512f 0%, #dd2476 100%);
            color: #ffffff !important;
        }

        /* ---------- METRIC LABELS ---------- */
        .stMetricLabel, .stMetricValue {
            color: #000000 !important;
            text-shadow: none !important;
        }

        /* ---------- INPUT BOXES ---------- */
        .stTextInput > div > div > input {
            background: rgba(255,255,255,0.95) !important;
            border-radius: 14px !important;
            color: #000000 !important;
            border: 1px solid rgba(255,255,255,0.85);
        }

        /* ---------- BUTTON TEXT ---------- */
        button[kind="primary"], button[kind="secondary"] {
            color: #ffffff !important;
        }

        /* ---------- MOVE CONTENT LEFT ---------- */
        .main .block-container {
            padding-left: 0.8rem;
            padding-right: 1.5rem;
            max-width: 1200px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Math Adventures", page_icon="🧠", layout="centered")
    apply_custom_styles()
    init_state()

    tracker = st.session_state.tracker
    engine = st.session_state.engine

    # Header with cartoon + (conditional) dancing buddies + stats
    col_left, col_right = st.columns([1, 2])

    with col_left:
        show_main_cartoon()

        # Mini dancing buddies ONLY when last answer was correct (happy)
        if st.session_state.hero_mood == "happy":
            st.markdown("### 🐾 Dancing buddies")
            show_mini_cartoons()

    with col_right:
        st.title("🧠 Math Adventures")
        st.markdown(
            "<div class='card'>"
            "Practice basic math (addition, subtraction, multiplication, division). "
            "The system tracks your performance and <b>automatically adjusts</b> the difficulty."
            "</div>",
            unsafe_allow_html=True,
        )

    # Rewards bar
    st.markdown("### ⭐ Rewards")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Coins", st.session_state.coins, help="Earn 10 coins for every correct answer!")
    with c2:
        st.metric("Current Streak", st.session_state.streak)
    with c3:
        st.metric("Best Streak", st.session_state.best_streak)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Session Controls")
        st.write(f"Difficulty: **{engine.current_level.capitalize()}**")
        st.write(f"Questions answered: **{tracker.total_attempts}**")

        st.session_state.max_questions = st.slider(
            "Total questions this session",
            min_value=5,
            max_value=30,
            value=st.session_state.max_questions,
            step=1,
        )

        if st.button("🔁 Restart Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            st.rerun()

    # If finished, show summary
    if st.session_state.finished:
        show_summary()
        return

    # Start screen: name + initial difficulty
    if not st.session_state.started:
        with st.form("start_form"):
            st.subheader("👋 Let's get to know you")
            name = st.text_input("Your name", value=st.session_state.name, placeholder="Type your name")
            difficulty = st.selectbox(
                "Choose starting difficulty",
                options=["Easy", "Medium", "Hard"],
                index=["Easy", "Medium", "Hard"].index(
                    engine.current_level.capitalize()
                ),
            )
            submitted = st.form_submit_button("🚀 Start Adventure!")

        if submitted:
            st.session_state.name = name.strip() or "Learner"
            engine.current_index = engine.levels.index(difficulty.lower())
            st.session_state.started = True
            st.session_state.finished = False
            st.session_state.current_puzzle = None
            st.session_state.coins = 0
            st.session_state.streak = 0
            st.session_state.best_streak = 0
            st.session_state.hero_mood = "thinking"
            st.rerun()
        else:
            st.info("Enter your name and choose a starting difficulty to begin.")
            return

    # After start: if we don't currently have a puzzle and we're not finished,
    # create the NEXT puzzle now.
    if (
        st.session_state.started
        and not st.session_state.finished
        and st.session_state.current_puzzle is None
        and tracker.total_attempts < st.session_state.max_questions
    ):
        start_new_puzzle()

    # If still no puzzle (e.g., reached max questions), go to summary
    if st.session_state.current_puzzle is None:
        st.session_state.finished = True
        show_summary()
        return

    puzzle = st.session_state.current_puzzle

    st.markdown("### ❓ Question time")
    st.markdown(
        f"<div class='card'>"
        f"<span class='badge'>Question {st.session_state.question_index} / {st.session_state.max_questions}</span>"
        f"<br><br><span style='font-size:1.6rem; font-weight:700;'>{puzzle.question}</span>"
        f"<br><span style='font-size:0.9rem; color:#555;'>Difficulty: <b>{puzzle.difficulty.capitalize()}</b></span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.form("answer_form", clear_on_submit=True):
        answer = st.text_input("Your answer", "", placeholder="Type your answer here")
        submitted = st.form_submit_button("Submit ✅")

    if submitted:
        process_answer(answer)

    if st.session_state.last_feedback:
        st.markdown("---")
        st.markdown(f"<div class='card'>{st.session_state.last_feedback}</div>", unsafe_allow_html=True)


def process_answer(raw_answer: str):
    """Check the user's answer against the CURRENT puzzle, then clear it."""
    tracker = st.session_state.tracker
    engine = st.session_state.engine
    puzzle = st.session_state.current_puzzle

    # Safety check
    if puzzle is None or st.session_state.start_time is None:
        st.warning("No active puzzle to check. Please try again.")
        return

    end_time = time.perf_counter()
    time_taken = end_time - st.session_state.start_time

    raw = raw_answer.strip()
    user_answer = None
    correct = False

    try:
        if raw:
            user_answer = int(raw)
        correct_answer = int(puzzle.answer)
        correct = (user_answer == correct_answer)
    except ValueError:
        user_answer = None
        correct = False
        correct_answer = puzzle.answer

    # Log attempt for THIS puzzle
    tracker.log_attempt(
        question=puzzle.question,
        correct_answer=correct_answer,
        user_answer=user_answer,
        correct=correct,
        time_taken=time_taken,
        difficulty=puzzle.difficulty,
    )

    # Update rewards & mood
    if correct:
        st.session_state.streak += 1
        st.session_state.coins += 10

        # Rotate main dancing cartoon on each correct answer
        st.session_state.cartoon_index = (st.session_state.cartoon_index + 1) % len(DANCING_CARTOONS)

        if st.session_state.streak > st.session_state.best_streak:
            st.session_state.best_streak = st.session_state.streak

        st.session_state.hero_mood = "happy"   # triggers dancing in header
    else:
        st.session_state.streak = 0
        st.session_state.hero_mood = "sad"     # no dancing, show sad/neutral

    # Update difficulty using recent performance
    recent_results = tracker.recent_correctness()
    new_level = engine.update_level(recent_results)

    # Build feedback message
    if user_answer is None:
        base = f"❌ That wasn't a valid number. The correct answer was <b>{correct_answer}</b>."
    elif correct:
        base = "✅ <b>Correct! Great job!</b>"
    else:
        base = f"❌ <b>Not quite.</b> The correct answer was <b>{correct_answer}</b>."

    reward_text = ""
    if correct:
        reward_text = (
            f"<br><br>🏅 You earned <span class='coin'>10 coins</span>!"
            f" Total coins: <b>{st.session_state.coins}</b>."
        )
        if st.session_state.streak >= 3:
            reward_text += f"<br>🔥 Streak: <b>{st.session_state.streak}</b> correct in a row!"
    else:
        reward_text = "<br><br>💡 Don't worry, you'll get the next one!"

    feedback = (
        base
        + reward_text
        + f"<br><br>⏱ Time taken: <b>{time_taken:.2f} seconds</b>"
        + f"<br>🎚 Next difficulty: <b>{new_level.capitalize()}</b>"
    )

    st.session_state.last_feedback = feedback

    # Clear the current puzzle; the NEXT run will create a new one
    st.session_state.current_puzzle = None

    # If we hit max questions, mark finished; summary will show on next run
    if tracker.total_attempts >= st.session_state.max_questions:
        st.session_state.finished = True

    # Force a rerun so the next puzzle (or summary) is shown immediately
    st.rerun()


def show_summary():
    tracker = st.session_state.tracker
    engine = st.session_state.engine
    name = st.session_state.name or "Learner"

    st.header("📊 Session Summary")

    if tracker.total_attempts == 0:
        st.info("No questions answered this session. Try again!")
        return

    accuracy_percent = tracker.accuracy * 100

    st.markdown(
        f"<div class='card'>"
        f"<h3>Great work, {name}! 🎉</h3>"
        f"<p>Here's how you did in this adventure.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Celebration dancing animal at the end
    st.markdown("### 🎉 Celebration dance!")
    st.image(DANCING_CARTOONS[0], width=220)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", tracker.total_attempts)
        st.metric("Correct", tracker.num_correct)
    with col2:
        st.metric("Incorrect", tracker.num_incorrect)
        st.metric("Accuracy", f"{accuracy_percent:.1f}%")
    with col3:
        st.metric("Coins", st.session_state.coins)
        st.metric("Best Streak", st.session_state.best_streak)

    st.write(f"⏱ **Average time per question:** {tracker.average_time:.2f} seconds")
    st.write(f"🎯 **Recommended next level:** {engine.current_level.capitalize()}")

    # Show detailed mistakes
    wrong_attempts = [a for a in tracker.attempts if not a.correct]

    if wrong_attempts:
        st.markdown("---")
        st.subheader("❌ Where you went wrong")

        rows = []
        for i, a in enumerate(wrong_attempts, start=1):
            rows.append(
                {
                    "#": i,
                    "Question": a.question,
                    "Your answer": "—" if a.user_answer is None else a.user_answer,
                    "Correct answer": a.correct_answer,
                    "Difficulty": a.difficulty.capitalize(),
                }
            )

        st.table(rows)
    else:
        st.success("🔥 Perfect session! You got everything correct.")

    st.success("Thanks for playing Math Adventures! 🎉")

    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()


def show_main_cartoon():
    """
    Show:
      - Dancing GIF only when hero_mood == 'happy'
      - Static cute card otherwise (neutral / thinking / sad)
    """
    mood = st.session_state.get("hero_mood", "neutral")

    # When correct: show dancing GIF
    if mood == "happy":
        idx = st.session_state.get("cartoon_index", 0)
        gif = DANCING_CARTOONS[idx]
        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding: 0.8rem;
                border-radius: 18px;
                background: rgba(255,255,255,0.9);
                box-shadow: 0 4px 16px rgba(0,0,0,0.15);
                width: 180px;
            ">
                <img src="{gif}" width="150">
                <div style="font-size:0.85rem; margin-top:0.4rem;">Yay! You got it right! 🎉</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Static friendly card
        if mood == "sad":
            emoji = "🐼"
            text = "That one was tricky… try again!"
        elif mood == "thinking":
            emoji = "🐱"
            text = "Thinking hard... you can do it!"
        else:  # neutral
            emoji = "🦊"
            text = "Welcome! Let's start your adventure!"

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding: 0.8rem;
                border-radius: 18px;
                background: rgba(255,255,255,0.9);
                box-shadow: 0 4px 16px rgba(0,0,0,0.15);
                width: 180px;
            ">
                <div style="font-size:2.5rem;">{emoji}</div>
                <div style="font-size:0.85rem; margin-top:0.4rem;">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_mini_cartoons():
    """Show three smaller dancing animal gifs (only called when hero_mood == 'happy')."""
    base_idx = st.session_state.get("cartoon_index", 0)
    idxs = [
        base_idx,
        (base_idx + 1) % len(DANCING_CARTOONS),
        (base_idx + 2) % len(DANCING_CARTOONS),
    ]

    c1, c2, c3 = st.columns(3)
    for col, i in zip((c1, c2, c3), idxs):
        with col:
            st.image(DANCING_CARTOONS[i], width=70)


if __name__ == "__main__":
    main()
