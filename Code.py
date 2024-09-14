import streamlit as st
import subprocess
import os

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

# Run button
if st.button("Run Code"):
    # Define the filename and compiler based on the selected language
    if filetype == "C++":
        filename = "temp.cpp"
        compiler = "g++"
    elif filetype == "C":
        filename = "temp.c"
        compiler = "gcc"
    elif filetype == "Java":
        filename = "Temp.java"
    elif filetype == "JavaScript":
        filename = "temp.js"
    else:
        filename = "temp.py"
    
    # Save the code to a temporary file
    with open(filename, "w") as f:
        f.write(code)
    
    try:
        if filetype == "Python":
            # Run Python code directly
            result = subprocess.run(["python", filename], capture_output=True, text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr

        elif filetype in ["C++", "C"]:
            # Compile C or C++ code first
            exe_file = "temp_exe"
            compile_result = subprocess.run([compiler, filename, "-o", exe_file], capture_output=True, text=True, timeout=10)
            
            if compile_result.returncode == 0:
                # If compilation is successful, run the executable
                run_result = subprocess.run([f"./{exe_file}"], capture_output=True, text=True, timeout=10)
                output = run_result.stdout if run_result.stdout else run_result.stderr
            else:
                # Compilation failed, return error
                output = compile_result.stderr

        elif filetype == "Java":
            # Compile Java code
            compile_result = subprocess.run(["javac", filename], capture_output=True, text=True, timeout=10)

            if compile_result.returncode == 0:
                # Run the compiled Java class
                run_result = subprocess.run(["java", "Temp"], capture_output=True, text=True, timeout=10)
                output = run_result.stdout if run_result.stdout else run_result.stderr
            else:
                # Compilation failed, return error
                output = compile_result.stderr

        elif filetype == "JavaScript":
            # Execute JavaScript code using Node.js
            result = subprocess.run(["node", filename], capture_output=True, text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        output = "Error: Code execution timed out."

    # Clean up temporary files
    if os.path.exists(filename):
        os.remove(filename)
    if filetype in ["C++", "C"] and os.path.exists(exe_file):
        os.remove(exe_file)
    if filetype == "Java" and os.path.exists("Temp.class"):
        os.remove("Temp.class")
    
    # Display the output
    st.subheader("Output:")
    st.code(output)