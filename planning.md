# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The tool will search the listings.json file looking to find items matching the users' description of a piece of clothing, while taking into consideration if a size and/or a price/budget limit is provided. It will filter through the listings with the given data and return the relevant matches in order of highest relevance.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): ... keywords from the user describing the article of clothing.
- `size` (str): ... string to store the size related to the article of clothing being described in order to filter any possible results in the listings, or if empty and unused if not provided.
- `max_price` (float): ... maximum price the user is willing to spend on the article of clothing, used to filter the listings for a result, or if empty and unused if not provided.

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
Will return a list of listing dicts that match the description provided by the user, sorted by relevance. Returns an empty list if nothing in the listings matches the user request.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
Returns an empty list if nothing in the listings matches the user request  — does NOT raise an exception. Will not proceed to call other functions. Instead will suggest the user to edit their filters of price and size, if provided. If no filters provided, suggest adding more descriptive keywords related to the article of clothing being searched and provide examples.
---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Returns a string with 1-2 outfit pairing suggestions to create an outfit based on the article of clothing provided and the wardrobe of the user.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): ... the article of clothing that resulted from the users' search in search_listinga(). Item to be paired with other items in the users' wardrobe.
- `wardrobe` (dict): ... dict with items in the users' wardrobe, possibly empty.

**What it returns:**
<!-- Describe the return value -->
Will return a non-empty string with the outfit suggestion generated (the items from the wardrobe are named along with the keywords describing the item). An empty wardrobe will cause the LLM to be prompted for general styling advice/ideas for the article of clothing.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
If the wardrobe is empty, the LLM will be prompted with general styling tips/ideas for items that may pair with the article of clothing. Returns suggestion.

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
Generates a caption based on the item to be purchased and one of the outfits.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): ... outfit suggestions generated from suggest_outfit().
- `new_item` (dict): ... the article of clothing that resulted from the users' search. Item to be paired with other items in the users' wardrobe.

**What it returns:**
<!-- Describe the return value -->
A string returned as a Caption between 2-4 sentences (inclusive) that may be used for a social media post. Caption should be informal, mentioning the new_item name, price, platform, and the general impression/vibe of the outfit. Captions should be unique from others generated and not recycled.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
If the outfit data is incomplete, return a string error message that the outfit data is not complete or missing and the card could not be generated - do NOT raise an exception.
---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
- Call _new_session() with string query and dict wardrobe
- Store extracted description/size/max_price in parsed
     - Have the LLM parse entered query to identify keywords pertaining to item description and any possible mention of a certain size or price limit.
- Call search_listings() with item description, size, and max_price.
     - If no results, return error message and end session - does NOT raise an exception..
          - Error message will suggest the user to edit their filters of price and size, if provided. If no filters provided, suggest adding more descriptive keywords related to the article of clothing being searched and provide examples .
     - Else, store top three results in search_results.
          - Will filter the listings with the keywords (size and/or price limit if provided too). Will attribute a value to each item from the filtered lists and will eliminate any listings with a score of 0. Sort the rest of the list and will store the three highest scored listings in ascending order.
- Store the first item in search_results as dict selected_item.
- Call suggest_outfit() with the selected_item and the user wardrobe dict
     - If wardrobe is empty, return generated styling suggestion
          -The LLM will be prompted with general styling tips/ideas for items that may pair with the article of clothing - does NOT raise an exception.
     - Else, generate a non-empty string with the outfit suggestion generated. 
          - The items from the wardrobe are named along with the keywords describing the item.
- Store results in string outfit_suggestion
- Call create_fit_card() with outfit_suggestion and selected_item
     - If outfit data is incomplete, return a string error message
          - Error message states that the outfit data is not complete or missing and the card could not be generated - does NOT raise an exception.
     - Else, generate a string caption between 2-4 sentences (inclusive) long that may be used for a social media post.      
          - Caption should be informal, mentioning the new_item name, price, platform, and the general impression/vibe of the outfit. Captions should be unique from others generated and not recycled.
