import streamlit as st
from file_utils import process_file
from chat_utils import load_chat_history, save_chat_history, get_assistant_response
import uuid  # For generating unique session IDs
import os

# Main app
def main():
    st.set_page_config(page_title="File Upload and Chat Interface", layout="wide")
    st.title("File Upload and Chat Interface App")

    # Define directories and files
    CHAT_HISTORY_DIR = "chat_histories"
    os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

    # Layout for chat session management and current chat interface
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Chat Sessions")
        
        # List chat sessions
        session_files = [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith('.json')]
        session_files = sorted(session_files, reverse=True)  # Sort to show recent sessions first

        selected_session = st.selectbox("Select Session", session_files)


        # Add a "Restart Session" button
        if st.button("Restart Session"):
            # Clear session state and cache
            st.session_state.clear()
            st.cache_data.clear()
            # Reload the page
            st.experimental_set_query_params()

        if selected_session:
            session_id = selected_session.replace(".json", "")
            st.session_state.session_id = session_id

            # Display chat history for the selected session
            chat_history = load_chat_history(session_id, CHAT_HISTORY_DIR)

            if chat_history:
                for message in chat_history:
                    role = message['role']
                    content = message['content']

        if selected_session:
            session_id = selected_session.replace(".json", "")
            st.session_state.session_id = session_id

            # Display chat history for the selected session
            chat_history = load_chat_history(session_id, CHAT_HISTORY_DIR)

            if chat_history:
                for message in chat_history:
                    role = message['role']
                    content = message['content']
                    if role == 'user':
                        st.markdown(f"""
                        <div style="padding: 10px; margin-bottom: 10px; border-radius: 15px; background-color: #1d1717; text-align: left;">
                            <strong style="color: #0000ff;">You:</strong> <p style="margin: 0; white-space: pre-wrap;">{content}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif role == 'assistant':
                        st.markdown(f"""
                        <div style="padding: 10px; margin-bottom: 10px; border-radius: 15px; background-color: #e0f7fa; color: #000000; text-align: left;">
                            <strong style="color: #004d40;">Assistant:</strong> <p style="margin: 0; white-space: pre-wrap;">{content}</p>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        st.header("Current Session Chat Interface")

        # Ensure a unique session ID for each user session
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        session_id = st.session_state.session_id

        # Chat input area
        user_input = st.text_area("Type your message here:", "", height=100)
        if st.button("Send"):
            if user_input:
                # Load chat history for the current session
                chat_history = load_chat_history(session_id, CHAT_HISTORY_DIR)

                # Add user message to chat history
                chat_history.append({'role': 'user', 'content': user_input})
                
                # Process the user message with OpenAI API
                assistant_response = get_assistant_response(user_input)
                
                # Add assistant response to chat history
                chat_history.append({'role': 'assistant', 'content': assistant_response})
                
                # Save updated chat history
                save_chat_history(session_id, chat_history, CHAT_HISTORY_DIR)
                
                # Display the assistant response
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 10px; border-radius: 15px; background-color: #e0f7fa; color: #000000; text-align: left;">
                    <strong style="color: #004d40;">Assistant:</strong> <p style="margin: 0; white-space: pre-wrap;">{assistant_response}</p>
                </div>
                """, unsafe_allow_html=True)

        # File upload
        uploaded_files = st.file_uploader("Choose files", type=["pdf", "csv", "txt"], accept_multiple_files=True)
        if uploaded_files:
            st.write("Files uploaded successfully.")
            for uploaded_file in uploaded_files:
                file_type = uploaded_file.type
                file_name = uploaded_file.name
                
                # Process the file based on its type
                result = process_file(uploaded_file, file_type)
                if result:
                    st.write(f"Processed file: {file_name} ({result['type']})")

if __name__ == "__main__":
    main()
