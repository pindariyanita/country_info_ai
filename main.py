from agent import build_graph

if __name__ == "__main__":
    app = build_graph()

    query = input("Ask a country question: ")

    result = app.invoke({
        "query": query,
        "country": None,
        "fields": None,
        "api_response": None,
        "final_answer": None,
        "error": None
    })

    print("\nAnswer:", result["final_answer"])