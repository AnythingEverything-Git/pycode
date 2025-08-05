import json

def ask_ai_for_design_doc(input_json: dict):
    prompt = f"""
    You are an highly experienced enterprise software architect and technical writer. You have vast knowledge on HLD patterns.

    I will give you a JSON describing a system with:
    - actors (users or external systems)
    - services (microservices or internal components)
    - interactions (connections between actors, services, and databases)

    Generate a **professional System Design Document** in **Markdown** with the following sections:

    # System Design Document

    1. **System Overview**
       - One paragraph summary of the system based on the JSON

    2. **High-Level Architecture**
       - List all actors, services, and databases with brief descriptions
       - Provide a bullet list of interactions
       - Provide detailed information about interactions
       - Explain the High-Level Architecture

    3. **Component Responsibilities**
       - Present a table with: Component | Type | Responsibility

    4. **Data Flow & Security Considerations**
       - Stepwise detailed description of data flow
       - Security, authentication, and scaling considerations

    5. **Future Enhancements**
       - Suggest 2-3 improvements for scalability, maintainability, or monitoring

    **Output Rules:**
    - Respond in **Markdown only**
    - Be **concise but professional**
    - No commentary outside the document
    - **Do not start with any sentences like "Here is..." or "The document is..."**

    Here is the system JSON:

    {json.dumps(input_json, indent=2)}
    """
    return prompt