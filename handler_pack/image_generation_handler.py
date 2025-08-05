import graphviz

from ai_prompts import ai_layout_prompt
from ai_uitls import ai_repsonse_utility
from handler_pack import json_file_handler

graphviz_path = r"C:\Graphviz-13.1.1\Graphviz-13.1.1-win64\bin"

def generate_ai_layout(input_json: dict):

    prompt = ai_layout_prompt.get_ai_layout_prompt(input_json)
    response = ai_repsonse_utility.ai_response(prompt, "You are a helpful assistant that outputs JSON only.")

    raw_output = response.choices[0].message.content.strip()
    return raw_output


def generate_architecture_png(input_json: dict, output_file="c4_ai_diagram"):
    print("✅ Generating AI layout plan...")
    layout_json_str = generate_ai_layout(input_json)
    cleaned_layout_json = json_file_handler.fix_ai_json(layout_json_str)
    print("✅ Rendering PNG...")
    render_layout_to_png(cleaned_layout_json, output_file)
    print(f"✅ C4 Container Diagram generated: {output_file}.png")


def render_layout_to_png(layout_json: dict, output_file="c4_ai_layout"):
    """
    Renders the AI-generated layout JSON to a professional HLD diagram (PNG) using Graphviz.
    Surrounds all microservices with a dotted-line cluster.
    """
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='TB', splines='ortho', fontname='Helvetica')

    # ----------------------
    # Step 1: Identify Microservices
    # ----------------------
    microservices = [node for node in layout_json.get("nodes", []) if node.get("type", "").lower() == "service"]
    other_nodes = [node for node in layout_json.get("nodes", []) if node.get("type", "").lower() != "service"]

    # ----------------------
    # Step 2: Render Non-Microservice Nodes
    # ----------------------
    for node in other_nodes:
        node_name = node.get("name", "").strip()
        node_type = node.get("type", "").lower()
        if not node_name or node_name.lower() == "null":
            continue

        # Professional color & shape mapping
        shape = "ellipse" if node_type == "actor" else "box"
        style = "filled"
        fillcolor = node.get("color", "white")

        if node_type == "db":
            shape = "cylinder"
        elif node_type == "external":
            style = "dashed,filled"

        dot.node(
            node_name,
            shape=shape,
            style=style,
            fillcolor=fillcolor,
            fontsize="12",
            fontcolor="black",
            width="1.2",
            height="0.8",
            pos=f'{node.get("x", 0)},{node.get("y", 0)}!'
        )

    # ----------------------
    # Step 3: Render Microservices in a Cluster
    # ----------------------
    if microservices:
        with dot.subgraph(name="cluster_microservices") as c:
            c.attr(label="Microservices Layer", color="gray", style="dotted", fontsize="14", fontname="Helvetica-Bold")
            for node in microservices:
                node_name = node.get("name", "").strip()
                if not node_name:
                    continue
                c.node(
                    node_name,
                    shape="box3d",
                    style="filled",
                    fillcolor=node.get("color", "lightblue"),
                    fontsize="12",
                    fontcolor="black",
                    width="1.2",
                    height="0.8",
                    pos=f'{node.get("x", 0)},{node.get("y", 0)}!'
                )

    # ----------------------
    # Step 4: Render Edges
    # ----------------------
    for edge in layout_json.get("edges", []):
        src = edge.get("from")
        dst = edge.get("to")
        label = edge.get("label", "").strip()

        if not src or not dst:
            continue

        # Determine color/style based on label
        edge_color = "black"
        edge_style = "solid"
        if "db" in label.lower():
            edge_color = "brown"; edge_style = "dashed"
        elif "rest" in label.lower() or "api" in label.lower():
            edge_color = "black"
        elif "queue" in label.lower() or "event" in label.lower():
            edge_color = "black"; edge_style = "dashed"
        elif "grpc" in label.lower():
            edge_color = "cyan"

        dot.edge(
            src,
            dst,
            xlabel=label,
            color=edge_color,
            fontcolor=edge_color,
            fontsize="10",
            style=edge_style,
            arrowsize="0.7"
        )

    # ----------------------
    # Step 5: Render PNG
    # ----------------------
    output_path = dot.render(output_file, cleanup=True)
    print(f"✅ Professional HLD PNG generated with microservices cluster: {output_path}")
    return output_path
