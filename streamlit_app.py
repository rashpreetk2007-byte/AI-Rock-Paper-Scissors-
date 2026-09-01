import random
import csv
import io
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Rock Paper Scissors",
    page_icon="✊",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .creator {
        text-align: center;
        font-size: 15px;
        font-weight: 600;
        margin-top: 10px;
    }

    .big-result {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        padding: 15px;
    }

    .gesture {
        text-align: center;
        font-size: 55px;
    }

    .center {
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "player_score": 0,
    "computer_score": 0,
    "draws": 0,
    "round_number": 0,
    "streak": 0,
    "best_streak": 0,
    "history": [],
    "last_result": "",
    "match_finished": False,
    "match_winner": "",
    "player_name": "Rashpreet",
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GAME DATA
# ============================================================

gesture_data = {
    "✊ Rock": "Rock",
    "✋ Paper": "Paper",
    "✌️ Scissors": "Scissors"
}


# ============================================================
# GAME LOGIC
# ============================================================

def determine_winner(player, computer):

    if player == computer:
        return "DRAW"

    if (
        (player == "Rock" and computer == "Scissors")
        or
        (player == "Paper" and computer == "Rock")
        or
        (player == "Scissors" and computer == "Paper")
    ):
        return "PLAYER"

    return "COMPUTER"


# ============================================================
# COMPUTER MOVE
# ============================================================

def computer_move(difficulty):

    moves = ["Rock", "Paper", "Scissors"]

    if difficulty == "Easy":
        return random.choice(moves)

    if difficulty == "Medium":

        return random.choice(moves)

    # Hard mode:
    # Small probability of choosing a strategic move
    if st.session_state.history:

        previous = st.session_state.history[-1]["You"]

        counter = {
            "Rock": "Paper",
            "Paper": "Scissors",
            "Scissors": "Rock"
        }

        if random.random() < 0.65:
            return counter[previous]

    return random.choice(moves)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">✊ AI Rock Paper Scissors</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '📱 Interactive Camera-Based Game'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="creator">'
    'Created by Rashpreet Kaur Arora'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# PLAYER SETTINGS
# ============================================================

st.subheader("👤 Player Settings")

name = st.text_input(
    "Enter your name",
    value=st.session_state.player_name
)

if name.strip():
    st.session_state.player_name = name.strip()


col1, col2 = st.columns(2)

with col1:

    difficulty = st.selectbox(
        "🤖 Difficulty",
        ["Easy", "Medium", "Hard"]
    )

with col2:

    match_mode = st.selectbox(
        "🏆 Match Mode",
        ["Single Round", "Best of 3", "Best of 5"]
    )


# ============================================================
# TARGET SCORE
# ============================================================

if match_mode == "Single Round":
    target_score = 1

elif match_mode == "Best of 3":
    target_score = 2

else:
    target_score = 3


st.divider()


# ============================================================
# SCOREBOARD
# ============================================================

st.subheader("🏆 Scoreboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "You",
        st.session_state.player_score
    )

with c2:
    st.metric(
        "Computer",
        st.session_state.computer_score
    )

with c3:
    st.metric(
        "Draws",
        st.session_state.draws
    )

with c4:
    st.metric(
        "🔥 Streak",
        st.session_state.streak
    )


st.divider()


# ============================================================
# MATCH STATUS
# ============================================================

if st.session_state.match_finished:

    st.markdown(
        '<div class="big-result">🏆 MATCH FINISHED</div>',
        unsafe_allow_html=True
    )

    if st.session_state.match_winner == "PLAYER":

        st.success(
            f"🎉 Congratulations {st.session_state.player_name}! "
            "You won the match!"
        )

    elif st.session_state.match_winner == "COMPUTER":

        st.error(
            "🤖 Computer won the match. Try again!"
        )

    else:

        st.info("🤝 Match ended in a draw.")

# ============================================================
# CAMERA
# ============================================================

if not st.session_state.match_finished:

    st.subheader("📷 Camera")

    st.write(
        "Show your hand and capture a picture."
    )

    st.write(
        "✊ Rock   •   ✋ Paper   •   ✌️ Scissors"
    )

    photo = st.camera_input(
        "Take a picture"
    )

    # --------------------------------------------------------
    # PHOTO CAPTURED
    # --------------------------------------------------------

    if photo is not None:

        st.success(
            "✅ Hand image captured!"
        )

        st.image(
            photo,
            caption="Captured Hand Image",
            use_container_width=True
        )

        st.divider()

        # ----------------------------------------------------
        # GESTURE SELECTION
        # ----------------------------------------------------

        st.subheader("🎯 Choose Your Gesture")

        selected = st.radio(
            "What gesture did you show?",
            list(gesture_data.keys()),
            horizontal=True
        )

        st.write(
            f"Selected: **{selected}**"
        )

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        if st.button(
            "🎮 PLAY ROUND",
            use_container_width=True
        ):

            player = gesture_data[selected]

            computer = computer_move(
                difficulty
            )

            result = determine_winner(
                player,
                computer
            )

            st.session_state.round_number += 1

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            if result == "PLAYER":

                st.session_state.player_score += 1

                st.session_state.streak += 1

                if (
                    st.session_state.streak
                    > st.session_state.best_streak
                ):
                    st.session_state.best_streak = (
                        st.session_state.streak
                    )

                result_text = "🎉 YOU WIN!"

            elif result == "COMPUTER":

                st.session_state.computer_score += 1

                st.session_state.streak = 0

                result_text = "🤖 COMPUTER WINS!"

            else:

                st.session_state.draws += 1

                result_text = "🤝 DRAW!"

            # ------------------------------------------------
            # SAVE HISTORY
            # ------------------------------------------------

            record = {
                "Round": st.session_state.round_number,
                "Player": st.session_state.player_name,
                "You": player,
                "Computer": computer,
                "Result": result_text,
                "Difficulty": difficulty
            }

            st.session_state.history.append(
                record
            )

            st.session_state.last_result = result_text

            # ------------------------------------------------
            # CHECK MATCH
            # ------------------------------------------------

            if (
                match_mode != "Single Round"
                and
                (
                    st.session_state.player_score
                    >= target_score
                    or
                    st.session_state.computer_score
                    >= target_score
                )
            ):

                st.session_state.match_finished = True

                if (
                    st.session_state.player_score
                    > st.session_state.computer_score
                ):

                    st.session_state.match_winner = "PLAYER"

                elif (
                    st.session_state.computer_score
                    > st.session_state.player_score
                ):

                    st.session_state.match_winner = "COMPUTER"

                else:

                    st.session_state.match_winner = "DRAW"


# ============================================================
# LAST RESULT
# ============================================================

if st.session_state.last_result:

    st.divider()

    st.subheader("🎯 Latest Result")

    latest = st.session_state.history[-1]

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(
            '<div class="gesture">👤</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='center'>"
            f"<b>{st.session_state.player_name}</b>"
            f"<br>{latest['You']}"
            f"</div>",
            unsafe_allow_html=True
        )

    with r2:

        st.markdown(
            '<div class="gesture">🤖</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='center'>"
            f"<b>Computer</b>"
            f"<br>{latest['Computer']}"
            f"</div>",
            unsafe_allow_html=True
        )

    if latest["Result"] == "🎉 YOU WIN!":

        st.success(
            f"🎉 {st.session_state.player_name}, YOU WIN!"
        )

    elif latest["Result"] == "🤖 COMPUTER WINS!":

        st.error(
            "🤖 COMPUTER WINS!"
        )

    else:

        st.info(
            "🤝 DRAW!"
        )


# ============================================================
# STATISTICS
# ============================================================

if st.session_state.round_number > 0:

    st.divider()

    st.subheader("📊 Statistics")

    total = (
        st.session_state.player_score
        +
        st.session_state.computer_score
        +
        st.session_state.draws
    )

    win_rate = (
        st.session_state.player_score
        / total
    ) * 100 if total else 0

    s1, s2 = st.columns(2)

    with s1:

        st.metric(
            "Total Rounds",
            total
        )

    with s2:

        st.metric(
            "Win Rate",
            f"{win_rate:.1f}%"
        )

    st.write(
        f"🔥 Best Win Streak: "
        f"**{st.session_state.best_streak}**"
    )

    st.progress(
        min(win_rate / 100, 1.0)
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

if st.session_state.round_number > 0:

    st.divider()

    st.subheader("🏅 Achievements")

    achievements = []

    if st.session_state.player_score >= 1:
        achievements.append("🥇 First Win")

    if st.session_state.player_score >= 3:
        achievements.append("🔥 3 Wins")

    if st.session_state.best_streak >= 3:
        achievements.append("⚡ 3-Win Streak")

    if st.session_state.player_score >= 5:
        achievements.append("👑 Champion")

    if not achievements:
        st.write(
            "Play more rounds to unlock achievements."
        )

    else:

        for achievement in achievements:
            st.success(achievement)


# ============================================================
# GAME HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📜 Game History")

    for game in reversed(
        st.session_state.history
    ):

        st.write(
            f"**Round {game['Round']}** — "
            f"You: {game['You']} | "
            f"Computer: {game['Computer']} | "
            f"{game['Result']}"
          )
      # --------------------------------------------------------
    # CSV DOWNLOAD
    # --------------------------------------------------------

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=[
            "Round",
            "Player",
            "You",
            "Computer",
            "Result",
            "Difficulty"
        ]
    )

    writer.writeheader()

    writer.writerows(
        st.session_state.history
    )

    st.download_button(
        label="⬇️ Download Game History",
        data=output.getvalue(),
        file_name="rock_paper_scissors_history.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# REMATCH / RESET
# ============================================================

st.divider()

col_a, col_b = st.columns(2)

with col_a:

    if st.button(
        "🔄 New Match",
        use_container_width=True
    ):

        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.draws = 0
        st.session_state.round_number = 0
        st.session_state.streak = 0
        st.session_state.history = []
        st.session_state.last_result = ""
        st.session_state.match_finished = False
        st.session_state.match_winner = ""

        st.rerun()


with col_b:

    if st.button(
        "🗑️ Reset Everything",
        use_container_width=True
    ):

        for key in defaults:
            if key == "player_name":
                st.session_state[key] = "Rashpreet"

            elif key == "history":
                st.session_state[key] = []

            elif key == "last_result":
                st.session_state[key] = ""

            elif key == "match_winner":
                st.session_state[key] = ""

            elif key == "match_finished":
                st.session_state[key] = False

            else:
                st.session_state[key] = 0

        st.rerun()


# ============================================================
# HOW TO PLAY
# ============================================================

with st.expander("ℹ️ How to Play"):

    st.write(
        """
        1. Enter your name.
        2. Select difficulty.
        3. Select Single Round, Best of 3 or Best of 5.
        4. Allow camera permission.
        5. Show Rock, Paper or Scissors.
        6. Capture your hand image.
        7. Select the gesture you showed.
        8. Press PLAY ROUND.
        9. The computer selects its move.
        10. The winner and score are updated.
        """
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

with st.expander("📚 About This Project"):

    st.write(
        """
        AI Rock Paper Scissors is an educational Python and
        Streamlit project.

        The application demonstrates camera capture,
        interactive game logic, score tracking, statistics,
        game history and computer-generated moves.

        Current version uses manual gesture selection after
        capturing the camera image.
        """
    )


# ============================================================
# TECHNOLOGIES
# ============================================================

with st.expander("🛠️ Technologies"):

    st.write(
        """
        🐍 Python

        🎨 Streamlit

        🔢 NumPy

        🖼️ Pillow

        🌐 Requests
        """
    )


# ============================================================
# LIMITATION
# ============================================================

with st.expander("⚠️ Current Limitation"):

    st.write(
        """
        Automatic hand-gesture recognition is not enabled
        in this version.

        The camera captures the image, while the player
        manually selects Rock, Paper or Scissors.

        OpenCV and MediaPipe are not required for this
        version.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="creator">
    ✊ AI Rock Paper Scissors<br>
    Created by Rashpreet Kaur Arora<br>
    BCA Student • 2026
    </div>
    """,
    unsafe_allow_html=True
)
