import streamlit as st
import pandas as pd
import numpy as np

st.title("Interactive AI Dashboard for Machine Learning & Data Analysis")
st.subheader("A faster way to build and share data apps!")
st.divider()

st.session_state["enter_name"] = False
st.session_state["file_uploaded"] = False
st.session_state["show_star"] = False

with st.chat_message("user"):
    name = st.text_input("Enter your name:")
    if name:
        st.success(f"Hello, {name} 👋")
        st.session_state["enter_name"] = True

# st.set_page_config(page_title="QA assistant app")
# st.markdown("_Markdown : This is a simple QA assistant app!_")
# st.latex("area of triangle = 1/2 * b * h")

if st.session_state["enter_name"]:
    with st.chat_message("user"):
        file = st.file_uploader("Upload your financial data in csv format", type="csv")
        if file is not None:
            with st.chat_message("assistant"):
                st.write("Thanks for uploading the file.")
                st.session_state["file_uploaded"] = True

if st.session_state["file_uploaded"]:
    st.write("Data Preview")
    st.session_state["show_feedback"] = False

    df = pd.read_csv(file)
    # st.dataframe(df)
    st.dataframe(df.head())
    st.divider()
    st.write("Data Summary")
    st.dataframe(df.describe())
    st.divider()
    columns = df.columns.tolist()
    # selected_col = st.selectbox("Select Column to filter by", columns)
    # unique_val = df[selected_col].unique()
    st.subheader('Data Visualization: Plot Data')
    chat = st.chat_message("user")
    x_col = chat.selectbox("Select X column", columns)
    y_col = chat.selectbox("Select Y column", columns)

        # Initialize session state properly
    if "show_chart" not in st.session_state:
        st.session_state["show_chart"] = False

        # When user clicks the button, show chart options
    if st.button("Generate Plot"):
        st.session_state["show_chart"] = True

        # If chart mode is activated, show chart type + plot
    if st.session_state["show_chart"]:
        chart_df = df[[x_col, y_col]].set_index(x_col)
        with st.chat_message("user"):
            chart_type = st.radio(
                "Select chart type",
                ["Line Chart", "Area Chart", "Scatter Chart"]
            )

            if chart_type == "Line Chart":
                st.line_chart(chart_df)

            elif chart_type == "Area Chart":
                st.area_chart(chart_df)

            elif chart_type == "Scatter Chart":
                st.scatter_chart(chart_df)
        st.session_state["show_feedback"] = True

    if st.session_state["show_feedback"]:
        with st.chat_message("user"):
            st.write("Enter your feedback")
            star = st.feedback("stars")
            if star:
                st.session_state["show_star"] = True

    if st.session_state["show_star"]:
        st.balloons()

#
# name = st.text_input("Enter your name:")
# if name:
#     st.success(f"Hello, {name} 👋")
#     test = st.text_input("What do you want to do?:")
#     if test:
#         st.success("Letz work together 👋")
#         # Create a button and display a message upon click
#         if st.button('Click me!'):
#             st.success('Button clicked successfully!')
#         # Create a slider widget
#         age = st.slider('Select your age:', min_value=0, max_value=100, value=30)
#         st.write(f'You are {age} years old.')
#         # Display a DataFrame
#         st.subheader('Sample Data')
#         data = {
#             'col1': np.random.rand(5),
#             'col2': np.random.randint(1, 100, 5),
#             'col3': ['A', 'B', 'C', 'D', 'E']
#         }
#         df = pd.DataFrame(data)
#         st.dataframe(df)
#         # Display a chart
#         st.subheader('Random Line Chart')
#         chart_data = pd.DataFrame(
#             np.random.randn(20, 3),
#             columns=['a', 'b', 'c']
#         )
#         st.subheader('Data Visualization')
#
#         st.line_chart(chart_data)

# streamlit run test-folder/app.py
