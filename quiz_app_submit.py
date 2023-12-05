# Step 1: Import necessary modules
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import streamlit as st

# Step 2: Defined a function to create the quiz prompt template
def create_the_quiz_prompt_template():
    """Create the prompt template for the quiz app."""
    # Define the template with placeholders for dynamic inputs   
    template = """
    You ARE QUIZ Generator . Let us
    create a quiz  {num_questions}   {quiz_type} questions about the this topic: {quiz_context}.

    The format of the quiz could be one of the following:
    - Multiple-choice: 
    - Questions:
        <Question1>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
        <Question2>: <a. Answer 1>, <b. Answer 2>, <c. Answer 3>, <d. Answer 4>
        ....
    - Answers:
        <Answer1>: <a|b|c|d>
        <Answer2>: <a|b|c|d>
        ....
        Example:
        - Questions:
        - 1. What is the capital of France?
            a. London
            b. Paris
            c. Berlin
            d. Rome
        - Answers: 
            1. b
    - True-false:
        - Questions:
            <Question1>: <True|False>
            <Question2>: <True|False>
            .....
        - Answers:
            <Answer1>: <True|False>
            <Answer2>: <True|False>
            .....
        Example:
            Questions:
        - 1. The Earth is flat. True or False?

        Answers:
        - 1. False
    - Open-ended:
    - Questions:
        <Question1>: 
        <Question2>:
    - Answers:    
        <Answer1>:
        <Answer2>:
    Example:
        Questions:
        - 1. Explain the concept of artificial intelligence.
        - 2. What are the advantages of using renewable energy sources?

        Answers: 
            1. Artificial intelligence refers to the simulation of human intelligence in machines that are programmed to think and learn.
            2. Renewable energy sources, such as solar and wind power, offer environmental benefits and help reduce dependence on non-renewable resources.
    """
    # then I Created a PromptTemplate instance and format it with sample inputs

    prompt = PromptTemplate.from_template(template)
    prompt.format(num_questions=3, quiz_type="multiple-choice", quiz_context="Data Structures in Python Programming")
    
    return prompt

# Step 3: Defined a function to create the quiz chain
def create_quiz_chain(prompt_template, llm):
    """Creates the chain for the quiz app."""
    return LLMChain(llm=llm, prompt=prompt_template)

# Step 4: Defined a function to split questions and answers from the quiz response

def split_questions_answers(quiz_response):
    """Function that splits the questions and answers from the quiz response."""
    questions = quiz_response.split("Answers:")[0]
    answers = quiz_response.split("Answers:")[1]
    return questions, answers

# Step 5: Defined the main function for the Streamlit app

def present_quiz(questions):
    """Function to present the quiz questions to the user."""
    st.write("Answer the following questions:")
    for i, question in enumerate(questions.split("\n")[1:-1], 1):
        st.write(f"{i}. {question}")

def submit_quiz(questions, user_answers):
    """Function to submit the quiz and display the score."""
    correct_answers = st.session_state.answers.split("\n")[1:-1]
    user_answers = user_answers.split("\n")[1:-1]

    score = sum(user_ans == correct_ans for user_ans, correct_ans in zip(user_answers, correct_answers))
    st.write(f"Your Score: {score}/{len(correct_answers)}")

    st.write("Correct Answers:")
    for i, (user_ans, correct_ans) in enumerate(zip(user_answers, correct_answers), 1):
        st.write(f"{i}. Your Answer: {user_ans}, Correct Answer: {correct_ans}")

def main():
    # Set the app title
    st.title("PWC Quiz Generator APP")
    st.write("Let Us Create Some Fun Quizzes.")
    
    # Get the user's OpenAI API key
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    # Create the quiz prompt template
    prompt_template = create_the_quiz_prompt_template()
    
    # Create the ChatOpenAI model instance with the user's API key
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create the quiz chain
    chain = create_quiz_chain(prompt_template, llm)
    
    # Get user inputs for quiz topic, number of questions, and quiz type
    context = st.text_area("Enter the quiz topic")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=20, value=3)
    quiz_type = st.selectbox("Select the quiz type", ["multiple-choice", "true-false", "open-ended"])
    
    # Generate quiz if the "Quiz ME!" button is clicked
    if st.button("Quiz ME!"):
        quiz_response = chain.run(num_questions=num_questions, quiz_type=quiz_type, quiz_context=context)
        st.write("Quiz Generated!")        
        # Split and store questions and answers in session state
        questions, answers = split_questions_answers(quiz_response)
        st.session_state.answers = answers
        st.session_state.questions = questions
        present_quiz(questions)

        # Add an input box for the user to submit answers
        user_answers = st.text_area("Enter your answers (e.g., a, b, c, d)", key="user_answers")

        # Add a "Submit Answers" button
        if st.button("Submit Answers"):
            submit_quiz(questions, user_answers)

    # Show answers if the "Show Answers" button is clicked
    if st.button("Show Answers"):
        st.markdown(st.session_state.questions)
        st.write("----")
        st.markdown(st.session_state.answers)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
