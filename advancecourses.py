import streamlit as st
import pandas as pd
import json

# Function to process the JSON and extract desired information into a DataFrame
def extract_data(json_data):
    # Lists to hold the extracted data
    topic_ids = []
    bc_video_ids = []

    # Traversing through the course data to extract Topic ID and Topic Video BC ID
    for lesson in json_data.get('lessons', []):
        for topic in lesson.get('topics', []):
            topic_ids.append(topic.get('topicId'))
            bc_video_id = topic.get('resource', {}).get('topicVideoIdBc', 'N/A')
            bc_video_ids.append(bc_video_id)

    # Creating the DataFrame
    data = {
        'Topic ID': topic_ids,
        'BC Video ID': bc_video_ids
    }
    return pd.DataFrame(data)

# Streamlit app interface
st.title('Course Topics and Video IDs Extractor')

# File uploader
uploaded_file = st.file_uploader("Upload your course JSON file")
if uploaded_file is not None:
    # Read the uploaded JSON file
    course_data = json.load(uploaded_file)

    # Check if the data structure is as expected
    if isinstance(course_data, dict):
        # Extract data and create DataFrame
        df = extract_data(course_data)
        
        # Display the DataFrame in the app
        st.write(df)
    else:
        st.error("The uploaded file does not contain valid course details in the expected format.")

# Instructions for running the app
# To run this app, save the script as 'app.py', then use the command 'streamlit run app.py' in your terminal.
