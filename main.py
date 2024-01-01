import streamlit as st
from sqlalchemy.exc import OperationalError
from methods import get_db_credentials_state, get_learn_questions_db_chain
import os
from dotenv import load_dotenv
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

# Initialize session state
if 'question_history' not in st.session_state:
    st.session_state.question_history = {}
if 'history_updated' not in st.session_state:
    st.session_state.history_updated = False


st.title("Data Retrieval in Natural Language")
#st.image("", width=200)

# Sidebar for database credentials and database selection
with st.sidebar:
    st.subheader("Database Selection")
    connect_to_default = st.checkbox("Connect to Default Sakila Database", True)
    if not connect_to_default:
        st.subheader("Custom Database Credentials")
        db_user = st.text_input("User", get_db_credentials_state()["db_user"])
        db_password = st.text_input("Password", get_db_credentials_state()["db_password"], type="password")
        db_host = st.text_input("Host", get_db_credentials_state()["db_host"])
        db_name = st.text_input("Database Name", get_db_credentials_state()["db_name"])

# Database connection and loading spinner
with st.spinner("Connecting to the database..."):
    try:
        if connect_to_default:
            # Use the default Sakila database
            db_user, db_password, db_host, db_name = "root", "", "localhost", "sakila"
            st.session_state.db_credentials = {"db_user": db_user, "db_password": db_password, "db_host": db_host, "db_name": db_name}
        else:
            # Update the session state with the latest custom credentials
            credentials_state = get_db_credentials_state()
            credentials_state["db_user"] = db_user
            credentials_state["db_password"] = db_password
            credentials_state["db_host"] = db_host
            credentials_state["db_name"] = db_name
        
        # Fetch the answer based on the provided database information
        chain = get_learn_questions_db_chain(db_user, db_password, db_host, db_name)

        # User input question
        if db_name.lower() == "sakila": 
            question = st.text_input("Enter your question:", "e.g., What are the top 5 films in the database?")
        else:
            question = st.text_input("Enter your question:")
            
        # Generate a unique identifier for the question (you can use a hash function, for simplicity, we use the question itself)
        question_id = hash(question)
        
        if question_id not in st.session_state.question_history and not st.session_state.history_updated:
        # Set the flag to True to indicate that history has been updated for this question
            st.session_state.history_updated = True
            
            # Error handling
            response = chain.run(question)

            # Update question history in session state
            history_entry = {"question": question, "answer": response}
            st.session_state.question_history.append(history_entry)

            # Display answer
            if response is None:
                st.error("Sorry, we couldn't find an answer to your question. Please try another one.")
            else:
                # Display answer
                st.success("Answer:")
                st.write(response)
        else:
            st.warning("This question has already been asked. Watch the previous answer in show history.")
            st.session_state.history_updated = False

    except OperationalError as e:
        st.error("Error connecting to the database. Please check your database credentials and try again. If you don't have a database, select the 'Connect to Default Sakila Database' option.")
        st.error(f"Error details: {str(e)}")


# History section
if st.button("Show History"):
    # Retrieve and display the question history from session state
    history = st.session_state.question_history

    st.write("Question History:")
    for entry in history:
        st.write(f"Question: {entry['question']}")
        st.write(f"Answer: {entry['answer']}")
        st.write("---")