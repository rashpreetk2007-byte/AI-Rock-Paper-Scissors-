import streamlit as st
import random
import io
import csv
from PIL import Image, ImageStat


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Rock Paper Scissors",
    page_icon="✊",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 5px;
}

.creator {
    text-align: center;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 20px;
}

.card {
    padding: 18px;
    border-radius: 20px;
    border: 1px solid rgba(128,128,128,0.25);
    margin: 10px 0;
}

.detected {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    padding: 15px;
}

.small-center {
    text-align: center;
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
    "last_result": None,
    "last_computer": None,
    "last_player": None,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GESTURES
# ============================================================

GESTURES = {
    "Rock": "✊",
    "Paper": "✋",
    "Scissors": "✌️"
}


# ============================================================
# LIGHTWEIGHT IMAGE ANALYSIS
# ============================================================

def analyze_image(image):

    """
    Lightweight heuristic.

    IMPORTANT:
    This is NOT a trained AI model.
    It only analyses basic image characteristics.
    """

    img = image.convert("RGB")
    img.thumbnail((300, 300))

    stat = ImageStat.Stat(img)

    brightness = sum(stat.mean) / 3

    # Estimate visual complexity using channel variation
    variation = sum(stat.rms) / 3

    # Conservative heuristic
    # Most uncertain images return low confidence.

    if brightness < 70:
        gesture = "Rock"
        confidence = 52

    elif variation > 145:
        gesture = "Paper"
        confidence = 50

    else:
        gesture = "Scissors"
        confidence = 48

    return gesture, confidence


# ============================================================
# GAME LOGIC
# ============================================================

def winner(player, computer):

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
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✊ AI Rock Paper Scissors</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '📷 Camera • 🔍 Gesture Analysis • 🎮 Game'
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
# SCORE
# ============================================================

st.subheader("🏆 SCORE")

a, b, c, d = st.columns(4)

with a:
    st.metric("👤 You", st.session_state.player_score)

with b:
    st.metric("🤖 Computer", st.session_state.computer_score)

with c:
    st.metric("🤝 Draws", st.session_state.draws)

with d:
    st.metric("🔥 Streak", st.session_state.streak)


st.divider()


# ============================================================
# CAMERA
# ============================================================

st.subheader("📷 Show Your Hand")

st.write(
    "Show one clear gesture in front of the camera:"
)

st.write(
    "✊ Rock   •   ✋ Paper   •   ✌️ Scissors"
)

photo = st.camera_input(
    "Capture Hand Gesture"
)


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if photo is not None:

    image = Image.open(photo)

    st.success("📸 Image captured successfully!")

    st.image(
        image,
        caption="Captured Hand Gesture",
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    st.subheader("🔍 Gesture Analysis")

    with st.spinner("Analyzing your hand..."):

        detected, confidence = analyze_image(image)

    emoji = GESTURES[detected]

    st.markdown(
        f"""
        <div class="card">
        <div class="small-center">DETECTED GESTURE</div>
        <div class="detected">{emoji} {detected.upper()}</div>
        <div class="small-center">
        Confidence: {confidence}%
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        confidence / 100
    )

    st.warning(
        "⚠️ This is a lightweight image heuristic, "
        "not a trained hand-recognition AI model."
    )

    # --------------------------------------------------------
    # CORRECTION
    # --------------------------------------------------------

    st.subheader("✅ Confirm Gesture")

    confirmed = st.radio(
        "If detection is incorrect, select the correct gesture:",
        [
            "✊ Rock",
            "✋ Paper",
            "✌️ Scissors"
        ],
        index=[
            "Rock",
            "Paper",
            "Scissors"
        ].index(detected),
        horizontal=True
    )

    player = confirmed.split(" ", 1)[1]

    st.divider()

    # --------------------------------------------------------
    # PLAY
    # --------------------------------------------------------

    if st.button(
        "🎮 PLAY ROUND",
        use_container_width=True
    ):

        computer = random.choice(
            ["Rock", "Paper", "Scissors"]
        )

        result = winner(
            player,
            computer
        )

        st.session_state.round += 1

        # ----------------------------------------------------
        # UPDATE SCORE
        # ----------------------------------------------------

        if result == "PLAYER":

            st.session_state.player_score += 1
            st.session_state.streak += 1

            st.session_state.best_streak = max(
                st.session_state.best_streak,
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

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        st.session_state.last_player = player
        st.session_state.last_computer = computer
        st.session_state.last_result = result_text

        st.session_state.history.append({
            "Round": st.session_state.round,
            "Player": player,
            "Computer": computer,
            "Result": result_text
        })


# ============================================================
# RESULT
# ============================================================

if st.session_state.last_result:

    st.divider()

    st.subheader("🎯 RESULT")

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(
            f"""
            <div class="card">
            <div class="small-center">
            👤 YOUR MOVE
            </div>
            <div class="detected">
            {GESTURES[st.session_state.last_player]}
            </div>
            <div class="small-center">
            {st.session_state.last_player}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2:

        st.markdown(
            f"""
            <div class="card">
            <div class="small-center">
            🤖 COMPUTER
            </div>
            <div class="detected">
            {GESTURES[st.session_state.last_computer]}
            </div>
            <div class="small-center">
            {st.session_state.last_computer}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if "YOU WIN" in st.session_state.last_result:

        st.success(
            "🎉 YOU WIN!"
        )

        st.balloons()

    elif "COMPUTER" in st.session_state.last_result:

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

total_games = (
    st.session_state.player_score
    + st.session_state.computer_score
    + st.session_state.draws
)

if total_games > 0:

    st.divider()

    st.subheader("📊 PERFORMANCE")

    win_rate = (
        st.session_state.player_score
        / total_games
    ) * 100

    x, y = st.columns(2)

    with x:
        st.metric(
            "Total Games",
            total_games
        )

    with y:
        st.metric(
            "Win Rate",
            f"{win_rate:.1f}%"
        )

    st.write(
        f"🔥 Best Streak: "
        f"**{st.session_state.best_streak}**"
    )

    st.progress(
        win_rate / 100
    )


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📜 GAME HISTORY")

    for game in reversed(
        st.session_state.history
    ):

        st.write(
            f"**Round {game['Round']}** | "
            f"You: {game['Player']} | "
            f"Computer: {game['Computer']} | "
            f"{game['Result']}"
        )

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=[
            "Round",
            "Player",
            "Computer",
            "Result"
        ]
    )

    writer.writeheader()

    writer.writerows(
        st.session_state.history
    )

    st.download_button(
        "⬇️ Download Game History",
        output.getvalue(),
        "rock_paper_scissors_history.csv",
        "text/csv",
        use_container_width=True
    )


# ============================================================
# RESET
# ============================================================

st.divider()

if st.button(
    "🔄 NEW GAME",
    use_container_width=True
):

    for key, value in defaults.items():

        if isinstance(value, list):
            st.session_state[key] = []

        else:
            st.session_state[key] = value

    st.rerun()


# ============================================================
# PROJECT INFO
# ============================================================

with st.expander("ℹ️ About Project"):

    st.write(
        """
        AI Rock Paper Scissors is an educational Python and
        Streamlit project created by Rashpreet Kaur Arora.

        The application uses the device camera to capture a
        hand image and performs lightweight image analysis.

        The detected gesture can be confirmed or corrected
        before playing the round.
        """
    )


with st.expander("🛠️ Technologies Used"):

    st.write(
        """
        🐍 Python

        🎨 Streamlit

        🖼️ Pillow

        🔢 NumPy

        🌐 Requests
        """
    )


with st.expander("⚠️ Recognition Note"):

    st.write(
        """
        The current mobile version does not use OpenCV or
        MediaPipe.

        Therefore the image analysis is only a lightweight
        heuristic and should not be considered a trained
        AI hand-gesture classifier.

        A trained model can be integrated in a future version.
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
