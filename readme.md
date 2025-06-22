Verifies Ollama server + model

Asks the user to enter a URL

Extracts and prints the clean article + list items

Waits for Enter key to continue

Sends content to LLM and prints response

Library	        Use
goose3	        Extracts clean main article text
beautifulsoup4	Finds and extracts list items from HTML
requests	Talks to Ollama server API


It will:

Extract the full article text + any bullet points

Display it to you

Then ask the LLM:

“Summarize and extract key insights from the following article…”
