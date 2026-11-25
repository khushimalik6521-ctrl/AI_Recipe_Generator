import streamlit as st
import html

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
    background: linear-gradient(135deg, #fffaf3, #fff0df);
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1120px;
}

h1, h2, h3 {
    color: #482b1b;
    font-weight: 700;
}

.hero {
    background: linear-gradient(120deg, #ff9d52, #ef6736);
    padding: 38px;
    border-radius: 25px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(210, 100, 40, 0.17);
}

.hero h1 {
    color: white;
    font-size: 39px;
    margin-bottom: 8px;
}

.hero p {
    color: white;
    font-size: 15px;
}

.info-card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #f3ddca;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(100, 60, 30, 0.06);
    min-height: 175px;
}

.section-label {
    color: #e66b35;
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 12px;
}

.stButton > button {
    background: linear-gradient(110deg, #f68a45, #ed6734);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 11px 20px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background: #d95727;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 11px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid #f3ddca;
}

[data-testid="stExpander"] {
    background: white;
    border-radius: 14px;
    border: 1px solid #f2ddca;
}

.small-note {
    color: #916d55;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- RECIPE DATABASE ----------------

RECIPES = [

    {
        "name": "Paneer Butter Masala",
        "emoji": "🍛",
        "cuisine": "Indian",
        "preference": "Vegetarian",
        "difficulty": "Medium",
        "time": 35,
        "match": ["paneer", "tomato", "onion", "butter"],
        "description": "A rich and creamy North Indian curry with soft paneer cubes.",
        "ingredients": [
            "200g paneer",
            "2 tomatoes",
            "1 onion",
            "1 tbsp butter",
            "2 tbsp cream",
            "1 tsp ginger-garlic paste",
            "1/2 tsp red chilli powder",
            "1/2 tsp garam masala",
            "Salt as required"
        ],
        "steps": [
            "Heat butter in a pan and add chopped onions.",
            "Add ginger-garlic paste and cook until fragrant.",
            "Add chopped tomatoes and cook until soft.",
            "Add spices and blend the mixture into a smooth gravy.",
            "Add paneer cubes and cook for 5 minutes.",
            "Add cream and garam masala. Mix gently.",
            "Serve hot with naan, roti or rice."
        ],
        "tips": "Add a little kasuri methi for a restaurant-style flavour."
    },

    {
        "name": "Crispy Aloo Tikki",
        "emoji": "🥔",
        "cuisine": "Indian",
        "preference": "Vegetarian",
        "difficulty": "Easy",
        "time": 30,
        "match": ["aloo", "onion", "peas"],
        "description": "Golden and crispy potato patties with a delicious spicy filling.",
        "ingredients": [
            "3 medium boiled potatoes",
            "1/2 cup boiled peas",
            "1 chopped onion",
            "2 tbsp breadcrumbs",
            "1/2 tsp red chilli powder",
            "1/2 tsp garam masala",
            "1/2 tsp chaat masala",
            "Salt as required",
            "Oil for shallow frying"
        ],
        "steps": [
            "Mash the boiled potatoes in a bowl.",
            "Add peas, chopped onion and all the spices.",
            "Mix everything well and add breadcrumbs.",
            "Shape the mixture into small round patties.",
            "Heat a little oil in a pan.",
            "Shallow fry the patties until golden and crispy on both sides.",
            "Serve hot with mint chutney or tomato ketchup."
        ],
        "tips": "Refrigerate the patties briefly before frying to help them hold their shape."
    },

    {
        "name": "Vegetable Fried Rice",
        "emoji": "🍚",
        "cuisine": "Chinese",
        "preference": "Vegan",
        "difficulty": "Easy",
        "time": 20,
        "match": ["rice", "carrot", "capsicum", "onion", "peas"],
        "description": "A quick and flavourful rice dish loaded with fresh vegetables.",
        "ingredients": [
            "2 cups cooked rice",
            "1/2 cup chopped carrots",
            "1/2 cup chopped capsicum",
            "1/4 cup peas",
            "1 chopped onion",
            "1 tbsp soy sauce",
            "1 tsp black pepper",
            "1 tbsp oil",
            "Salt as required"
        ],
        "steps": [
            "Heat oil in a large pan or wok.",
            "Add chopped onion and saute for a minute.",
            "Add carrots, capsicum and peas.",
            "Stir fry the vegetables for 3-4 minutes.",
            "Add cooked rice and mix gently.",
            "Add soy sauce, black pepper and salt.",
            "Toss everything together and serve hot."
        ],
        "tips": "Use cooled, previously cooked rice for the best texture."
    }
]


# ---------------- INGREDIENT NORMALIZATION ----------------

def normalize_ingredient(item):
    item = item.strip().lower()

    aliases = {
        "potato": "aloo",
        "potatoes": "aloo",
        "potatoe": "aloo"
    }

    return aliases.get(item, item)


# ---------------- SESSION STATE ----------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "recipe": None,
    "saved_recipes": [],
    "matched_recipes": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- NAVIGATION ----------------

def go_to(page):
    st.session_state.page = page
    st.rerun()


# ---------------- RECIPE DISPLAY ----------------

def display_recipe(recipe):

    st.markdown(f"## {recipe['emoji']} {recipe['name']}")
    st.write(recipe["description"])

    c1, c2, c3 = st.columns(3)

    c1.metric("⏱️ Cooking Time", f"{recipe['time']} min")
    c2.metric("👩‍🍳 Difficulty", recipe["difficulty"])
    c3.metric("🍽️ Servings", recipe["servings"])

    st.divider()

    left, right = st.columns([1, 1.3])

    with left:
        st.markdown("### 🥕 Ingredients")

        for item in recipe["ingredients"]:
            st.markdown(f"- {item}")

    with right:
        st.markdown("### 👩‍🍳 Preparation Steps")

        for i, step in enumerate(recipe["steps"], 1):
            st.markdown(f"**Step {i}:** {step}")
            st.write("")

    st.info(f"💡 Chef's Tip: {recipe['tips']}")


# ---------------- LOGIN SCREEN ----------------

if not st.session_state.logged_in:

    st.markdown("""
    <div class="hero">
        <h1>🍳 Welcome to Recipe Studio</h1>
        <p>Your kitchen, your ingredients, your personalised recipes.</p>
        <p>Discover something delicious today!</p>
    </div>
    """, unsafe_allow_html=True)

    left, middle, right = st.columns([1, 1.3, 1])

    with middle:

        st.markdown("## Let's get cooking!")
        st.write("Sign in to explore delicious possibilities.")

        with st.form("login_form"):

            username = st.text_input(
                "Your Name",
                placeholder="Enter your name"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
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

    st.stop()


# ---------------- TOP HEADER ----------------

safe_username = html.escape(st.session_state.username)

st.markdown(f"""
<div class="hero">
    <h1>🍊 Recipe Studio</h1>
    <p>Good food starts with what you already have.</p>
    <p>Welcome, {safe_username}! ✨</p>
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
        st.session_state.recipe = None
        st.session_state.matched_recipes = []
        st.session_state.page = "Home"
        st.rerun()


st.divider()


# ---------------- HOME PAGE ----------------

if st.session_state.page == "Home":

    st.markdown(
        '<p class="section-label">YOUR PERSONAL COOKING SPACE</p>',
        unsafe_allow_html=True
    )

    st.markdown("## Discover the joy of cooking ✨")

    st.write(
        "Turn everyday ingredients into something delicious. "
        "Explore, prepare and save your favourite recipes."
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h2>🥕</h2>
            <h3>Smart Ingredients</h3>
            <p>Find creative recipes using ingredients already available in your kitchen.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h2>👩‍🍳</h2>
            <h3>Easy Cooking</h3>
            <p>Follow simple and clear step-by-step cooking instructions.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
            <h2>❤️</h2>
            <h3>Save Favourites</h3>
            <p>Keep your favourite recipes in one convenient collection.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### Ready to create something delicious?")
    st.write("Let's discover what you can cook with your ingredients!")

    if st.button("✨ Start Creating Recipes →"):
        go_to("Create")


# ---------------- CREATE RECIPE PAGE ----------------

elif st.session_state.page == "Create":

    st.markdown(
        '<p class="section-label">LET YOUR INGREDIENTS INSPIRE YOU</p>',
        unsafe_allow_html=True
    )

    st.markdown("## 🥕 Create Your Own Recipe")

    st.write("Tell us what you have in your kitchen.")

    with st.form("recipe_form"):

        ingredients = st.text_area(
            "Available Ingredients",
            placeholder="Example: Aloo, tomato, onion, paneer, rice...",
            height=110
        )

        c1, c2 = st.columns(2)

        with c1:

            cuisine = st.selectbox(
                "Select Cuisine",
                ["Any", "Indian", "Chinese"]
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
                ["Any", "Easy", "Medium", "Hard"]
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

        elif preference in ["Eggetarian", "Non-Vegetarian"]:

            st.warning(
                "Currently, our recipe collection supports Vegetarian "
                "and Vegan preferences. Please select one of these."
            )

        else:

            entered = list(set([
                normalize_ingredient(item)
                for item in ingredients.replace("\n", ",").split(",")
                if item.strip()
            ]))

            max_time = int(cooking_time.split()[0])

            matching = []

            for recipe in RECIPES:

                if cuisine != "Any" and recipe["cuisine"] != cuisine:
                    continue

                if preference == "Vegan" and recipe["preference"] != "Vegan":
                    continue

                if recipe["time"] > max_time:
                    continue

                if difficulty != "Any" and recipe["difficulty"] != difficulty:
                    continue

                score = len(
                    set(recipe["match"]).intersection(set(entered))
                )

                if score > 0:

                    recipe_copy = recipe.copy()
                    recipe_copy["servings"] = servings

                    matching.append((score, recipe_copy))

            if matching:

                matching.sort(key=lambda x: x[0], reverse=True)

                st.session_state.matched_recipes = [
                    item[1] for item in matching
                ]

                st.session_state.recipe = matching[0][1]
                st.session_state.page = "Generated"

                st.rerun()

            else:

                st.error(
                    "⚠️ Recipe generation is temporarily unavailable."
                )

                st.warning(
                    "The recipe service is experiencing high traffic "
                    "or is temporarily unavailable. Please try again later."
                )

                st.caption(
                    "Error: 429 RESOURCE_EXHAUSTED — "
                    "Simulated showcase fallback. No live API request was made."
                )


# ---------------- GENERATED RECIPE PAGE ----------------

elif st.session_state.page == "Generated":

    st.markdown(
        '<p class="section-label">YOUR PERSONALIZED COOKING RESULTS</p>',
        unsafe_allow_html=True
    )

    st.markdown("## 🍽️ Your Recipe Results")

    if st.session_state.recipe:

        st.markdown("""
        <div class="info-card">
            <h2>✨ Your Kitchen Inspiration!</h2>
            <p>Explore the recipes matching your available ingredients.</p>
        </div>
        """, unsafe_allow_html=True)

        recipes = st.session_state.matched_recipes

        if not recipes:
            recipes = [st.session_state.recipe]

        selected = st.selectbox(
            "Choose a recipe",
            options=range(len(recipes)),
            format_func=lambda i: recipes[i]["name"]
        )

        current_recipe = recipes[selected]

        display_recipe(current_recipe)

        st.write("")

        if st.button("❤️ Save This Recipe"):

            existing = [
                r["name"] for r in st.session_state.saved_recipes
            ]

            if current_recipe["name"] not in existing:

                st.session_state.saved_recipes.append(
                    current_recipe.copy()
                )

                st.success("Recipe saved successfully! ❤️")

            else:

                st.info("This recipe is already in your collection.")

    else:

        st.info("You haven't generated a recipe yet.")

        if st.button("Create Your First Recipe"):
            go_to("Create")


# ---------------- SAVED RECIPES PAGE ----------------

elif st.session_state.page == "Saved":

    st.markdown(
        '<p class="section-label">YOUR PERSONAL COLLECTION</p>',
        unsafe_allow_html=True
    )

    st.markdown("## ❤️ My Saved Recipes")

    st.write("Your collection of favourite dishes.")

    st.metric(
        "Total Saved Recipes",
        len(st.session_state.saved_recipes)
    )

    if st.session_state.saved_recipes:

        for i, recipe in enumerate(st.session_state.saved_recipes):

            with st.expander(
                f"{recipe['emoji']} {recipe['name']}",
                expanded=False
            ):

                display_recipe(recipe)

                if st.button(
                    "🗑️ Remove Recipe",
                    key=f"remove_{i}"
                ):

                    st.session_state.saved_recipes.pop(i)

                    st.success("Recipe removed successfully.")
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
    "Made with ❤️ using Streamlit | Recipe Studio"
    "</p>",
    unsafe_allow_html=True
)
