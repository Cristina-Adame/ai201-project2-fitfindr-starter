# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.

---
## Tools

Tools the agent uses.

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

## Planning Loop

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

Session is initialized with the users intial query and the wardrobe dict. The query is then parsed by the LLM with keywords of the description/size/max_price stored in parsed. Parsed is passed to search_listings as description/size/max_price. The
relevant listings are stored in search_results with the most relevant result stored in dict selected_item. Suggest_outfit() is called with selected_item and wardrobe to generate and store string outfit_suggestion. Create_fit_card() is called with selected_item and outfit_suggestion to generate and stored in string fit_card. Any errors from the session are stored in error. Session is returned.
---


## Error Handling

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Returns an empty list if nothing in the listings matches the user request  — does NOT raise an exception. Will not proceed to call other functions. Instead will suggest the user to edit their filters of price and size, if provided. If no filters provided, suggest adding more descriptive keywords related to the article of clothing being searched and provide examples. |
| suggest_outfit | Wardrobe is empty | The LLM will be prompted with general styling tips/ideas for items that may pair with the article of clothing. Returns string suggestion.|
| create_fit_card | Outfit input is missing or incomplete | return a string error message that the outfit data is not complete or missing and the card could not be generated - do NOT raise an exception. |

**Sample Error Message:**
```text
Example: running search_listings("designer ballgown", size="XXS", max_price=5) 
returned [] without raising an exception. The agent responded with: 
"No listings found. Try adjusting your size (XXS) and price limit ($5.0) filters, 
or use different keywords."
```
---


## Spec Reflection
---


## AI Usage Section
