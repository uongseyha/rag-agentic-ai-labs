# Import necessary modules
import os
from dotenv import load_dotenv
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.llm_config import LLMConfig
import json
import time
import random
import logging
from autogen import ConversableAgent

# Suppress API key format warning
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

# print("AG2 modules imported successfully!")

# # Create a configuration file for your API keys
# # Replace with your actual API key
# config_list = [
#     {
#         "model": "gpt-4o-mini",
#         "api_key": os.getenv("OPENAI_API_KEY")
#     }
# ]

# # Alternatively, you can create a JSON file
# '''
# with open('config.json', 'w') as f:
#    json.dump(config_list, f)
    
# Then load it
# config_list = config_list_from_json("config.json")
# '''

# LLM configuration (API key will be taken from environment variable)
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    ]
}

# Student agent
student = ConversableAgent(
    name="student",
    system_message="You are a curious student. You ask clear, specific questions to learn new concepts.",
    human_input_mode="NEVER",
    llm_config=llm_config
)

# Tutor agent
tutor = ConversableAgent(
    name="tutor",
    system_message="You are a helpful tutor who provides clear and concise explanations suitable for a beginner.",
    human_input_mode="NEVER",
    llm_config=llm_config
)

# Start conversation
chat_result = student.initiate_chat(
    recipient=tutor,
    message="Can you explain what a neural network is?",
    max_turns=2,
    summary_method="reflection_with_llm"
)

print("\nFinal Summary:")
print(chat_result.summary)