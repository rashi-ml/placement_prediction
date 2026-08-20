# import streamlit as st 
# import pypickle as pk

# model=pk.load("placement_model.pkl")



# st.title("Placement Prediction")



# cgpa=st.slider("CGPA",1.0,10.0,7.0)
# apt_score=st.slider("Aptitude Score",1,100,55)
# commun_skill=st.slider("Communication Skill",1,10,5)
# Int=st.selectbox("Internship",["No","Yes"])
# project=st.number_input("Projects",0)

# submit=st.button("Predict placement",type="primary")

# if submit:
#     if Int =="Yes":
#         ins_v=1
#     else:
#         ins_v=0
#     result = model.predict([[cgpa,apt_score,commun_skill,ins_v,project]])
#     if result[0]==1:
#         st.success("Student can be placed😁")
#     else:
#         st.error("Student can not be placed😵")

import streamlit as st
import pickle
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Placement Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .prediction-card {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .recommendation {
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():

    with open("placement_model.pkl", "rb") as file:
        model = pickle.load(file)

    return model


try:
    model = load_model()

except FileNotFoundError:

    st.error(
        "❌ placement_model.pkl was not found. "
        "Please place the model file in the same folder as app.py."
    )

    st.stop()

except Exception as e:

    st.error(f"❌ Error loading model: {e}")

    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
        width=100
    )

    st.header("🎓 Placement Predictor")

    st.write(
        "An AI-powered application that predicts "
        "whether a student is likely to get placed "
        "based on academic and professional attributes."
    )

    st.divider()

    st.subheader("📌 Model Features")

    st.write("• CGPA")
    st.write("• Aptitude Score")
    st.write("• Communication Skill")
    st.write("• Internship")
    st.write("• Number of Projects")

    st.divider()

    st.caption("Machine Learning Placement Prediction System")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 AI Placement Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict a student\'s placement probability using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# TOP INFORMATION CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🤖 Model", "ML Model")

with col2:
    st.metric("📊 Features", "5")

with col3:
    st.metric("🎯 Prediction", "Binary")

with col4:
    st.metric("⚡ Response", "Instant")


st.divider()


# --------------------------------------------------
# STUDENT INPUT SECTION
# --------------------------------------------------

st.subheader("👨‍🎓 Student Information")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### 📚 Academic Performance")

    cgpa = st.slider(
        "CGPA",
        min_value=1.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    aptitude_score = st.slider(
        "Aptitude Score",
        min_value=1,
        max_value=100,
        value=55
    )


with col2:

    st.markdown("### 💼 Professional Skills")

    communication_skill = st.slider(
        "Communication Skill",
        min_value=1,
        max_value=10,
        value=5
    )

    internship = st.selectbox(
        "Internship Experience",
        ["No", "Yes"]
    )

    projects = st.number_input(
        "Number of Projects",
        min_value=0,
        max_value=20,
        value=2,
        step=1
    )


st.divider()


# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

st.subheader("📋 Student Profile")

internship_value = 1 if internship == "Yes" else 0

profile = pd.DataFrame(
    {
        "Parameter": [
            "CGPA",
            "Aptitude Score",
            "Communication Skill",
            "Internship",
            "Projects"
        ],
        "Value": [
            cgpa,
            aptitude_score,
            communication_skill,
            internship,
            projects
        ]
    }
)

st.dataframe(
    profile,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

col1, col2, col3 = st.columns([1, 1, 2])

with col1:

    predict_button = st.button(
        "🚀 Predict Placement",
        type="primary",
        use_container_width=True
    )

with col2:

    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True
    )

if reset_button:
    st.rerun()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict_button:

    # Create model input
    input_data = [[
        cgpa,
        aptitude_score,
        communication_skill,
        internship_value,
        projects
    ]]

    try:

        prediction = model.predict(input_data)

        result = prediction[0]

        st.divider()

        st.subheader("🤖 Prediction Result")

        # --------------------------------------------------
        # PROBABILITY
        # --------------------------------------------------

        probability = None

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(input_data)

            probability = probabilities[0][1] * 100


        # --------------------------------------------------
        # PLACED
        # --------------------------------------------------

        if result == 1:

            st.success(
                "🎉 Student is likely to get placed!"
            )

            if probability is not None:

                st.metric(
                    "Placement Probability",
                    f"{probability:.2f}%"
                )

                st.progress(
                    int(probability)
                )

            st.balloons()

            st.markdown(
                """
                ### 🎯 Recommendation

                The student has a positive placement prediction.

                Continue improving:
                - Technical skills
                - Communication
                - Aptitude preparation
                - Real-world projects
                - Internship experience
                """
            )

        # --------------------------------------------------
        # NOT PLACED
        # --------------------------------------------------

        else:

            st.error(
                "⚠️ Student may have difficulty getting placed."
            )

            if probability is not None:

                st.metric(
                    "Placement Probability",
                    f"{probability:.2f}%"
                )

                st.progress(
                    int(probability)
                )

            st.markdown(
                """
                ### 💡 Improvement Recommendations

                The student should focus on:

                🔹 Improving CGPA

                🔹 Practicing aptitude questions

                🔹 Improving communication skills

                🔹 Completing industry-relevant projects

                🔹 Getting internship experience

                🔹 Preparing for technical interviews
                """ 
            )


        # --------------------------------------------------
        # FEATURE ANALYSIS
        # --------------------------------------------------

        st.divider()

        st.subheader("📊 Student Performance Analysis")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "CGPA",
                f"{cgpa}/10"
            )

        with metric2:

            st.metric(
                "Aptitude",
                f"{aptitude_score}/100"
            )

        with metric3:

            st.metric(
                "Communication",
                f"{communication_skill}/10"
            )


        # --------------------------------------------------
        # PERFORMANCE CHART
        # --------------------------------------------------

        chart_data = pd.DataFrame(
            {
                "Skill": [
                    "CGPA",
                    "Aptitude",
                    "Communication",
                    "Projects"
                ],

                "Score": [
                    cgpa * 10,
                    aptitude_score,
                    communication_skill * 10,
                    min(projects * 10, 100)
                ]
            }
        )

        st.subheader("📈 Performance Overview")

        st.bar_chart(
            chart_data.set_index("Skill")
        )


    except Exception as e:

        st.error(
            f"❌ Prediction failed: {e}"
        )


# --------------------------------------------------
# ABOUT SECTION
# --------------------------------------------------

st.divider()

with st.expander("ℹ️ About this application"):

    st.write(
        """
        ### AI Placement Predictor

        This application uses a trained Machine Learning model
        to predict whether a student is likely to get placed.

        The model uses the following input features:

        1. CGPA
        2. Aptitude Score
        3. Communication Skill
        4. Internship Experience
        5. Number of Projects

        The prediction is generated using the trained
        `placement_model.pkl` model.

        **Note:** The prediction is an ML-based estimate and
        should not be treated as a guaranteed placement outcome.
        """
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <br>
    <center>
    🎓 <b>AI Placement Predictor</b><br>
    Built with Python, Machine Learning & Streamlit
    </center>
    """,
    unsafe_allow_html=True
)




