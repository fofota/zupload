import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

# Function to parse HTML table into a DataFrame
def parse_html_table(html_content):
    # Replacing the first nat to Nationality, and the second one to NFi (Natural Fitness)
    html_content = html_content.decode('utf-8')  # Convert bytes to string 
    html_content = html_content.replace('<th>Nat</th>', '<th>Nationality</th>', 1)
    html_content = html_content.replace('<th>Nat</th>', '<th>NFi</th>')
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    return df

# Streamlit app
def main():
    st.title("Uploading Page for Z")

    # File uploader
    uploaded_file = st.file_uploader("Upload HTML file", type=["html"])

    if uploaded_file is not None:
        # Read content of the uploaded file
        html_content = uploaded_file.read()

        # Parse HTML table into DataFrame
        df = parse_html_table(html_content)

        # Display DataFrame
        st.write("Parsed DataFrame:")
        st.write(df)
    if st.button("Save as CSV"):
            df.to_csv("parsed_data.csv", index=False)
            st.success("DataFrame saved as CSV: parsed_data.csv")

if __name__ == "__main__":
    main()