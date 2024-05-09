import streamlit as st
import requests
import json
import pandas as pd

# Set the page configuration for full width
st.set_page_config(layout="wide")

# Function to get the authentication token
def get_auth_token():
    url = 'https://hydra.prod.learnapp.com/auth/refresh'
    headers = {
        'x-api-key': 'u36jbrsUjD8v5hx2zHdZNwqGA6Kz7gsm',
        'Content-Type': 'application/json'
    }
    data = {"grantType": "refresh_token"}
    response = requests.post(url, headers=headers, json=data)
    return response.json().get('accessToken')

# Function to fetch data using the token and canonical titles
def fetch_data(token, canonical_titles):
    course_details_list = []
    for title in canonical_titles:
        url = f'https://catalog.prod.learnapp.com/catalog/courses/titles/{title}'
        headers = {
            'accept': '*/*',
            'authorization': f'Bearer {token}',
            'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
        }
        response = requests.get(url, headers=headers)
        course_details_list.append(response.json())
    return course_details_list

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

# Load JSON data for courses, titles, and subjects
@st.cache_data
def load_courses():
    with open('finalcourses.json', 'r') as file:
        courses = json.load(file)
    return courses

# Main function to run the app
def main():
    st.title("Course Data Viewer")

    # Load courses and extract titles and subjects
    courses = load_courses()
    subjects = list(set(course['subject'] for course in courses))  # Unique subjects
    titles = [course['canonicalTitle'] for course in courses]  # All titles initially

    # Multi-select for subjects
    selected_subjects = st.multiselect("Select a Subject", subjects)

    # Filter titles based on selected subjects
    if selected_subjects:
        filtered_titles = [course['canonicalTitle'] for course in courses if course['subject'] in selected_subjects]
    else:
        filtered_titles = titles  # No filter applied if no subjects selected

    # Multi-select to select multiple course titles from the filtered list
    selected_titles = st.multiselect("Select Course Titles", filtered_titles)

    if st.button("Fetch Course Details"):
        token = get_auth_token()
        if token:
            course_details_list = fetch_data(token, selected_titles)
            if course_details_list:
                df = create_data_frame(course_details_list)
                st.dataframe(df)
            else:
                st.write("No data available for the selected titles.")  # Fallback if no data is fetched
        else:
            st.error("Failed to authenticate. Check the API key and network.")

if __name__ == "__main__":
    main()
