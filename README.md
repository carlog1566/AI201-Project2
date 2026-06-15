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

## Tool Inventory

### Tool 1: search_listings

Purpose: 
- Finds clothing listings that match a user's query based on description, size and budget

Inputs:
- description (str): Item description (e.g. "vintage graphic tee")
- size (str | None): Clothing size filter (e.g. "M", "L", "S")
- max_price (float | None): Maximum budget constraint

Outputs:
- list[dict] of matching listings sorted by relevance
- Each listing includes: id (str), title (str), description (str), category (str), style_tags (str), size (str), price (float), brand (str), platform (str)
- Returns [] if no matches exist

### Tool 2: suggest_outfit

Purpose: 
- Generates outfit recommendations by combining a selected listing with items from the user's wardrobe.

Inputs:
- new_item (dict): Selected listing from search_listings
- wardrobe (dict): User wardrobe (from get_example_wardrobe() or get_empty_wardrobe())

Outputs:
- str: Natural language outfit styling suggestion
- If wardrobe is empty, returns general styling advice without wardrobe references

### Tool 3: create_fit_card

Purpose:
- Generates a short social media caption based on the outfit and selected item.

Inputs:
- outfit (str): Output of suggest_outfit
- item (dict): Selected listing

Outputs:
- str: Caption styled like Instagram/TikTok post text
- If outfit is missing, generates fallback caption using listing only.

## Planning Loop

### Step 1: User Input

- The system receives a natrual language query:

    Example: "vintage graphic tee under $30 size M"
- This input is passed into the planning loop as the starting state

### Step 2: Planning Loop Initialization

- A session dictionary is created to track all intermediate states such as original query, parsed parameters, tool outputs, and error state
- This ensures all tool outputs are stored and accessible throughout execution

### Step 3: Search Listings

- The agent calls

```python
search_listings(query, size, budget)
```
- This is the first tool execution step and determines whether the pipeline continues
- If results is empty, it will return an error like "No listings found. Try another search.", stop execution, and does not call any further tools
- If results is not empty, we continue the pipeline

### Step 4: Select Item

- If results is not empty, we store the first item from the results array in the session
```python
selected_item = results[0]
session["selected_item"] = selected_item
```

### Step 5: Suggest Outfit

- The agent calls:
```python
suggest_outfit(selected_item, wardrobe)
```
- If wardrobe is empty, it will return general styling advice with no reference to the wardrobe
- Else, it will generate an outfit recommendation using the selected item and the wardrobe items
- The result is then stored into the session
```python
session["outfit_suggestion"]
```

### Step 6: Create Fit Card

- The agent calls
```python
create_fit_card(outfit_suggestion, selected_item)
```
- If outfit_suggestion is missing or empty, it will generate a fallback caption using only the listed info
- Else, it will generate a full styled caption
- The result is then stored into the session
```python
session["fit_card"]
```

### Step 7: Final Output
- The session is returned as the final result:
- selected_item
- outfit suggestion
- fit_card
- error (if any)

## State Management
The agent uses a session dictionary to store information throughout a single interaction

The session tracks:
- The original query
- Parsed query parameters
- Search results
- The selected listing
- The user's wardrobe
- The outfit suggestion
- The generated fit card
- Any error messages

Information is passed between tools through this session dictionary:
- After search_listings(), the top result is stored as selected_tiem
- selected_item and wardrobe are passed into suggest_outfit()
- The returned outfit suggestion is stored as outfit_suggestion
- outfit_suggestion and selected_item are passed into create_fit_card()
- The resulting caption is stored as fit_card

## Error Handling

### Tool 1: search_listings
- Fails when there are no matching results

Test Case:
```python
"designer ballgown size XXS under $5
```
Observed Behavior:
- Returns []
- Agent stops immediately

Response:
- "No matching lisstings found. Try adjusting your size, budget, or search terms."

### Tool 2: suggest_outfit

- Fails when the wardrobe is empty

Test Case:
```python
get_empty_wardrobe()
```
Observed Behavior:
- Returns general styling advice for the selected listing
- No crash or exception

Example Output:
- "This piece works well with neutral basics and layered accessories for balance."

### Tool 3: create_fit_card
- Fails when it is missing the outfit string

Test Case:
```python
create_fit_card("", selected_item)
```
Observed Behavior:
- Returns fallback caption instead of crashing

Example Output:
- "Thrifted gem: vintage find at an unbeatable price"

## Spec Reflection 
One way the spec helped was by having the planning loop and error handling be designed before it was implemented in code. This made it easier to build and test each tool independently before connecting them together

One way that implementation diverged from the original spec was in the query parsing. The spec didn't prescribe how to extract the description, size, and budget so during implementation, regex parsing was used since it was easier to test and more deterministic.

## AI Usage

### Instance 1: Planning Loop Implementation
I provided ChatGPT with my planning loop, state management, and architecture diagram and asked it to help generate code for the agent logic. The generated output included the complete code for the planning loop and session structure. However, before using it I reviewed the code and modified it to ensure that:

- the workflow stopped when no listings were found,
- the selected item was stored in the session state before being passed to later tools, and
- the tools were not called for no reason.

### Instance 2: Gradio Integration
I provided ChatGPT with the isntructions from app.py and asked it to help implement handle_query(). The genereated output correctly selected the wardrobes and called the agent, but I revised the implementation to:

- add validation for empty user queries,
- ensure error messages appeared only in the listing output panel, and
- safely access session values when formatting the listing text.

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
