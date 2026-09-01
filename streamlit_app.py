import streamlit as st
import random
from datetime import datetime

# ============================================================
# AI ROCK PAPER SCISSORS
# Created by Rashpreet Kaur Arora
# BCA II Year
# ============================================================

st.set_page_config(
    page_title="AI Rock Paper Scissors",
    page_icon="✊",
    layout="centered"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 950px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    text-align: center;
    padding: 20px 5px 10px;
}

.title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

.creator {
    font-size: 16px;
    font-weight: 700;
    margin-top: 10px;
}

.game-card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    margin: 12px 0;
    text-align: center;
}

.move {
    font-size: 65px;
    margin: 10px;
}

.move-name {
    font-size: 22px;
    font-weight: 700;
}

.win {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    background: #e9f9ef;
    border: 2px solid #45b96b;
}

.lose {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    background: #fff0f0;
    border: 2px solid #df6464;
}

.draw {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    background: #fff8df;
    border: 2px solid #e1b93d;
}

.result-text {
    font-size: 30px;
    font-weight: 800;
}

.footer {
    text-align: center;
    color: #777;
    padding-top: 30px;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "player_score": 0,
    "computer_score": 0,
    "draws": 0,
    "round": 0,
    "streak": 0,
    "best_streak": 0,
    "history": [],
    "last_player": None,
    "last_computer": None,
    "last_result": None,
    "game_over": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GAME DATA
# ============================================================

moves = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌️"
}

counter_move = {
    "Rock": "Paper",
    "Paper": "Scissors",
    "Scissors": "Rock"
}


# ============================================================
# FUNCTIONS
# ============================================================

def get_result(player, computer):

    if player == computer:
        return "Draw"

    if (
        (player == "Rock" and computer == "Scissors")
        or
        (player == "Paper" and computer == "Rock")
        or
        (player == "Scissors" and computer == "Paper")
    ):
        return "Player"

    return "Computer"


def reset_game():

    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.draws = 0
    st.session_state.round = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.history = []
    st.session_state.last_player = None
    st.session_state.last_computer = None
    st.session_state.last_result = None
    st.session_state.game_over = False


def target_score(mode):

    if mode == "Best of 3":
        return 2

    if mode == "Best of 5":
        return 3

    if mode == "Best of 7":
        return 4

    return 1


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="title">
✊ AI Rock Paper Scissors
</div>

<div class="subtitle">
🎮 Interactive Camera-Based Game
</div>

<div class="creator">
Created by Rashpreet Kaur Arora
</div>

</div>
""", unsafe_allow_html=True)

st.divider()


# ============================================================
# PLAYER SETTINGS
# ============================================================

st.header("👤 Player Settings")

player_name = st.text_input(
    "Player Name",
    value="Rashpreet"
)

col1, col2 = st.columns(2)

with col1:

    difficulty = st.selectbox(
        "🤖 Difficulty",
        [
            "Easy",
            "Normal",
            "Hard"
        ]
    )

with col2:

    mode = st.selectbox(
        "🏆 Match Mode",
        [
            "Single Round",
            "Best of 3",
            "Best of 5",
            "Best of 7"
        ]
    )

target = target_score(mode)


# ============================================================
# SCOREBOARD
# ============================================================

st.divider()

st.header("🏆 Scoreboard")

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "👤 You",
        st.session_state.player_score
    )

with b:
    st.metric(
        "🤖 Computer",
        st.session_state.computer_score
    )

with c:
    st.metric(
        "🤝 Draws",
        st.session_state.draws
    )

with d:
    st.metric(
        "🔥 Streak",
        st.session_state.streak
    )

st.caption(
    f"Match target: {target} win(s)"
)


# ============================================================
# CAMERA
# ============================================================

st.divider()

st.header("📸 Camera")

st.write(
    "Show your hand in front of the camera and capture the image."
)

st.markdown(
    """
    ✊ **Rock** &nbsp;&nbsp;&nbsp;
    ✋ **Paper** &nbsp;&nbsp;&nbsp;
    ✌️ **Scissors**
    """
)

photo = st.camera_input(
    "Take Hand Gesture Photo"
)

if photo is not None:

    st.success(
        "✅ Hand image captured successfully!"
    )

    st.image(
        photo,
        caption="Your Captured Hand Gesture",
        use_container_width=True
    )


# ============================================================
# GESTURE SELECTION
# ============================================================

st.divider()

st.header("🖐 Select Your Gesture")

st.info(
    "Select the gesture shown in your camera photo."
)

gesture = st.radio(
    "Your Gesture",
    [
        "Rock",
        "Paper",
        "Scissors"
    ],
    horizontal=True,
    format_func=lambda x:
        f"{moves[x]} {x}"
)

st.markdown(
    f"""
    <div class="game-card">

    <div class="move">
    {moves[gesture]}
    </div>

    <div class="move-name">
    Your Choice: {gesture}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PLAY BUTTON
# ============================================================

