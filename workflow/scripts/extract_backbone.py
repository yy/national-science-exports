""" extract backbone from proximity file """
import sys
import re

import networkx as nx

import nsp.core


def extract_alpha_from_path(fpath):
    """ assuming the following format: "..._..._alpha02_..._xxx.ext"

    "alpha02" means alpha = 0.2
    """
    alpha_str = re.search(r"_alpha(\d+?)_", fpath).group(1)
    alpha = float("{}.{}".format(alpha_str[0], alpha_str[1:]))
    return alpha


PROX_FILE = sys.argv[1]
BACKBONE_FILE = sys.argv[2]
ALPHA = extract_alpha_from_path(BACKBONE_FILE)

g_com = nx.read_weighted_edgelist(PROX_FILE, delimiter="\t")
g_com.remove_edges_from(nx.selfloop_edges(g_com))
g_backbone = nsp.core.extract_backbone(g_com, ALPHA)

with open(BACKBONE_FILE, "w") as fout:
    fout.write("{}\t{}\t{}\n".format("source", "target", "weight"))
    for e in g_backbone.edges(data="weight", default=1):
        fout.write("{}\t{}\t{}\n".format(e[0], e[1], e[2]))
