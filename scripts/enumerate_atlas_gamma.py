#!/usr/bin/env python3
"""Exhaust fixed-B Γ MILPs over connected bipartite Graph Atlas entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import networkx as nx

from mememathics_erdos23.gamma import maximize_gamma_for_fixed_b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-order", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    records = []
    for graph in nx.graph_atlas_g():
        order = graph.number_of_nodes()
        if not (1 <= order <= args.maximum_order):
            continue
        if not nx.is_connected(graph) or not nx.is_bipartite(graph):
            continue
        graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
        optimum, chosen = maximize_gamma_for_fixed_b(graph)
        records.append(
            {
                "order": order,
                "edges": graph.number_of_edges(),
                "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                "gamma": optimum,
                "bound": order * order,
                "ratio": optimum / (order * order),
                "chosen_m": chosen,
            }
        )

    records.sort(key=lambda row: (row["ratio"], row["order"], row["edges"]), reverse=True)
    payload = {"maximum_order": args.maximum_order, "instances": len(records), "records": records}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
