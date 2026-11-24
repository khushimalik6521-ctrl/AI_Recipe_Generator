
import streamlit as st
from google import genai

# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Recipe Studio",
    page_icon="🍳",
    layout="wide"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #fff9f2;
}

.main-title {
    text-align: center;
    color: #d96842;
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #78675e;
    font-size: 17px;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #e8754d;
    color: white;
    border-radius: 12px;
    border: none;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #c95b36;
    color: white;
}

.recipe-box {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #f0ddce;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<div class="main-title">🍳 AI Recipe Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Discover delicious recipes using the ingredients you already have!</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# INTRODUCTION
st.subheader("🥗 Let's create something delicious!")
st.write("Tell us what you have in your kitchen.")

# INPUT FORM
with st.form("recipe_form"):

    col1, col2 = st.columns(2)

    with col1:
        ingredients = st.text_area(
            "🥕 Available Ingredients",
            placeholder="Example: Paneer, Tomato, Potato, Onion...",
            height=130
        )

        cuisine = st.selectbox(
            "🌍 Select Cuisine",
            [
                "Indian",
                "South Indian",
                "Italian",
                "Chinese",
                "Mexican",
                "Continental"
            ]
        )

        food_type = st.selectbox(
            "🥗 Food Preference",
            ["Vegetarian", "Non-Vegetarian", "Vegan"]
        )

    with col2:
        cooking_time = st.selectbox(
            "⏱️ Available Cooking Time",
            [
                "15 minutes",
                "30 minutes",
                "45 minutes",
                "60 minutes"
            ]
        )

        difficulty = st.selectbox(
            "👩‍🍳 Cooking Difficulty",
            ["Easy", "Medium", "Advanced"]
        )

        servings = st.selectbox(
            "🍽️ Number of Servings",
            [1, 2, 3, 4, 5, 6]
        )

    submitted = st.form_submit_button(
        "✨ Generate My Recipe"
    )

# GENERATE RECIPE ONLY AFTER BUTTON CLICK
if submitted:

    if not ingredients.strip():
        st.warning("Please enter your available ingredients.")

    else:
        prompt = f"""
        You are a professional chef and recipe assistant.

        Create one delicious and practical recipe using these details:

        Available ingredients: {ingredients}
        Cuisine: {cuisine}
        Food preference: {food_type}
        Available cooking time: {cooking_time}
        Difficulty: {difficulty}
        Servings: {servings}

        Follow these rules:
        1. Respect the selected food preference.
        2. Prefer the ingredients provided by the user.
        3. Mention any additional ingredients separately.
        4. Keep the cooking instructions simple and clear.
        5. Do not claim the recipe is ready in less time than
           realistically required.

        Format your answer with these headings:

        # Recipe Name
        Short description

        ## Preparation Time
        ## Cooking Time
        ## Difficulty
        ## Ingredients
        ## Step-by-Step Instructions
        ## Chef's Tips
        ## Serving Suggestions

        Keep the response concise, attractive and easy to follow.
        """

        try:
            with st.spinner("👩‍🍳 Creating your recipe..."):

                client = genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config={
                        "temperature": 0.6,
                        "max_output_tokens": 1100
                    }
                )

                recipe = response.text

                if not recipe:
                    st.error("No recipe was returned. Please check later.")
                else:
                    st.session_state["recipe"] = recipe

                client.close()

        except Exception as error:
            st.error(
                "Recipe generation failed. Please check your API "
                "configuration and quota. No automatic retry was made."
            )
            print("Error:", str(error))

# DISPLAY GENERATED RECIPE
if st.session_state.get("recipe"):

    st.divider()
    st.subheader("🍽️ Your Personalized Recipe")

    st.markdown(
        '<div class="recipe-box">',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state["recipe"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.success("Your recipe has been created successfully!")

    st.download_button(
        label="📥 Download Recipe",
        data=st.session_state["recipe"],
        file_name="my_recipe.txt",
        mime="text/plain"
    )

st.divider()

st.markdown(
    "<center>Made with ❤️ using Generative AI</center>",
    unsafe_allow_html=True
)
