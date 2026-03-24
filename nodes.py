import re

def extract_intent(state):
    query = state["query"].lower()

    country = None

    # Pattern 1: "of Germany"
    match = re.search(r"of ([a-zA-Z ]+)", query)
    if match:
        country = match.group(1)

    # Pattern 2: "does Japan use"
    if not country:
        match = re.search(r"does ([a-zA-Z ]+) use", query)
        if match:
            country = match.group(1)

    # Pattern 3: "currency japan is"
    if not country:
        match = re.search(r"currency ([a-zA-Z ]+) is", query)
        if match:
            country = match.group(1)

    # Pattern 4: generic fallback → pick known country-like word
    if not country:
        words = query.replace("?", "").split()
        
        # remove common words
        stopwords = {"what", "which", "is", "the", "does", "use", "using", "currency", "population", "capital"}
        candidates = [w for w in words if w not in stopwords]

        if candidates:
            country = candidates[-1]  # last meaningful word

    if country:
        country = country.strip(" ?.")

    # Field extraction
    fields = []
    if "capital" in query:
        fields.append("capital")
    if "population" in query:
        fields.append("population")
    if "currency" in query:
        fields.append("currencies")

    if not country:
        return {**state, "error": "Could not identify country"}

    return {**state, "country": country, "fields": fields}

from tools import fetch_country_data

def call_api(state):
    if state.get("error"):
        return state

    result = fetch_country_data(state["country"])

    if "error" in result:
        return {**state, "error": result["error"]}

    return {**state, "api_response": result}

def synthesize_answer(state):
    if state.get("error"):
        return {**state, "final_answer": state["error"]}

    data = state["api_response"]
    fields = state["fields"]

    answers = []

    for field in fields:
        if field == "capital":
            answers.append(f"Capital: {data.get('capital', ['N/A'])[0]}")
        elif field == "population":
            answers.append(f"Population: {data.get('population', 'N/A')}")
        elif field == "currencies":
            currencies = data.get("currencies", {})
            currency_names = [v["name"] for v in currencies.values()]
            answers.append(f"Currency: {', '.join(currency_names)}")

    if not answers:
        return {**state, "final_answer": "No valid fields requested."}

    return {**state, "final_answer": " | ".join(answers)}