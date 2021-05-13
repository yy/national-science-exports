#!/usr/bin/env Rscript
#
# Build Node and Edge data files
# Author: Dakota Murray
#
# Requires the path to the .graphml file containing the coordinates of nodes
# in the graph along with the edge to the backbone-extracted edge weights and an
# output path.
#

args = commandArgs(trailingOnly=TRUE)

edges <- rNSP::BuildEdgeFile(
  path_to_graph = args[1],
  path_to_edge_weights = args[2])

# write the file
write.csv(edges, file = args[3])