- Store result in fit_card
- Return the session
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

Session is initialized with the users intial query and the wardrobe dict. The query is then parsed by the LLM with keywords of the description/size/max_price stored in parsed. Parsed is passed to search_listings as description/size/max_price. The
relevant listings are stored in search_results with the most relevant result stored in dict selected_item. Suggest_outfit() is called with selected_item and wardrobe to generate and store string outfit_suggestion. Create_fit_card() is called with selected_item and outfit_suggestion to generate and stored in string fit_card. Any errors from the session are stored in error. Session is returned.
---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Returns an empty list if nothing in the listings matches the user request  — does NOT raise an exception. Will not proceed to call other functions. Instead will suggest the user to edit their filters of price and size, if provided. If no filters provided, suggest adding more descriptive keywords related to the article of clothing being searched and provide examples. |
| suggest_outfit | Wardrobe is empty | The LLM will be prompted with general styling tips/ideas for items that may pair with the article of clothing. Returns string suggestion.|
| create_fit_card | Outfit input is missing or incomplete | return a string error message that the outfit data is not complete or missing and the card could not be generated - do NOT raise an exception. |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕```
User query
    │
    ▼
Planning Loop (run_agent) ──────────────────────────────────────────────────────────────────────────┐
    │                                                                         					│
    ├─► _new_session(query, wardrobe)                                            				│
    │       │                                                                    				│
    │       ▼                                                                    				│
    │   LLM parses query → session: parsed = {description, size, max_price}     				│
    │       │                                                                    				│	
    │       ▼                                                                    				│
    │   search_listings(description, size, max_price)                            				│
    │       │                                                                    				│
    │       ├─► results == []                                                    				│
    │       │       │                                                            				│	
    │       │       └─► [ERROR] "No listings found. Try adjusting your           				│
    │       │                    price/size filters or use different keywords."   				│
    │       │                        └─► Return session ───────────────────────────────────────────►│
    │       │                                                                    				│
    │       │ results != []                                                      				│
    │       ▼                                                                    				│
    │   session: search_results = top 3 relevant matches                         				│
    │   session: selected_item = results[0]                                      				│
    │       │                                                                    				│
    │       ▼                                                                    				│
    │   suggest_outfit(selected_item, wardrobe)                                  				│
    │       │                                                                    				│
    │       ├─► wardrobe: items == []                                            				│
    │       │       │                                                            				│
    │       │       └─► return general styling advice                            				│
    │       │                                                                    				│
    │       │ wardrobe: items != []                                              				│
    │       └─► return string with selected item and outfit pairings             				│
    │       │                                                                    				│
    │       ▼                                                                    				│
    │   session: outfit_suggestion = outfit string from suggest_outfit()         				│
    │       │                                                                    				│
    │       ▼                                                                    				│
    │   create_fit_card(outfit_suggestion, selected_item)                        				│
    │       │                                                                    				│
    │       ├─► outfit_suggestion == ""                                          				│
    │       │       │                                                            				│
    │       │       └─► [ERROR] "Outfit data is not complete or missing,         				│	
    │       │                    card could not be generated."                   				│
    │       │                        └─► Return session ───────────────────────────────────────────►│
    │       │                                                                    				│
    │       └─► return 2-4 sentence caption                                      				│
    │       │                                                                    				│
    │       ▼                                                                    				│
    │   session: fit_card = caption string from create_fit_card()                				│
    │       │                                                                  					└───────── error path returns here
    │       ▼                                                                    				
    └─► Return session                           														
```
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
Tool 1: search_listings()
     - Will give claude the tool 1 specs with the four fields filled out (What it does, Input parameters, What it returns, What happens if it fails or returns nothing) and ask it to implement it into the tools.py file. Ensure to utilize load_listings() from utils/data_loader.py.
     - Review generated function before running.
     - Expect it to produce session search_results with the list of matching listing dicts and the session selected_item which is the top relevent result.
     - Verify with queries with varying information in the description, price, and size to ensure it works with the minimal and maximal information that can be provided.
