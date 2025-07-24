# AI Research Assistant Agent

This project is a powerful, autonomous AI agent built from scratch using open-source models and libraries. It's designed to perform initial research on any given topic by searching the web, analyzing the results, and synthesizing a comprehensive answer.
it's a demonstration of a modern, agentic AI architecture that can reason, plan, and use tools to achieve complex goals.

### 🚀 Key Features

* **Autonomous Reasoning**: The agent uses the **ReAct (Reason + Act)** framework to break down complex questions, formulate plans, and execute them step-by-step.
* **Live Web Search**: Connected to the live internet via the **Tavily API**, allowing it to access up-to-the-minute information.
* **Open-Source at the Core**: Powered by a local, open-source LLM (**Google's Gemma**) running on the **Ollama** server. This ensures privacy and full control over the AI "brain".
* **Secure by Design**: API keys and secrets are managed securely using a **`.env`** file, following best practices for application development.
* **Built from Scratch**: The core reasoning loop and tool integration logic were built from the ground up in Python, demonstrating a deep understanding of how these systems work without relying on high-level frameworks.

### 🛠️ Technology Stack

* **LLM Server**: [Ollama](https://ollama.com/)
* **LLM Model**: [Gemma](https://huggingface.co/google/gemma-2b-it) (or any other model supported by Ollama)
* **Web Search API**: [Tavily](https://tavily.com/)
* **Core Language**: Python
* **Key Libraries**: [`ollama`](https://pypi.org/project/ollama/), [`tavily-python`](https://pypi.org/project/tavily-python/), [`python-dotenv`](https://pypi.org/project/python-dotenv/)

### ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```

2.  **Install Ollama:** Download and run the Ollama application from the [official website](https://ollama.com/).

3.  **Pull the LLM model:** Open your terminal and pull the Gemma model.
    ```bash
    ollama pull gemma
    ```

4.  **Install Python dependencies:** Install all required libraries from the **`requirements.txt`** file.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up your API Key:**
    * Get a free API key from [Tavily.com](https://tavily.com/).
    * Create a file named **`.env`** in the root of the project directory.
    * Add your API key to the **`.env`** file like this:
        ```
        TAVILY_API_KEY="your-tavily-api-key"
        ```

### ▶️ How to Run

Once the setup is complete, simply run the **`main.py`** script from your terminal:

```bash
python main.py
```

The agent will start, check your environment, and then begin answering the research question defined in the script. You can watch its reasoning process in real-time in the console output!
