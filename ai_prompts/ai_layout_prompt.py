import json


def get_ai_layout_prompt(input_json):
    prompt = f"""
                You are a senior software architect and C4 diagram expert.

                I will provide a merged system architecture JSON containing:
                - "actors": external users or systems
                - "microservices": internal services (with optional DBs)
                - "databases": database components
                - "events": interactions between actors, services, and databases

                Here is the architecture JSON:
                {json.dumps(input_json, indent=2)}

                Your task:
                Generate a **production-ready HLD JSON** for a C4-style Container Diagram, reflecting a professional microservices architecture with inter-service interactions like this reference pattern:

                    End User -> API Gateway -> Microservices Layer -> External Systems
                    Microservices communicate with each other using REST, gRPC, Events (Kafka/RabbitMQ)
                    Databases align below their respective services
                    Analytics/Logging services are optional downstream services

                The output JSON must have this structure:

                {{
              "nodes": [
                {{
                  "name": "string - node name (actor/service/db/external)",
                  "type": "actor | gateway | service | db | external",
                  "layer": "frontend | gateway | microservice | data | external",
                  "x": int,
                  "y": int,
                  "color": "lightgreen | lightblue | lightyellow | lightgray"
                }}
              ],
              "edges": [
                {{
                  "from": "string - source node name",
                  "to": "string - target node name",
                  "label": "REST API | gRPC Call | Message Queue | DB Query | Event Stream",
                  "direction": "uni | bi",
                  "criticality": "High | Medium | Low"
                }}
              ],
              "microservice_interactions": [
                {{
                  "caller": "string - microservice name",
                  "callee": "string - microservice name",
                  "protocol": "REST | gRPC | Event",
                  "sync": true,
                  "purpose": "string - short description"
                }}
              ]
            }}

                Layout & Styling Rules:
                1. Place **End Users** (actors) at the top (y=0)
                2. Place **API Gateway or BFF services** in the second row (y=-1)
                3. Place **microservices layer** in the middle (y=-2)
                4. Place **databases** below their microservices (y=-3)
                5. Place **external systems** at the bottom (y=-4)
                6. Maintain horizontal spacing of 2 units between nodes in each layer
                7. Use these colors:
                   - Actors → lightgreen
                   - Gateways → lightskyblue
                   - Internal services → lightblue
                   - Databases → lightyellow
                   - External systems → lightgray
                8. Interactions:
                   - REST → blue solid arrow
                   - gRPC → cyan solid arrow
                   - Async Event/Queue → green dashed arrow
                   - DB Query → brown dashed arrow
                9. Explicitly include **microservice-to-microservice interactions** in `edges` and `microservice_interactions`
                10. Ensure JSON is **valid**, no nulls, no trailing commas, properly closed braces/brackets
                11. Output **only valid JSON**, no commentary or markdown
                """
    return prompt
