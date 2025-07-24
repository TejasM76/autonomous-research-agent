# Conversational AI Research Assistant

This project is a powerful, autonomous AI agent built from scratch in Python. It's designed to function as an interactive research assistant, capable of having a continuous conversation, using tools to search the web and read pages, and remembering past interactions to provide context-aware responses.
it's a demonstration of a modern, agentic AI architecture that can reason, plan, remember, and interact with users and external tools to achieve complex goals.

### 🚀 Key Features

* **Conversational & Interactive**: Engage in a continuous, back-and-forth chat session with the agent, which maintains context throughout the conversation.
* **Long-Term Memory**: The agent summarizes each conversation and saves the key points, allowing it to "remember" past interactions for more personalized future sessions.
* **Autonomous Multi-Tool Use**: The agent intelligently decides when to use its tools, such as performing a `web_search` to find sources and then a `read_web_page` to analyze them in depth.
* **Open-Source at the Core**: Powered by a local, open-source LLM (**Google's Gemma**) running on the **Ollama** server, ensuring privacy and full control over the AI "brain".
* **Secure by Design**: API keys and secrets are managed securely using a **`.env`** file, following professional best practices.
* **Built from Scratch**: The core reasoning loop, memory system, and tool integration logic were built from the ground up, demonstrating a deep understanding of how these systems work.

### 🛠️ Technology Stack

* **LLM Server**: [Ollama](https://ollama.com/)
* **LLM Model**: [Gemma](https://huggingface.co/google/gemma-2b-it)
* **Web Search API**: [Tavily](https://tavily.com/)
* **Web Scraping**: [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
* **Core Language**: Python
* **Key Libraries**: [`ollama`](https://pypi.org/project/ollama/), [`tavily-python`](https://pypi.org/project/tavily-python/), [`python-dotenv`](https://pypi.org/project/python-dotenv/), [`requests`](https://pypi.org/project/requests/)

### ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```

2.  **Install Ollama:** Download and run the Ollama application from the [official website](https://ollama.com/).

3.  **Pull the LLM model:**
    ```bash
    ollama pull gemma
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up your API Key:**
    * Get a free API key from [Tavily.com](https://tavily.com/).
    * Create a file named **`.env`** in the root of the project directory.
    * Add your API key to the **`.env`** file:
        ```
        TAVILY_API_KEY="your-tavily-api-key"
        ```

### ▶️ How to Run

Once the setup is complete, run the main script from your terminal:

```bash
python main.py
```

The agent will start an interactive chat session. You can ask it research questions, and it will use its tools to find answers. Type `quit` or `exit` to end the session, at which point the agent will summarize and save the conversation.