if not st.session_state.game_over:

    if st.button(
        "🎮 PLAY ROUND",
        use_container_width=True,
        type="primary"
    ):

        # ----------------------------------------------------
        # COMPUTER MOVE
        # ----------------------------------------------------

        if difficulty == "Easy":

            computer = random.choice(
                list(moves.keys())
            )

        elif difficulty == "Normal":

            if random.random() < 0.35:

                computer = counter_move[gesture]

            else:

                computer = random.choice(
                    list(moves.keys())
                )

        else:

            if random.random() < 0.65:

                computer = counter_move[gesture]

            else:

                computer = random.choice(
                    list(moves.keys())
                )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        result = get_result(
            gesture,
            computer
        )

        st.session_state.round += 1

        st.session_state.last_player = gesture

        st.session_state.last_computer = computer

        st.session_state.last_result = result

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        if result == "Player":

            st.session_state.player_score += 1

            st.session_state.streak += 1

            if (
                st.session_state.streak
                >
                st.session_state.best_streak
            ):

                st.session_state.best_streak = (
                    st.session_state.streak
                )

        elif result == "Computer":

            st.session_state.computer_score += 1

            st.session_state.streak = 0

        else:

            st.session_state.draws += 1

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        st.session_state.history.append(
            {
                "Round":
                    st.session_state.round,

                "Player":
                    gesture,

                "Computer":
                    computer,

                "Result":
                    result,

                "Time":
                    datetime.now().strftime(
                        "%H:%M:%S"
                    )
            }
        )

        # ----------------------------------------------------
        # MATCH END
        # ----------------------------------------------------

        if mode == "Single Round":

            st.session_state.game_over = True

        else:

            if (
                st.session_state.player_score
                >= target
                or
                st.session_state.computer_score
                >= target
            ):

                st.session_state.game_over = True

        st.rerun()


# ============================================================
# RESULT
# ============================================================

if st.session_state.last_result:

    st.divider()

    st.header("🎯 Round Result")

    player_move = st.session_state.last_player

    computer_move = st.session_state.last_computer

    result = st.session_state.last_result

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="game-card">

            <h3>👤 {player_name}</h3>

            <div class="move">
            {moves[player_move]}
            </div>

            <div class="move-name">
            {player_move}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="game-card">

            <h3>🤖 Computer</h3>

            <div class="move">
            {moves[computer_move]}
            </div>

            <div class="move-name">
            {computer_move}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # RESULT MESSAGE
    # --------------------------------------------------------

    if result == "Player":

        st.markdown(
            """
            <div class="win">

            <div class="result-text">
            🎉 YOU WIN!
            </div>

            <p>Excellent move!</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif result == "Computer":

        st.markdown(
            """
            <div class="lose">

            <div class="result-text">
            🤖 COMPUTER WINS!
            </div>

            <p>Try another strategy.</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="draw">

            <div class="result-text">
            🤝 DRAW!
            </div>

            <p>Both players selected the same move.</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MATCH RESULT
# ============================================================

if st.session_state.game_over:

    st.divider()

    if mode == "Single Round":

        st.success(
            "🏁 Round completed!"
        )

    elif (
        st.session_state.player_score
        >= target
    ):

        st.success(
            f"🏆 {player_name} WON THE MATCH!"
        )

    elif (
        st.session_state.computer_score
        >= target
    ):

        st.error(
            "🤖 COMPUTER WON THE MATCH!"
        )


# ============================================================
# STATISTICS
# ============================================================

st.divider()

st.header("📊 Game Statistics")

total = (
    st.session_state.player_score
    +
    st.session_state.computer_score
    +
    st.session_state.draws
)

if total > 0:

    win_rate = (
        st.session_state.player_score
        / total
    ) * 100

else:

    win_rate = 0


s1, s2, s3 = st.columns(3)

with s1:

    st.metric(
        "🎮 Total Rounds",
        total
    )

with s2:

    st.metric(
        "📈 Win Rate",
        f"{win_rate:.1f}%"
    )

with s3:

    st.metric(
        "🔥 Best Streak",
        st.session_state.best_streak
    )


# ============================================================
# GAME HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.header("📜 Game History")

    for game in reversed(
        st.session_state.history
    ):

        if game["Result"] == "Player":

            icon = "✅"

        elif game["Result"] == "Computer":

            icon = "❌"

        else:

            icon = "🤝"

        st.write(
            f"{icon} **Round {game['Round']}** — "
            f"{moves[game['Player']]} "
            f"{game['Player']} vs "
            f"{moves[game['Computer']]} "
            f"{game['Computer']} — "
            f"**{game['Result']}** "
            f"({game['Time']})"
        )


# ============================================================
# BUTTONS
# ============================================================

st.divider()

b1, b2 = st.columns(2)

with b1:

    if st.button(
        "🔄 NEW GAME",
        use_container_width=True
    ):

        reset_game()

        st.rerun()


with b2:

    if st.button(
        "🧹 CLEAR HISTORY",
        use_container_width=True
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# HOW TO PLAY
# ============================================================

st.divider()

st.header("📖 How to Play")

st.markdown("""
**Step 1:** Enter your name.

**Step 2:** Select difficulty.

**Step 3:** Select match mode.

**Step 4:** Show your hand to the camera.

**Step 5:** Capture the photo.

**Step 6:** Select Rock, Paper or Scissors according to your hand.

**Step 7:** Press **PLAY ROUND**.

**Step 8:** Compare your move with the computer.

**Step 9:** Check your score, streak and game history.
""")


# ============================================================
# TECHNICAL NOTE
# ============================================================

st.info(
    "Camera capture is implemented without OpenCV or MediaPipe. "
    "The current version does not automatically classify the "
    "captured hand image; the player selects the gesture manually."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<b>✊ AI Rock Paper Scissors</b><br>

Interactive Camera-Based Game<br>

Built with Python + Streamlit + Pillow<br><br>

<strong>Created by Rashpreet Kaur Arora</strong><br>

BCA II Year • Educational Project

</div>
""", unsafe_allow_html=True)
