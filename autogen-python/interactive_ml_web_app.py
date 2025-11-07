import streamlit as st
import pandas as pd
import numpy as np

st.title("Interactive AI Dashboard for Machine Learning & Data Analysis")
st.subheader("A faster way to build and share data apps!")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name} 👋")
 # st.set_page_config(page_title="QA assistant app")
# st.markdown("_Markdown : This is a simple QA assistant app!_")
# st.latex("area of triangle = 1/2 * b * h")
    file = st.file_uploader("Upload your financial data in csv format", type="csv")
    if file is not None:
        st.write("File Uploaded, Revieweing ...")
        st.write("Data Preview")
        df = pd.read_csv(file)
    # st.dataframe(df)
        st.write(df.head())
        st.write("Data Summary")

        st.write(df.describe())
        columns = df.columns.tolist()
    # selected_col = st.selectbox("Select Column to filter by", columns)
    # unique_val = df[selected_col].unique()
        st.subheader('Data Visualization: Plot Data')
        x_col = st.selectbox("Select X column", columns)
        y_col = st.selectbox("Select Y column", columns)

        if st.button("Generate Plot"):
            chart_df = df[[x_col, y_col]].set_index(x_col)
            st.line_chart(chart_df)

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
