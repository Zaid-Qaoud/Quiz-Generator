Quiz Generator App Documentation

Overview:

The Quiz Generator App is a Streamlit-based application designed to facilitate the effortless creation of custom quizzes. This application leverages the LangChain library for natural language processing and the OpenAI GPT-3.5-turbo model for generating quiz content.

Code Structure:

1. Imports:
    - The script imports necessary modules from LangChain and Streamlit.

2. Prompt Template Creation:
    - create_the_quiz_prompt_template(): Defines a function to create a prompt template for quiz generation. The template is dynamically formatted using the LangChain library.

3. Quiz Chain Creation:
    - create_quiz_chain(prompt_template, llm): Creates a LangChain model chain for quiz generation using the specified prompt template and ChatOpenAI model.

4. Splitting Questions and Answers:
    - split_questions_answers(quiz_response): Defines a function to split the questions and answers from the generated quiz response.

5. Main Application:
    - main(): The main function sets up the Streamlit app interface, allowing users to input the quiz topic, number of questions, and quiz type. It then generates and displays the quiz, as well as provides an option to reveal the answers.

Usage:

1. Launching the App:
    - Run the script, and the Streamlit app will be launched.

2. Input Parameters:
    - Enter the quiz topic, the number of questions, and select the quiz type (multiple-choice, true-false, open-ended).

3. Generate Quiz:
    - Click the "Quiz ME!" button to generate a quiz based on the provided inputs.

4. View Questions:
    - The generated questions will be displayed on the app.

5. Show Answers:
    - Click the "Show Answers" button to reveal the corresponding answers.

How to Run the Code:

- Ensure you have the required dependencies installed (LangChain, Streamlit).
- Set up an OpenAI API key and replace it in the script.
- Make sure your OpenAI library version is 0.28.0.
- Open a terminal or command prompt.
- Navigate to the directory containing the script.
- Run the script from cmd if you are using windows:
    ```
    streamlit run  quiz_app.py
    ```
- after running the code insure that you write your openai key correctly in the enter your api key tab 

Dependencies:

- LangChain
- Streamlit
- OpenAI GPT-3.5-turbo model

Important Note:

- Ensure the OpenAI library version is 0.28.0. Compatibility with other versions is not guaranteed.
- note that quiz_app_submit.py is a prototype and have issue with submitting the user answers

Customization:

- The template for quiz generation can be modified within the create_the_quiz_prompt_template() function to suit specific requirements.
