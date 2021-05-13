#!/usr/bin/env Rscript
#
# Build Network visualization
# Author: Dakota Murray
#
# Handles the generation of the full NSP network visualization with labelss
# using the BuildNetwork function from the rNSP package.
#


# Plot parameters
PLOT_WIDTH = 15
PLOT_HEIGHT = 10

# Node parameters
NODE_COLOR_LEVELS = c("Arts and Humanities", "Social Sciences", "Engineering",
                      "Medical Sciences", "Natural Sciences")
MAX_NODE_SIZE = 15
NODE_SIZE_BREAKS = c(100000, 1000000, 3000000)

# Edge parameters
EDGE_SIZE = 0.25
EDGE_ALPHA = 0.35

# Label parameters
LABEL_SIZE = 3
LABEL_REPEL_FORCE = 2
LABEL_MIN_SEGMENT_LENGTH = 10




# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)

nodes = args[1]
edges = args[2]
output = args[3]


# Load the files
# Supress warnings for this one command, as one column name is missing and
# loaded with a default name, resulting in a warning that we can safely ignore
options(warn=-1)
nodes <- readr::read_csv(args[1], col_types = readr::cols())
edges <- readr::read_csv(args[2], col_types = readr::cols())

# Delete the first empty column
edges[, 1] <- NULL

# Re-up the warnings
options(warn=0)

# Filter and aggregate nodes for all countries and years
nodes.filtered <- rNSP::FilterNodes(nodes, showWarnings = FALSE)

# Plot the network
fig <- rNSP::BuildNetwork(nodes.filtered,
                    edges,
                    node.color.levels = NODE_COLOR_LEVELS,
                    edge.size = EDGE_SIZE,
                    edge.alpha = EDGE_ALPHA,
                    max.node.size = MAX_NODE_SIZE,
                    node.colors = nodes.filtered$level_3,
                    node.sizes = nodes.filtered$total_papers,
                    node.size.breaks = NODE_SIZE_BREAKS)

# ggrepel can many times move the labels really far away from
# the data points. Here I set a seed that results in decent labels
set.seed(91)
# Add labels
fig <- fig + ggrepel::geom_text_repel(
              ggplot2::aes(label = Specialty),
              size = LABEL_SIZE,
              force = LABEL_REPEL_FORCE,
              min.segment.length = LABEL_MIN_SEGMENT_LENGTH,

            )

print("plotting output")
ggplot2::ggsave(args[3], fig, height = PLOT_HEIGHT, width = PLOT_WIDTH, useDingbats = FALSE)
