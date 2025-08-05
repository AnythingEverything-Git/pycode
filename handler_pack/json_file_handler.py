import json
import re

from ai_prompts import extract_architecture_ai_prompt
from ai_uitls.ai_repsonse_utility import ai_response


def fix_ai_json(raw_output: str):
    """
    Cleans and repairs AI JSON output to handle:
    1. Missing {} or []
    2. Missing last closing bracket/brace
    3. Single → double quote conversion (safe)
    4. Trailing commas
    """
    if not raw_output:
        return None

    # 1️⃣ Extract first JSON block: { ... } or [ ... ]
    match = re.search(r'(\{.*|\[.*)', raw_output, re.DOTALL)
    json_str = match.group(0).strip() if match else raw_output.strip()

    # 2️⃣ Remove trailing commas before } or ]
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

    # 3️⃣ Safely convert Python-like dict to JSON
    # Convert only keys/values in single quotes to double quotes without touching already double-quoted strings
    def safe_quote_replace(match):
        return '"' + match.group(1) + '"'

    # Replace single-quoted keys
    json_str = re.sub(r"(?<!\")'([A-Za-z0-9_ ]+)'(?=\s*:)", safe_quote_replace, json_str)
    # Replace single-quoted string values
    json_str = re.sub(r":\s*'([^']*)'", lambda m: ':"{}"'.format(m.group(1)), json_str)

    # 4️⃣ Auto-complete missing closing braces/brackets
    open_curly = json_str.count("{")
    close_curly = json_str.count("}")
    if close_curly < open_curly:
        json_str += "}" * (open_curly - close_curly)

    open_square = json_str.count("[")
    close_square = json_str.count("]")
    if close_square < open_square:
        json_str += "]" * (open_square - close_square)

    # 5️⃣ Attempt JSON parsing
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def extract_architecture_from_chunk(chunk_text):
    prompt = extract_architecture_ai_prompt.extract_architecture_prompt(chunk_text)

    response = ai_response(prompt, "You are a helpful assistant that outputs JSON only.")

    raw_output = response.choices[0].message.content.strip()
    data_parsed = fix_ai_json(raw_output)
    if not data_parsed:
        print("⚠️ JSON parse error, skipping chunk...")
    return data_parsed

def create_json_file_from_brd(chunks):
    global actor, svc, inter, architecture
    all_actors = {}  # key: actor name, value: actor dict
    all_services = {}  # key: service name, value: full service dict
    all_databases = {}  # key: db name, value: db dict
    all_events = set()  # tuple (from, to, type, description)
    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk {idx + 1}/{len(chunks)} ...")
        data = extract_architecture_from_chunk(chunk)  # AI JSON output

        # ---------------- Actors ----------------
        for actor in data.get("actors", []):
            if isinstance(actor, dict):
                name = actor.get("name", str(actor))
                actor_type = actor.get("type", "External")
            else:
                name = str(actor)
                actor_type = "External"
            all_actors[name] = {"name": name, "type": actor_type}

        # ---------------- Microservices ----------------
        for svc in data.get("microservices", data.get("services", [])):
            name = svc.get("name")
            if not name:
                continue
            # Merge or create service entry
            if name not in all_services:
                all_services[name] = {
                    "name": name,
                    "db": svc.get("db"),
                    "exposes": svc.get("exposes", []),
                    "consumes": svc.get("consumes", []),
                    "scaling": svc.get("scaling", "Unknown"),
                    "criticality": svc.get("criticality", "Medium")
                }

            # Register DB in all_databases if exists
            db_name = svc.get("db")
            if db_name:
                if db_name not in all_databases:
                    all_databases[db_name] = {
                        "name": db_name,
                        "type": "Unknown",
                        "used_by": [name]
                    }
                else:
                    if name not in all_databases[db_name]["used_by"]:
                        all_databases[db_name]["used_by"].append(name)

        # ---------------- Events / Interactions ----------------
        for inter in data.get("events", data.get("interactions", [])):
            src = inter.get("from")
            dst = inter.get("to")
            typ = inter.get("type", "Unknown")
            desc = inter.get("description", "")
            if src and dst:
                tup = (src, dst, typ, desc)
                all_events.add(tup)
    print("✅ Architecture extracted from all chunks!")
    # ---------------------
    # STEP 3: Merge into final JSON
    # ---------------------
    architecture = {
        "actors": list(all_actors.values()),
        "microservices": list(all_services.values()),
        "databases": list(all_databases.values()),
        "events": [
            {"from": f, "to": t, "type": typ, "description": d or ""}
            for f, t, typ, d in all_events
        ]
    }
    with open("merged_architecture.json", "w", encoding="utf-8") as f:
        json.dump(architecture, f, indent=2)
    print("✅ Merged architecture JSON saved: merged_architecture.json")
    return architecture
