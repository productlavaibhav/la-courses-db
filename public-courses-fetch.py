import streamlit as st
import requests
import json

# Function to get the authentication token
def get_auth_token():
    url = 'https://hydra.prod.learnapp.com/auth/refresh'
    headers = {
        'x-api-key': 'u36jbrsUjD8v5hx2zHdZNwqGA6Kz7gsm',
        'Content-Type': 'application/json'
    }
    data = {"grantType": "refresh_token"}
    response = requests.post(url, headers=headers, json=data)
    access_token = response.json().get('accessToken')  # Retrieve the access token as a string
    return access_token

# Function to fetch data using the token and a canonical title
def fetch_data(token, canonical_title):
    url = f'https://catalog.prod.learnapp.com/catalog/courses/titles/{canonical_title}'
    headers = {
        'accept': '*/*',
        'authorization': f'Bearer {token}',
        'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()
    return {k: v for k, v in response_data.items() if k not in ['assets', 'mentors']}

# Load JSON data
@st.cache
def load_titles():
    with open('finalcourses.json', 'r') as file:
        courses = json.load(file)
        titles = [course['canonicalTitle'] for course in courses]
    return titles

def main():
    st.title("Course Data Viewer")
    titles = load_titles()
    selected_title = st.selectbox("Select a Course Title", titles)
    if st.button("Fetch Course Details"):
        token = get_auth_token()
        if token:
            course_data = fetch_data(token, selected_title)
            #st.json(course_data)  # Show JSON data in Streamlit
            
            st.title(course_data["title"])
            st.subheader(course_data["summary"])
            st.text(f"Difficulty: {course_data['difficulty']} | Subject: {course_data['subject']}")

            # Features
            st.write("Course Features:")
            for feature in course_data["features"]:
                st.write(f"- {feature}")

            # Mentor Section
            avatar_url = f"https://assets.learnapp.com/catalog/courses/8c38e496-ca22-4020-b719-7a253976ef58/{mentors['avatar']}"
            st.image(avatar_url, caption=mentors['name'], width=300)  # Setting width is optional, adjust based on your layout needs
            st.write(f"**Name:** {mentors['name']}")
            st.write(f"**About:** {mentors['about']}")

            

            

            # Lessons
            st.subheader("Lessons")
            for lesson in course_data["lessons"]:
                with st.expander(lesson["title"]):
                    st.write(lesson["summary"])
                    st.subheader("Topics Covered")
                    for topic in lesson["topics"]:
                        st.write("- " + topic["title"])

            # Language Selection
            st.subheader("Select Language")
            language = st.selectbox("Choose a language", course_data["languages"])  # Assuming it's 'languages', not 'language'
            st.write(f"You selected the language: {language}")
        else:
            st.error("Failed to authenticate. Check the API key and network.")

if __name__ == "__main__":
    main()
