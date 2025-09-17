# random-mcp-server

This MCP server gives LLM the tools to use random number generators. Here are the available tools:
```
  • random_random_int: Generate random integer between min and max (inclusive)
  • random_random_float: Generate random float between min and max
  • random_random_choice: Pick random item(s) from a list
```
Here are some example use cases
```
💬 You: choose three random items from [a,b,c,d,e,f,g,h]
🤔 Assistant: 🔧 Executing random_random_choice...
The three random items are: **f, d, c**.

💬 You: throw a dice and give me the result
🤔 Assistant: 🔧 Executing random_random_int...
You rolled a **4**!

💬 You: give me a random probability
🤔 Assistant: 🔧 Executing random_random_float...
Here’s a random probability: **0.8593**
```
To use this, clone this repository, then add the dependencies, it is recommended to use `uv`. Then, you can use Anthropic's SDK with the following configuration:
```json
{
    command: "uv",
    args: ["run", "--directory", "/PATH/TO/REPO",
        "/PATH/TO/REPO/mcp_http_bridge.py",
        "https://random-number-mcp-server.manuelalejandromartinezf.workers.dev"]
}
```