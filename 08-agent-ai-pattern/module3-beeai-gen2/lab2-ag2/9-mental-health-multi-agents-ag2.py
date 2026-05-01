# Import necessary modules
import os
from dotenv import load_dotenv
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function
from autogen.llm_config import LLMConfig
import json
import time
import random
import logging
from autogen import ConversableAgent
from typing import Annotated
from openai import OpenAI
from pydantic import BaseModel
import warnings

# Load environment variables
load_dotenv()

# Suppress autogen and other deprecation/user warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Suppress warnings from autogen.oai.client
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Initialize OpenAI Client (API Key is automatically managed from environment variables or configured in OpenAI settings)
client = OpenAI()

# Disable Docker execution to prevent runtime errors
code_execution_config = {"use_docker": False}

# LLM configuration (API key will be taken from environment variable)
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    ]
}

# Create AI Agents with distinct roles 
patient_agent = ConversableAgent(
    name="patient",
    system_message="You describe your emotions and mental health concerns.",
    llm_config=llm_config
)

emotion_analysis_agent = ConversableAgent(
    name="emotion_analysis",
    system_message="You analyze the user's emotions based on their input."
                   "Do not provide treatment or self-care advice."
                   "Instead, just summarize the dominant emotions they may be experiencing.",
    llm_config=llm_config
)

therapy_recommendation_agent = ConversableAgent(
    name="therapy_recommendation",
    system_message="You suggest relaxation techniques and self-care methods"
                   "only based on the analysis from the Emotion Analysis Agent."
                   "Do not analyze emotions—just give recommendations based on the prior response.",
    llm_config=llm_config
)

# Create GroupChat for AI Agents 
groupchat = GroupChat(
    agents=[emotion_analysis_agent, therapy_recommendation_agent],
    messages=[], 
    max_round=3,  # Ensures the conversation does not stop too early 
    speaker_selection_method="round_robin"
)

# Create GroupChatManager 
manager = GroupChatManager(name="manager", groupchat=groupchat)

# Function to start the chatbot interaction 
def start_mental_health_chat():
    """Runs a chatbot for mental health support with distinct agent roles.""" 
    print("\nWelcome to the AI Mental Health Chatbot!") 
    user_feelings = input("How are you feeling today?")

    # Initiate conversation
    print("\nAnalyzing emotions...")
    response = patient_agent.initiate_chat(
        manager, 
        message=f"I have been feeling {user_feelings}. Can you help?"
    )

    # Ensure the therapy agent gets triggered
    if not response:  # If the initial response is empty, retry with explicit therapy agent prompt
        response = therapy_recommendation_agent.initiate_chat(
            manager, 
            message="Based on the user's emotions, please provide therapy recommendations."
        )

# Run the chatbot 
start_mental_health_chat()