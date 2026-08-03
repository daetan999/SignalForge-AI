"""Architecture visualization generated from validated solution components."""

from __future__ import annotations

from schemas.opportunity import SolutionComponent


def build_architecture_dot(components: list[SolutionComponent]) -> str:
    """Build a Graphviz DOT diagram for Streamlit rendering."""
    services = {component.service for component in components}
    lines = [
        "digraph SignalForge {",
        'rankdir="LR";',
        'graph [bgcolor="transparent", pad="0.2", nodesep="0.45", ranksep="0.65"];',
        'node [shape="box", style="rounded,filled", fillcolor="#F8FAFC", '
        'color="#334155", fontname="Arial"];',
        'edge [color="#64748B", penwidth="1.5"];',
        'users [label="Enterprise Users"];',
        'app [label="SignalForge Application"];',
        "users -> app;",
    ]
    previous = "app"
    service_nodes: list[tuple[str, str]] = []
    for index, service in enumerate(sorted(services), start=1):
        node = f"svc{index}"
        safe = service.replace('"', "'")
        service_nodes.append((node, safe))
        lines.append(f'{node} [label="{safe}"];')
    for node, _ in service_nodes:
        lines.append(f"{previous} -> {node};")
        previous = node
    lines.append("}")
    return "\n".join(lines)
