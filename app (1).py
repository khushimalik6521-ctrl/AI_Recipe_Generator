import streamlit as st
from google import genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Recipe Studio",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fffaf2, #fff1df);
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1, h2, h3 {
    color: #472b1b;
}

.hero {
    background: linear-gradient(120deg, #ff9d52, #f56b35);
    padding: 35px;
    border-radius: 24px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 8px;
}

.hero p {
    color: white;
    font-size: 16px;
}

.info-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #f4ddc8;
    margin-bottom: 16px;
}

.stButton > button {
    background: #f47738;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background: #df5e25;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 10px;
}

.small-note {
    color: #916d55;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "recipe": "",
    "saved_recipes": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- NAVIGATION ----------------
def go_to(page):
    st.session_state.page = page
    st.rerun()


# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:

    st.markdown("""
    <div class="hero">
        <h1>🍳 Welcome to Recipe Studio</h1>
        <p>Your kitchen, your ingredients, your personalised recipes.</p>
    </div>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([1, 1.3, 1])

    with middle:
        st.markdown("## Let's get cooking!")
        st.write("Sign in to explore delicious possibilities.")

        with st.form("login_form"):
            username = st.text_input("Your Name", placeholder="Enter your name")
            password = st.text_input(
                "Demo Password",
                type="password",
                placeholder="Enter any password"
            )
            submitted = st.form_submit_button("Login →")

            if submitted:
                if username.strip() and password.strip():
                    st.session_state.username = username.strip()
                    st.session_state.logged_in = True
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.warning("Please enter your name and password.")

        st.caption("Demo login: Enter any name and any password.")

    st.stop()


# ---------------- TOP HEADER ----------------
st.markdown(f"""
<div class="hero">
    <h1>🍊 Recipe Studio</h1>
    <p>Good food starts with what you already have.</p>
    <p>Welcome, {st.session_state.username}!</p>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION BAR ----------------
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button("🏠 Home"):
        go_to("Home")

with nav2:
    if st.button("🥕 Create Recipe"):
        go_to("Create")

with nav3:
    if st.button("🍽️ Generated"):
        go_to("Generated")

with nav4:
    if st.button("❤️ Saved Recipes"):
        go_to("Saved")

with nav5:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()


st.divider()


# ---------------- HOME PAGE ----------------
if st.session_state.page == "Home":

    st.markdown("## Discover the joy of cooking ✨")
    st.write("Your personal AI cooking assistant is ready to help.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h2>🥕</h2>
            <h3>Use Your Ingredients</h3>
            <p>Find creative recipes using ingredients already in your kitchen.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h2>🤖</h2>
            <h3>AI Powered</h3>
            <p>Get personalised recipe suggestions with the help of Gemini AI.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <h2>❤️</h2>
            <h3>Save Your Favourites</h3>
            <p>Keep your favourite recipes in one convenient place.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### Ready to create something delicious?")

    if st.button("Start Creating Recipes →"):
        go_to("Create")


# ---------------- CREATE RECIPE PAGE ----------------
elif st.session_state.page == "Create":

    st.markdown("## 🥕 Create Your Own Recipe")
    st.write("Tell us what you have in your kitchen.")

    with st.form("recipe_form"):

        ingredients = st.text_area(
            "Available Ingredients",
            placeholder="Example: Potato, tomato, onion, paneer, rice...",
            height=110
        )

        c1, c2 = st.columns(2)

        with c1:
            cuisine = st.selectbox(
                "Select Cuisine",
                ["Indian", "Italian", "Chinese", "Mexican", "Continental", "Any"]
            )

            preference = st.selectbox(
                "Food Preference",
                ["Vegetarian", "Vegan", "Eggetarian", "Non-Vegetarian"]
            )

            cooking_time = st.selectbox(
                "Available Cooking Time",
                ["15 minutes", "30 minutes", "45 minutes", "60 minutes"]
            )

        with c2:
            difficulty = st.selectbox(
                "Cooking Difficulty",
                ["Easy", "Medium", "Hard"]
            )

            servings = st.number_input(
                "Number of Servings",
                min_value=1,
                max_value=10,
                value=2
            )

        generate = st.form_submit_button("✨ Generate My Recipe")

    if generate:
        if not ingredients.strip():
            st.warning("Please enter some ingredients first.")

        else:
            api_key = st.secrets.get("GEMINI_API_KEY")

            if not api_key:
                st.error("API key not configured. Please check Streamlit Secrets.")

            else:
                prompt = f"""
                You are a professional chef and recipe assistant.

                Create ONE practical and delicious recipe using these details:

                Available ingredients: {ingredients}
                Cuisine: {cuisine}
                Food preference: {preference}
                Cooking time: {cooking_time}
                Difficulty: {difficulty}
                Servings: {servings}

                Follow this format:

                Recipe Name:
                Short Description:
                Preparation Time:
                Cooking Time:
                Ingredients:
                Step-by-Step Instructions:
                Chef's Tips:

                Keep the instructions clear and beginner-friendly.
                Respect the selected food preference.
                Do not suggest ingredients that conflict with it.
                """

                try:
                    with st.spinner("👩‍🍳 Your recipe is being prepared..."):

                        client = genai.Client(api_key=api_key)

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt,
                            config={
                                "temperature": 0.6,
                                "max_output_tokens": 1100
                            }
                        )

                        st.session_state.recipe = response.text
                        st.session_state.page = "Generated"
                        st.rerun()

                except Exception as e:
                    st.error("Recipe generation failed. Please check the API configuration.")
                    st.caption(str(e))


# ---------------- GENERATED RECIPE PAGE ----------------
elif st.session_state.page == "Generated":

    st.markdown("## 🍽️ Your Generated Recipe")

    if st.session_state.recipe:

        st.markdown("""
        <div class="info-card">
            <h2>✨ Made specially for you!</h2>
            <p>Your personalised AI-generated recipe is ready.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.recipe)

        if st.button("❤️ Save This Recipe"):
            if st.session_state.recipe not in st.session_state.saved_recipes:
                st.session_state.saved_recipes.append(
                    st.session_state.recipe
                )
                st.success("Recipe saved successfully!")

            else:
                st.info("This recipe is already saved.")

    else:
        st.info("You haven't generated a recipe yet.")
        if st.button("Create Your First Recipe"):
            go_to("Create")


# ---------------- SAVED RECIPES PAGE ----------------
elif st.session_state.page == "Saved":

    st.markdown("## ❤️ My Saved Recipes")
    st.write("Your personal collection of favourite dishes.")

    if st.session_state.saved_recipes:

        for i, recipe in enumerate(st.session_state.saved_recipes):

            with st.expander(f"🍲 Saved Recipe {i + 1}"):

                st.markdown(recipe)

                if st.button("Remove Recipe", key=f"remove_{i}"):
                    st.session_state.saved_recipes.pop(i)
                    st.success("Recipe removed.")
                    st.rerun()

    else:
        st.markdown("""
        <div class="info-card">
            <h2>🥗 No saved recipes yet!</h2>
            <p>Generate a recipe and save your favourites here.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create a Recipe"):
            go_to("Create")


# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p class='small-note' style='text-align:center;'>"
    "Made with ❤️ using Streamlit & Gemini AI | Recipe Studio"
    "</p>",
    unsafe_allow_html=True
)
