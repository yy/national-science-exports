#!/usr/bin/env Rscript
#
# Build Network visualization
# Author: Dakota Murray
#
# Handles the generation of the full NSP network visualization with labelss
# using the BuildNetwork function from the rNSP package.
#

# Plot parameters
PLOT_WIDTH = 8
PLOT_HEIGHT = 5

# Node parameters
NODE_COLOR_LEVELS = c("Arts and Humanities", "Social Sciences", "Engineering",
                      "Medical Sciences", "Natural Sciences")
MAX_NODE_SIZE = 15
NODE_OUTLINE_SIZE = 0.3

# Edge parameters
EDGE_SIZE = 0.35
EDGE_ALPHA = 0.2


# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)

nodes = args[1]
edges = args[2]
country = args[3]
year = args[4]
output = args[5]


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

# If the "whole period" is passed, then set the year to null so that
# we aggregate on all years.
if (year == '1973-2017') {
  year = NULL
}

# Check that the country exists in our data!
if (!country %in% nodes$Country) {
  print("The provided countery name does not exist in the nodes table")
  nodes.filtered <- NULL
} else {
  nodes.filtered <- rNSP::FilterNodes(nodes, country = country, years = year)
}

# If data exists for that combination, plot and save result
if (!is.null(nodes.filtered) & any(nodes.filtered$total_papers > 0) & any(!is.na(nodes.filtered$high_rca))) {
  fig <- rNSP::BuildNetwork(nodes.filtered,
                            edges,
                            node.colors = nodes.filtered$level_3,
                            node.color.levels = NODE_COLOR_LEVELS,
                            node.sizes = nodes.filtered$total_papers,
                            node.stroke = NODE_OUTLINE_SIZE,
                            edge.size = EDGE_SIZE,
                            edge.alpha = EDGE_ALPHA,
                            max.node.size = MAX_NODE_SIZE,
                            node.show = nodes.filtered$high_rca)
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
ggplot2::ggsave(args[5], fig, height = PLOT_HEIGHT, width = PLOT_WIDTH, useDingbats = FALSE)
