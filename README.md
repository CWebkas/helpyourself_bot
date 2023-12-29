# Google Chatbot Integration

## Overview
This repository contains code for a Google Chatbot integration, designed to interact with users in Google Chat spaces. It includes handling events such as adding the bot to a space, removing it, processing messages, and responding to card clicks. The bot is built using Python and integrates with various services like OpenAI's GPT, Google Cloud Secret Manager, and BigQuery.

![image](https://github.com/CWebkas/helpyourself_bot/assets/30929659/de904107-0486-4ab3-a5c0-9dc66b857eb4)


## Features
- **Event Handling**: Manages various Google Chat events (`ADDED_TO_SPACE`, `REMOVED_FROM_SPACE`, `MESSAGE`, `CARD_CLICKED`).
- **Message Processing**: Processes incoming messages and commands, providing responses based on the context.
- **Slash Command Support**: Custom commands for specific interactions.
- **Chat History Management**: Stores and retrieves conversation history for personalized interactions.
- **Integration with AI Services**: Utilizes OpenAI's GPT for generating dynamic responses.

## Prerequisites
- Python 3.8 or higher
- Access to Google Cloud Platform services
- An OpenAI API key for GPT integration
