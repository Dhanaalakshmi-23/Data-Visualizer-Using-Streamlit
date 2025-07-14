import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊  Data Visualizer')

working_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the folder where your CSV files are located
folder_path = f"{working_dir}/data"  # Update this to your folder path

# List all files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dropdown to select a file
selected_file = st.selectbox('Select a file', files, index=None)

if selected_file:
    # Construct the full path to the file
    file_path = os.path.join(folder_path, selected_file)

    # Read the selected CSV file
    df = pd.read_csv(file_path)

    from io import StringIO

# Display Data Summary
    st.subheader("📌 Data Summary")

# Show basic stats
    with st.expander("👀 View Head (Top 5 Rows)"):
        st.dataframe(df.head())

    with st.expander("📐 View Shape (Rows, Columns)"):
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    with st.expander("📊 View Describe (Statistics Summary)"):
        st.dataframe(df.describe())

    with st.expander("ℹ️ View Info (Data Types and Nulls)"):
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)


    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Theme selection
    theme = st.selectbox("Select Theme", ["Light", "Dark"])

    # Apply style based on theme
    if theme == "Dark":
        plt.style.use('dark_background')
        sns.set_theme(style="darkgrid")
    else:
        plt.style.use('default')
        sns.set_theme(style="whitegrid")


    # Generate the plot based on user selection
    if st.button('Generate Plot'):
        if x_axis == "None" or (plot_type != 'Count Plot' and y_axis == "None"):
            st.warning("Please select valid columns for X and Y axes.")
        else:
            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'

            ax.tick_params(axis='x', labelsize=10)
            ax.tick_params(axis='y', labelsize=10)
            plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)
            st.pyplot(fig)
