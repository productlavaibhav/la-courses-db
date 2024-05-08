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
@st.cache_data
def load_titles():
    with open('C:/Users/ayush/Downloads/finalcourses.json', 'r') as file:
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
            course_details = fetch_data(token, selected_title)
            st.json(course_details)
        else:
            st.error("Failed to authenticate. Check the API key and network.")

if __name__ == "__main__":
    main()
