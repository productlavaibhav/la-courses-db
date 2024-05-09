import streamlit as st
import pandas as pd
import json

# Function to convert JSON data to DataFrame
def create_data_frame(course_details_list):
    ids, titles, canonicalTitles, isReleaseds, isSecrets, topicIds, topicTitles, topicVideoIdBcs, playbackTimes = [], [], [], [], [], [], [], [], []
    for course_details in course_details_list:
        for lesson in course_details.get('lessons', []):
            for topic in lesson.get('topics', []):
                ids.append(course_details.get('id'))
                titles.append(course_details.get('title'))
                canonicalTitles.append(course_details.get('canonicalTitle'))
                isReleaseds.append(course_details.get('isReleased'))
                isSecrets.append(course_details.get('isSecret'))
                topicIds.append(topic.get('topicId'))
                topicTitles.append(topic.get('title'))
                topicVideoIdBcs.append(topic.get('resource', {}).get('topicVideoIdBc', 'N/A'))
                playbackTimes.append(topic.get('resource', {}).get('playbackTime', 'N/A'))
    
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

# Streamlit app
st.title('JSON to DataFrame Converter')

uploaded_file = st.file_uploader("Choose a JSON file")
if uploaded_file is not None:
    # Read the uploaded JSON file
    json_data = json.load(uploaded_file)
    
    # Check if the JSON data is a list of course details
    if isinstance(json_data, list):
        # Convert JSON data to DataFrame
        df = create_data_frame(json_data)
        
        # Display the DataFrame in the app
        st.write(df)
    else:
        st.error("The uploaded file does not contain a list of course details.")
