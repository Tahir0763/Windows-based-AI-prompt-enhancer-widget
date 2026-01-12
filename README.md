# Windows-based AI Prompt Enhancer Widget

## Overview
This is a Windows-based widget designed to enhance AI prompts using various AI models. It provides a convenient overlay interface for quick interactions.

## Features
- **AI-Powered Prompt Enhancement**: utilizes AI models to refine and improve prompts.
- **Overlay Widget**: A floating widget for easy access.
- **Clipboard Integration**: Seamlessly works with your clipboard content.
- **Model Selection**: Choose between different AI models (e.g., Gemini, OpenRouter).

## Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the main script to start the application:
```bash
python main.py
```

## Structure
- `main.py`: Entry point of the application.
- `ai_handler.py`: Handles interactions with AI APIs.
- `overlay.py`: Manages the GUI overlay.
- `key_eavesdropper.py`: Listens for keyboard shortcuts/events.
