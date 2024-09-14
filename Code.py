import streamlit as st
import requests
import json

# RapidAPI credentials (replace with your actual RapidAPI key)
RAPIDAPI_KEY = "5655e1925cmsh3b43150048e8c3dp1b0b56jsne55049150f2d"  # Replace with your actual RapidAPI key

# Language-specific Hello World code snippets
hello_world_examples = {
    "Python": '''print("Hello, World!")''',
    "C++": '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello, C++!" << endl;
    return 0;
}''',
    "C": '''#include <stdio.h>

int main() {
    printf("Hello, C!\\n");
    return 0;
}''',
    "Java": '''public class Temp {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}''',
    "JavaScript": '''console.log("Hello, JavaScript!");'''
}

# Streamlit app title
st.title("Online Python, C++, C, Java, and JavaScript Compiler")

# Dropdown to select file type
filetype = st.selectbox("Choose language", ["Python", "C++", "C", "Java", "JavaScript"])

# Display Hello World code for the selected language
default_code = hello_world_examples[filetype]

# Code editor with default Hello World code based on the language selected
code = st.text_area("Write your code here", value=default_code, height=300)

# Language mapping for the API
language_map = {
    "Python": "python3",  # Python 3.x
    "C++": "cpp",         # C++
    "C": "c",             # C
    "Java": "java",       # Java
    "JavaScript": "nodejs"  # JavaScript using Node.js
}

# Initialize output variable to ensure it is always defined
output = ""

# Run button
if st.button("Run Code"):
    # API URL and Headers for RapidAPI
    url = "https://online-code-compiler.p.rapidapi.com/v1/"
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,  # Replace with your actual RapidAPI key
        'x-rapidapi-host': "online-code-compiler.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    # Define the payload for the API request
    payload = {
        "language": language_map[filetype],  # Correct language
        "version": "latest",                 # Use the latest version of the language
        "code": code,                        # The code entered by the user
        "input": None                        # No input provided (stdin)
    }

    # Make the request to RapidAPI
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        result = response.json()

        # Get the output after the execution completes
        if response.status_code == 200:
            output = result.get("output") or "No output returned"
        else:
            output = f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        output = f"An error occurred: {str(e)}"

    # Display the output
    st.subheader("Output:")
    st.code(output)
