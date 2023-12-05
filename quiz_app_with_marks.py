# Step 1: Import necessary modules
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import streamlit as st

# Step 2: I Defined a function to create the quiz prompt template
def create_the_quiz_prompt_template():
    """Create the prompt template for the quiz app."""
    # Define the template with placeholders for dynamic inputs   
    template = """
    You ARE QUIZ Generator . Let us
    create a quiz  {num_questions}   {quiz_type} questions about the this topic: {quiz_context}.

    The format of the quiz could be one of the following:
    - Multiple-choice: 
        <Question1>: <Answer a>, <Answer b>, <Answer c>, <Answer d>
        <Question2>: <Answer a>, <Answer b>, <Answer c>, <Answer d>
        ....
    - Answers:
        <Answer1>: a
        <Answer2>: b
        ....
        Example:
        - 1. What is the capital of France?
            a. London
            b. Paris
            c. Berlin
            d. Rome
    Example:
    - Questions:
        <Question1>: <Answer a>, <Answer b>, <Answer c>, <Answer d>
        <Question2>: <Answer a>, <Answer b>, <Answer c>, <Answer d>
        ....
    - Answers:
        <Answer1>: a
        <Answer2>: b
        ....
        Example:
        - Questions:
        - 1. What is the capital of France?
            a. London
            b. Paris
            c. Berlin
            d. Rome
        - Answers:
            b
    """

    # then I Created a PromptTemplate instance and format it with sample inputs
    prompt = PromptTemplate.from_template(template)
    prompt.format(num_questions=1, quiz_type="multiple-choice", quiz_context="animals")

    return prompt

# Step 3: I Defined a function to create the quiz chain
def create_quiz_chain(prompt_template, llm):
    """Creates the chain for the quiz app."""
    return LLMChain(llm=llm, prompt=prompt_template)

# Step 4: I Defined a function to split questions and answers from the quiz response
def split_questions_answers(quiz_response):
    """Function that splits the questions and answers from the quiz response."""
    questions = quiz_response.split("Answers:")[0]
    answers = quiz_response.split("Answers:")[1]
    return questions, answers

# Step 5: I Defined the main function for the Streamlit app
def main():
    # Set the app title
    st.title("PWC Quiz Generator APP")
    st.write("Let Us Create Some Fun Quizzes.")
    
    # Get the user's OpenAI API key
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    # Create the quiz prompt template
    prompt_template = create_the_quiz_prompt_template()
    
    # Create the ChatOpenAI model instance with the user's API key and set the model name with temprature to get more random results
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Create the quiz chain
    chain = create_quiz_chain(prompt_template, llm)
    
    # Get user inputs for quiz topic, number of questions
    context = st.text_area("Enter the quiz topic")
    num_questions = st.number_input("Enter the number of questions", min_value=1, max_value=20, value=1)
    
    # Generate quiz if the "Quiz ME!" button is clicked
    if st.button("Quiz ME!"):
        quiz_response = chain.run(num_questions=num_questions, quiz_type="multiple-choice", quiz_context=context)
        st.write("Quiz Generated!")        
        # Split and store questions and answers in session state
        questions, answers = split_questions_answers(quiz_response)
        st.session_state.answers = answers
        st.session_state.questions = questions
        st.write(questions)
    # I created a form to save the user answers
    with st.form("my_form"):
        # Add a text input to the form
        user_input = st.text_input("Enter your answer for the question:")

        # Add a button to the form so we can save the answer
        submitted = st.form_submit_button("Submit")

    # Check if the form is submitted
    if submitted:
        # Process the user input
        # Split the input string by commas and convert it to a set to get unique elements
        user_set = list(user_input.split(','))

        # Sort my answers so i can compare them correctly
        sorted_answers = sorted(user_set)
        st.write("You entered:", sorted_answers)
        lettered_answers = [answer.split()[-1] for answer in list(st.session_state.answers.split("\n")) if answer.strip()]
        
        st.write("the correct answers are:", lettered_answers)
        Score = 0
        
        st.write("the questions were",(st.session_state.questions))

        # Compare and increment counter for each match
        for user_answer, correct_answer in zip(sorted_answers, lettered_answers):
            if user_answer == correct_answer:
                Score += 1
        st.write("your mark is",Score)

    # Show answers if the "Show Answers" button is clicked
    if st.button("Show Answers"):
        st.markdown(st.session_state.questions)
        st.write("----")
        st.markdown(st.session_state.answers)

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
