import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import boto3

# AWS S3 credentials and settings
AWS_ACCESS_KEY_ID = 'AKIA2UC3FZENMNUVYZEL'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'eu-north-1'
S3_BUCKET_NAME = 'zupload1015'

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

# Function to upload CSV to AWS S3
def upload_to_s3(df, bucket, filename):
    csv_data = df.to_csv(index=False).encode('utf-8')
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    s3.put_object(Bucket=bucket, Key=filename, Body=csv_data)

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
            # Save CSV locally
            local_csv_path = "parsed_data.csv"
            df.to_csv(local_csv_path, index=False)
            
            # Upload CSV to AWS S3
            upload_to_s3(df, S3_BUCKET_NAME, "parsed_data.csv")
            
            st.success("DataFrame saved as CSV: parsed_data.csv and uploaded to AWS S3")

if __name__ == "__main__":
    main()