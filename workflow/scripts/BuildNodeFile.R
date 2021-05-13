#!/usr/bin/env Rscript
#
# Build Node and Edge data files
# Author: Dakota Murray
#
# Command line arguments requested map to what is required in the rNSP::BuildnodeEdgeFiles.R file and
# related functions—please consult this file for more information
#

# Mirroring parameters
MIRROR.NODES.X = FALSE
MIRROR.NODES.y = TRUE

# Workflow parameters
SHOW.PROGRESS = FALSE

args = commandArgs(trailingOnly=TRUE)

# construct the node datafile
nodes <- rNSP::BuildNodeFile(
  path_to_graph = args[1],
  path_to_count = args[2],
  path_to_rca = args[3],
  path_to_disciplines = args[4],
  mirror.nodes.x = MIRROR.NODES.X,
  mirror.nodes.y = MIRROR.NODES.y,
  showProgress = SHOW.PROGRESS)

write.csv(nodes, file = args[5])
