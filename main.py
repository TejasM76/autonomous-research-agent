import os
import re
import ollama
import sys
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables from a .env file
# This is the secure way to handle API keys.
load_dotenv()

# ---
# A couple of quick checks to make sure our environment is ready.
# ---

def check_environment():
    """Checks if the Ollama server and Tavily API key are ready."""
    try:
        ollama.list()
        print("✅ Ollama server is running.")
    except Exception:
        print("❌ Ollama server is not running! Please start the Ollama application.")
        return False

    if "TAVILY_API_KEY" not in os.environ or not os.environ["TAVILY_API_KEY"]:
        print("❌ TAVILY_API_KEY not found in .env file!")
        print("Please create a .env file and add your free API key from https://tavily.com.")
        return False
    
    print("✅ Tavily API key loaded successfully.")
    return True

# ---
# Let's define the tools our agent can use.
# ---

# Initialize the Tavily client. It will automatically use the API key from the environment.
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """A tool that performs a web search using the Tavily API."""
    print(f"🔎 Searching the web for: '{query}'")
    try:
        results = tavily_client.search(query=query, search_depth="basic", max_results=3)
        
        # Format the results into a clean string for the LLM to read.
        formatted_results = ""
        for res in results.get("results", []):
            formatted_results += f"Title: {res['title']}\nURL: {res['url']}\nSnippet: {res['content']}\n\n"
        return formatted_results
    except Exception as e:
        return f"Error during web search: {e}"

# ---
# This is the agent's "brain" - the function that calls our local LLM.
# ---

def call_llm(prompt: str):
    """A simple wrapper for calling the Ollama model."""
    try:
        response = ollama.chat(
            model='gemma',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0} # We want deterministic, predictable responses
        )
        return response['message']['content']
    except Exception as e:
        return f"Error calling Ollama: {e}"

# ---
# The prompt is the agent's "operating system". It's the most important part.
# ---

REACT_PROMPT_TEMPLATE = """
You are a diligent AI Research Assistant. Your goal is to answer the user's question by finding relevant, up-to-date information on the internet.

You have access to the following tool:
- web_search(query: str): Use this to search the web for information.

To use the tool, you MUST use the following format:
Thought: [Your reasoning. Analyze the user's question and decide on a search query.]
Action: web_search("your concise search query")

The tool will return an Observation with search results.
- If the Observation contains the answer, synthesize it and provide the final answer.
- If the Observation is not sufficient, you can perform another search.

When you have the final answer, you MUST use this format:
Thought: I have gathered enough information to answer the user's question.
Final Answer: [A comprehensive answer to the user's question based on the search results.]

Let's begin!

User's Question: {input}
{agent_scratchpad}
"""

# ---
# This is the main loop that runs the agent's thought process.
# ---

def run_agent(user_query: str, tools: dict):
    agent_scratchpad = ""
    max_loops = 5

    for loop_count in range(max_loops):
        print(f"\n--- LOOP {loop_count + 1} ---")

        # Create the full prompt for this loop.
        full_prompt = REACT_PROMPT_TEMPLATE.format(
            input=user_query,
            agent_scratchpad=agent_scratchpad
        )
        
        # Call the LLM to get its thought and action.
        llm_response = call_llm(full_prompt)
        print(f"🤖 LLM Response:\n{llm_response}")

        if "Final Answer:" in llm_response:
            final_answer = llm_response.split("Final Answer:")[-1].strip()
            print("\n🏁 AGENT FINISHED 🏁")
            return final_answer

        action_match = re.search(r"Action: (.*)", llm_response, re.DOTALL)
        if not action_match:
            print("--- ERROR: Could not parse action from LLM response. ---")
            return "Agent failed to produce a valid action."

        action_string = action_match.group(1).strip()
        tool_name = action_string.split('(')[0]
        
        if tool_name in tools:
            try:
                tool_input_str = action_string.split('(', 1)[1][:-1]
                tool_input = eval(tool_input_str, {"__builtins__": None}, {})
                
                print(f"🛠️ Calling Tool: `{tool_name}` with input: `{tool_input}`")
                observation = tools[tool_name](tool_input)
            except Exception as e:
                observation = f"Error parsing or executing tool: {e}"
        else:
            observation = f"Error: Unknown tool '{tool_name}'."
        
        print(f"📝 Observation:\n{observation}")
        agent_scratchpad += f"{llm_response}\nObservation: {observation}\n"

    return "Agent could not finish in the allowed number of steps."

# ---
# This is where we kick everything off.
# ---

if __name__ == "__main__":
    if not check_environment():
        sys.exit(1)

    agent_tools = {
        "web_search": web_search
    }
    
    query = "What is the Llama 3 model from Meta AI, and what are its key features?"
    
    final_result = run_agent(query, agent_tools)
    
    print("\n\n✅ Final Result ✅")
    print(final_result)
