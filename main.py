import logging
from datetime import datetime
import pandas as pd
import openai
from google.cloud import secretmanager, bigquery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import functions_framework
import datastore_util
import dialog_util
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

# Configuration class
class CFG:
    # Model configurations and paths
    embeddings_model_repo = 'T-Systems-onsite/cross-en-de-roberta-sentence-transformer'
    Embeddings_path = './faiss_index_hp/'

# Load embeddings and vector DB
embeddings = HuggingFaceInstructEmbeddings(model_name=CFG.embeddings_model_repo, model_kwargs={"device": "cpu"})
vectordb = FAISS.load_local(CFG.Embeddings_path, embeddings)

def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def request_gpt(messages, temperature):
    # Function to make requests to GPT
    pass

def generate(prompt, history, user_id=None, thread_id=None, temperature=0.5, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0):
    # Main generation function
    pass

@functions_framework.http
def handle_chat(request):
    """Handles incoming messages and events from Google Chat."""
    event_data = request.get_json()
    logging.info("Received event_data: %s", event_data)

    event_type = event_data['type']

    # Handle event based on its type
    if event_type == 'ADDED_TO_SPACE':
        return handle_added_to_space(event_data)
    elif event_type == 'REMOVED_FROM_SPACE':
        return handle_removed_from_space()
    elif event_type == 'MESSAGE':
        return process_message_event(event_data)
    elif event_type == 'CARD_CLICKED':
        return handle_card_clicked(event_data)
    else:
        logging.warning("Unhandled event type: %s", event_type)
        return {}

def handle_added_to_space(event_data):
    """Handles the event when the bot is added to a space."""
    space_type = event_data['space']['type']

    if space_type == 'ROOM':
        return {"text": "Thanks for adding me. Mention me with @ in a message whenever you need help."}
    elif space_type == 'DM':
        user_display_name = event_data['user']['displayName']
        return {"text": f"Hi {user_display_name}! How can I help you?"}
    else:
        logging.warning("Unknown space type: %s", space_type)
        return {}

def handle_removed_from_space():
    """Handles the event when the bot is removed from a space."""
    logging.info("Bot removed from space")
    return {}

def handle_card_clicked(event_data):
    """Handles the event when a card is clicked."""
    # Process card click event here
    # Example: Generate and send an image, handle feedback, etc.
    return {"text": "Card clicked event processed"}


def process_message_event(event_data, feedback=False):
    """Processes message events from Google Chat."""

    incoming_message = event_data.get('message', {})
    user_text = 'Say thank you for my evaluation in German.' if feedback else incoming_message.get('argumentText', "")
    user_name = event_data['user']['name']
    user_id = user_name.split("/")[1]
    space_name = event_data['space']['name'].split("/")[1]
    space_type = event_data['space']['spaceType']
    today_date_string = datetime.now().strftime('%Y-%m-%d')

    # Generate a unique thread ID for direct messages
    thread_id = f"{user_id}-{space_name}-{today_date_string}" if space_type == "DIRECT_MESSAGE" else None

    logging.info(f"User text: {user_text}, Thread ID: {thread_id}")

    # Process the command based on commandId, if present
    command_id = incoming_message.get('slashCommand', {}).get('commandId')
    messages, result = [], None

    if command_id == "1":
        # Handle specific command (e.g., new request)
        result = generate(user_text, history=[])
        messages.append([user_text, result])
    elif command_id == "2":
        # Handle another specific command (e.g., feedback)
        return dialog_util.feedback_dialog()
    else:
        # Handle regular message event
        thread_obj = datastore_util.get_thread(thread_id) if thread_id else None
        history = thread_obj.get_messages()[0][1] if thread_obj else ""
        result = generate(user_text, history, user_id, thread_id)

    if thread_id:
        messages.append([user_text, result])
        datastore_util.store_messages(thread_id, messages)

    # Log the response
    logging.info(f"Chat response: {result}")

    return {"text": result}



