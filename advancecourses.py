import streamlit as st
import pandas as pd
import json

# Function to process the JSON and extract comprehensive information into a DataFrame
def extract_data(json_data):
    # Lists to hold the extracted data
    ids, titles, canonicalTitles, isReleaseds, isSecrets = [], [], [], [], []
    topicIds, topicTitles, topicVideoIdBcs, playbackTimes = [], [], [], []

    # Traversing through the course data to extract various details
    for lesson in json_data.get('lessons', []):
        for topic in lesson.get('topics', []):
            # Appending course-level details
            ids.append(json_data.get('id'))
            titles.append(json_data.get('title'))
            canonicalTitles.append(json_data.get('canonicalTitle'))
            isReleaseds.append(json_data.get('isReleased'))
            isSecrets.append(json_data.get('isSecret'))
            # Appending topic-level details
            topicIds.append(topic.get('topicId'))
            topicTitles.append(topic.get('title'))
            topicVideoId = topic.get('resource', {}).get('topicVideoIdBc', 'N/A')
            topicVideoIdBcs.append(topicVideoId)
            playbackTime = topic.get('resource', {}).get('playbackTime', 'N/A')
            playbackTimes.append(playbackTime)

    # Creating the DataFrame
    data = {
        'ID': ids,
        'Title': titles,
        'Canonical Title': canonicalTitles,
        'Is Released': isReleaseds,
        'Is Secret': isSecrets,
        'Topic ID': topicIds,
        'Topic Title': topicTitles,
        'Topic Video ID': topicVideoIdBcs,
        'Playback Time': playbackTimes
    }
    return pd.DataFrame(data)

# Streamlit app interface
st.title('Comprehensive Course Data Extractor')

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