Tool 2: suggest_outfit()
     - Will give claude the tool 2 specs with the four fields filled out (What it does, Input parameters, What it returns, What happens if it fails or returns nothing) and ask it to implement it into the tools.py file. 
     - Review generated function before running.
     - Expect it to produce the string outfit_suggestion with the 1-2 outfit suggestions to pair with the selected_item.
     - Verify with queries that test and ensure it won't crash if wardrobe['items'] is empty. Verify that general styling suggestions are provided wardrobe is empty. Verify that output is a non-empty string and that specific items from the wardrobe are listed. 
Tool 3: create_fit_card()
     - Will give claude the tool 3 specs with the four fields filled out (What it does, Input parameters, What it returns, What happens if it fails or returns nothing) and ask it to implement it into the tools.py file. 
     - Review generated function before running.
     - Expect it to produce the string fit_card which has the caption post about the outfit which includes the item, wardrobe pairing, vibe of outfit, and platform name.
     - Check stub signature for parameters passed for create_fit_card()
     - Verify with queries that the correct error message appears when outfit is empty. Verify outputs vary, if not then raise LLM temperature. Verify the fit_card includes the item, wardrobe pairing, vibe of outfit, and platform name.

**Milestone 4 — Planning loop and state management:**
- Will provide Claude with the agent diagram, the planning loop and state management portions of the planning.md document. 
- Expect it to produce a new session with _new_session(), have the LLM parse the query, call search_listings() to produce the search_results dict and the selected_item, call suggest_outfit() to produce the outfit_suggestion, call create_fit_card() to produce the fit_card, return the session. Will produce an error message if ever required.
- Verify it matches the specs given by ensuring the tools are called when needed and return/end the session if an error occurs (e.g. if the search_listings dict is empty, then the suggest_outfit() and create_fit_card() tools are NOT called).
---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
- Initialize session with query and wardrobe
- Agent calls LLM to parse the qeury to find the description/price/size. 
     - This example would be
          - description: "vintage graphic tee"
          - size: None
          - max_price: 30.0

- Calls search_listings() with the parsed parameters. 

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
- If step 1 returned with an empty search_results list, return error message prompting user to try something different.
- Else, selected_item(the top item from search_results) and wardrobe are passed to suggest_outfit(). 
     - This example
          - selected_item: "Graphic Tee — 2003 Tour Bootleg Style"
- If wardrobe is empty, LLM is prompted for general styling suggestions.
- Else, ask LLM to suggest specific outfit combinations with the selected_item and named wardrobe items. 
     - This example
          - selected_item: "Graphic Tee — 2003 Tour Bootleg Style"
          - outfit: "Graphic Tee — 2003 Tour Bootleg Style pairs well with Vintage black denim jacket and Baggy Carpenter Jeans — Dark Wash "

**Step 3:**
<!-- Continue until the full interaction is complete -->
- The generated outfit string and the selected_item dict are passed to create_fit_card() where a 2-4 sentence caption is generated about the clothing item and the outfit.
     -This example:
          - fit_card: "Found this $24 trendy Graphic Tee — 2003 Tour Bootleg Style that pairs well with Vintage black denim jacket and Baggy Carpenter Jeans — Dark Wash. Thankful for <platform-name>!"
- If the outfit is empty, generates error message
     - This example:
          -"ERROR: Outfit data is missing or empty."

**Final output to user:**
<!-- What does the user actually see at the end? -->
- the selected item of clothing from listing
- the outfit suggestion of the selected item and user wardrobe item(s)
- the fit card caption

**Description of what FitFindr needs to do:**
FitFindr, an AI agent, needs to take an request from the user that includes a description and/or price point/limit and/or size. It then needs to search the listings to find three matching listings by sorted relevance while returning the top result, return an outfit suggestion with the top result and something from the existing wardrobe, then return a fit card involving the new item and paired wardrobe item(s). If an error occurs, FitFindr cannot return an empty input but instead suggests a user to try something different.
