import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Page 1 - Load CSV file
def page_load_data():
    st.title("Load CSV File")
    file = st.file_uploader("Upload a CSV file", type="csv")
    
    if file is not None:
        df = pd.read_csv(file)
        st.dataframe(df)
        st.session_state["data"] = df
        st.success("File uploaded successfully!")

# Page 2 - Data description and statistics
def page_data_stats():
    st.title("Data Description")
    st.write("Data information and statistics:")
    data = st.session_state["data"]
    st.write(data.info())
    st.write(data.describe())

# Page 3 - Custom line chart
def page_custom_line_chart():
    st.title("Custom Line Chart")
    st.write("Select X and Y columns to create a line chart:")
    data = st.session_state["data"]
    columns = data.columns.tolist()
    x_column = st.selectbox("Select X column", columns)
    y_column = st.selectbox("Select Y column", columns)
    
    # Generate line chart
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_column], data[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    st.pyplot(plt)

# Page 4 - Histograms
def page_histograms():
    st.title("Histograms")
    st.write("Select a column to create a histogram:")
    data = st.session_state["data"]
    column = st.selectbox("Select column", data.columns)
    
    # Generate histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True)
    st.pyplot(plt)

# Page 5 - Column count
def page_column_count():
    st.title("Column Count")
    st.write("Select a column to count its values:")
    data = st.session_state["data"]
    column = st.selectbox("Select column", data.columns)
    
    # Count values
    value_counts = data[column].value_counts()
    st.write(value_counts)

# Page 6 - Map longitude and latitude
def page_map():
    st.title("Map Longitude and Latitude")
    st.write("Specify Longitude and Latitude columns to map:")
    data = st.session_state["data"]
    lat_column = st.selectbox("Select Latitude column", data.columns)
    lon_column = st.selectbox("Select Longitude column", data.columns)
    
    # Create map
    map_data = data[[lat_column, lon_column]].dropna()
    m = folium.Map(location=[map_data[lat_column].mean(), map_data[lon_column].mean()], zoom_start=10)
    for index, row in map_data.iterrows():
        folium.Marker(location=[row[lat_column], row[lon_column]]).add_to(m)
    st.write(m)

# Main function to run the application
def main():
    st.set_page_config(layout="wide")

    # Page selection sidebar
    page = st.sidebar.selectbox("Select a page",
                                ("Load Data", "Data Description", "Custom Line Chart",
                                 "Histograms", "Column Count", "Map Longitude and Latitude"))

    # Load data
    if page == "Load Data":
        page_load_data()

    # Check if data is loaded
    if "data" not in st.session_state:
        st.warning("Please load a CSV file first.")
        return

    # Page navigation
    if page == "Data Description":
        page_data_stats()
    elif page == "Custom Line Chart":
        page_custom_line_chart()
    elif page == "Histograms":
        page_histograms()
    elif page == "Column Count":
        page_column_count()
    elif page == "Map Longitude and Latitude":
        page_map()

if __name__ == "__main__":
    main()
