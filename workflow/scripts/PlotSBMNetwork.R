#!/usr/bin/env Rscript
#
# Build Network visualization
# Author: Dakota Murray
#
# Handles the generation of the full NSP network visualization with labelss
# using the BuildNetwork function from the rNSP package.
#
library(dplyr)

# Plot parameters
PLOT_WIDTH = 5
PLOT_HEIGHT = 8


MAX_NODE_SIZE = 15
NODE_OUTLINE_SIZE = 0.3

# Edge parameters
EDGE_SIZE = 0.35
EDGE_ALPHA = 0.2

# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)

nodes = args[1]
edges = args[2]
sbm = args[3]
output = args[4]

# Load the files
# Supress warnings for this one command, as one column name is missing and
# loaded with a default name, resulting in a warning that we can safely ignore
options(warn=-1)
nodes <- readr::read_csv(nodes, col_types = readr::cols())
edges <- readr::read_csv(edges, col_types = readr::cols())

# Delete the first empty column
edges[, 1] <- NULL

# Re-up the warnings
options(warn=0)

# Load the SBM group labels
sbm <- read.delim(sbm, sep = "\t", header = F) %>%
  rename(Specialty = V1, SBM = V2)

nodes.filtered <- rNSP::FilterNodes(nodes, country = NULL, years = NULL) %>%
  left_join(sbm, all.x = T)


# If data exists for that combination, plot and save result
if (any(nodes.filtered$total_papers > 0) & any(!is.na(nodes.filtered$high_rca))) {
  fig <- rNSP::BuildNetwork(nodes.filtered,
                            edges,
                            node.colors = nodes.filtered$SBM,
                            node.sizes = nodes.filtered$total_papers,
                            node.stroke = NODE_OUTLINE_SIZE,
                            edge.size = EDGE_SIZE,
                            edge.alpha = EDGE_ALPHA,
                            max.node.size = MAX_NODE_SIZE) +
                      ggplot2::guides(size = F, fill = F)
} else {
  # Else, save a blank pdf
   fig <- ggplot2::ggplot() +
            ggplot2::geom_text(ggplot2::aes(label = paste0("No Data for ", country,
                                                           "\nduring period ", year),
                                   x = 1,
                                   y = 1),
                                size = 5)

}

# Save the plot
ggplot2::ggsave(args[4], fig, height = PLOT_WIDTH, width = PLOT_HEIGHT, useDingbats = FALSE)
