import os
import re
import ollama
import sys
from tavily import TavilyClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment variables from a .env file
load_dotenv()

# ---
# A simple class to handle conversation memory
# ---
class ConversationMemory:
    def __init__(self, memory_file="memory.txt"):
        self.memory_file = memory_file

    def load_memory(self):
        """Loads the conversation summary from the memory file."""
        try:
            with open(self.memory_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "" # Return empty string if no memory file exists yet

    def save_memory(self, conversation_summary: str):
        """Saves a new conversation summary."""
        print("\n💾 Saving conversation summary...")
        with open(self.memory_file, 'w') as f:
            f.write(conversation_summary)
        print("✅ Memory saved.")

# ---
# Environment and Status Checks
# ---
def check_environment():
    try:
        ollama.list()
    except Exception:
        print("❌ Ollama server is not running! Please start the Ollama application.")
        return False
    if "TAVILY_API_KEY" not in os.environ or not os.environ["TAVILY_API_KEY"]:
        print("❌ TAVILY_API_KEY not found in .env file!")
        return False
    return True

# ---
# The Agent's Toolbelt
# ---
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
def web_search(query: str) -> str:
    print(f"🔎 Searching the web for: '{query}'")
    try:
        results = tavily_client.search(query=query, search_depth="basic", max_results=3)
        return "\n".join([f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}" for r in results.get("results", [])])
    except Exception as e: return f"Error: {e}"

def read_web_page(url: str) -> str:
    print(f"📖 Reading content from URL: {url}")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        return "\n".join([p.get_text() for p in soup.find_all('p')])[:4000]
    except Exception as e: return f"Error: {e}"

# ---
# The Agent's Brain
# ---
def call_llm(prompt: str):
    try:
        response = ollama.chat(model='gemma', messages=[{'role': 'user', 'content': prompt}], options={'temperature': 0})
        return response['message']['content']
    except Exception as e: return f"Error calling Ollama: {e}"

# ---
# The Agent's "Operating System" (Prompt with Memory)
# ---
REACT_PROMPT_TEMPLATE = """
You are a helpful and conversational AI Research Assistant.

Here is a summary of our previous conversation:
<memory>
{memory}
</memory>

Your goal is to answer the user's current question. You can have a back-and-forth conversation.

You have access to the following tools:
- web_search(query: str): Search the web for relevant articles and URLs.
- read_web_page(url: str): Read the full content of a web page.

Research Strategy:
1. Use `web_search` to find promising web pages.
2. Use `read_web_page` to read the most relevant URL.
3. Analyze the content to answer the user's question.
4. If you need more information, you can read another URL or perform a new search.

To use a tool, you MUST use the following format:
Thought: [Your reasoning and plan.]
Action: [The tool to use, e.g., web_search("some query")]

When you have the final answer for the CURRENT question, use this format:
Thought: I have the final answer.
Final Answer: [Your comprehensive answer. Cite the URL(s) you used.]

Let's begin!

User's Current Question: {input}
{agent_scratchpad}
"""

# ---
# The Agent's Execution Loop
# ---
def run_agent(user_query: str, tools: dict, memory: str):
    agent_scratchpad = ""
    max_loops = 7
    for loop_count in range(max_loops):
        print(f"\n--- Agent Loop {loop_count + 1} ---")
        full_prompt = REACT_PROMPT_TEMPLATE.format(
            memory=memory,
            input=user_query,
            agent_scratchpad=agent_scratchpad
        )
        llm_response = call_llm(full_prompt)
        print(f"🤖 Agent's thought process:\n{llm_response}")

        if "Final Answer:" in llm_response:
            return llm_response.split("Final Answer:")[-1].strip()
        
        action_match = re.search(r"Action: (.*)", llm_response, re.DOTALL)
        if action_match:
            action_string = action_match.group(1).strip()
            tool_name = action_string.split('(')[0]
            if tool_name in tools:
                try:
                    tool_input_str = action_string.split('(', 1)[1][:-1]
                    tool_input = eval(tool_input_str, {"__builtins__": None}, {})
                    observation = tools[tool_name](tool_input)
                except Exception as e: observation = f"Error: {e}"
            else: observation = f"Error: Unknown tool '{tool_name}'."
            agent_scratchpad += f"{llm_response}\nObservation: {observation}\n"
        else:
            # If there's no action, it's a conversational turn. We just return the response.
            return llm_response
            
    return "Agent could not finish in the allowed number of steps."

# ---
# The Main Chat Application Loop
# ---
def main():
    if not check_environment():
        sys.exit(1)

    agent_tools = {"web_search": web_search, "read_web_page": read_web_page}
    memory_handler = ConversationMemory()
    
    # Keep track of the full conversation for summarization at the end
    conversation_history = []
    
    print("🤖 AI Research Assistant is online. Type 'quit' or 'exit' to end the session.")
    
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["quit", "exit"]:
            if conversation_history:
                # Join the history into a single string
                full_conversation = "\n".join(conversation_history)
                
                # Ask the LLM to summarize
                summary_prompt = f"Please summarize the key points of the following conversation in a few bullet points for my future reference:\n\n{full_conversation}"
                summary = call_llm(summary_prompt)
                
                # Save the summary
                memory_handler.save_memory(summary)
            
            print("🤖 It was great chatting with you. Goodbye!")
            break

        # Add user input to history
        conversation_history.append(f"You: {user_input}")

        # Load long-term memory for the current turn
        current_memory = memory_handler.load_memory()
        
        # Run the agent to get a response
        response = run_agent(user_input, agent_tools, current_memory)
        print(f"🤖 Assistant: {response}")

        # Add agent response to history
        conversation_history.append(f"Assistant: {response}")

if __name__ == "__main__":
    main()
