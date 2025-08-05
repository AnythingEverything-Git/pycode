
def extract_architecture_prompt(chunk_text):
    prompt = f"""
    You are a senior software architect.
    Analyze the following business requirement chunk and extract architecture details for High-Level Design (HLD).
    Return **ONLY a valid JSON object** following this strict schema:

    {{
      "actors": [
        {{
          "name": "string - actor name",
          "type": "External | Internal | External System"
        }}
      ],
      "microservices": [
        {{
          "name": "string - service name",
          "db": "string - database name or null if no db",
          "exposes": ["REST | gRPC | GraphQL | WebSocket | Event"],
          "consumes": ["REST | Queue | Event | DB"],
          "scaling": "string - e.g., AutoScale, Fixed, OnDemand",
          "criticality": "High | Medium | Low"
        }}
      ],
      "databases": [
        {{
          "name": "string - database name",
          "type": "SQL | NoSQL | InMemory",
          "used_by": ["list of microservice names"]
        }}
      ],
      "events": [
        {{
          "from": "string - source service or actor",
          "to": "string - destination service or actor",
          "type": "REST | Queue | Event | DB",
          "description": "string - purpose of this interaction"
        }}
      ]
    }}

    Rules:
    - JSON must be syntactically valid. Double-check for missing commas, brackets, or quotes.
    - Use double quotes for all JSON keys and values.
    - Include all services, DBs, and interactions inferred from the chunk.
    - If an element is not applicable, use null or an empty list.
    - No markdown, no explanations, no extra text outside JSON.

    Business Requirement Chunk:
    {chunk_text}
    """
    return prompt
