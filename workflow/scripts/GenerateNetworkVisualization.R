#!/usr/bin/env Rscript
#
# Build Network visualization
# Author: Dakota Murray
#
# Handles the generation of a single NSP network visualization using the BuildNetwork function
# from the rNSP package.
#
library("optparse")

option_list = list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="Path to input node datafile containing country-level infomration", metavar="character"),
  make_option(c("-e", "--edges"), type="character", default=NULL,
              help="Path to the input edges datafile", metavar="character"),
  make_option(c("-o", "--out"), type="character", default="out.pdf",
              help="Output file name [default= %default]", metavar="character"),
  make_option(c("-c", "--country"), type="character", default=NULL,
              help="Country to plot (if any)", metavar="character"),
  make_option(c("-y", "--years"), type="character", default=NULL,
              help="Year interval to plot", metavar="character"),
  make_option("--width", type="numeric", default=5,
              help="Width of output plot", metavar="character"),
  make_option("--height", type="numeric", default=8,
              help="Height of output plot", metavar="character")
)


# Complete parsing
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# Load the files
# Supress warnings for this one command, as one column name is missing and
# loaded with a default name, resulting in a warning that we can
# safely ignore
options(warn=-1)
nodes <- readr::read_csv(opt$input, col_types = readr::cols())
edges <- readr::read_csv(opt$edges, col_types = readr::cols())

# Delete the first empty column
edges[, 1] <- NULL

# Re-up the warnings
options(warn=0)

# Filter and aggregate nodes
nodes.filtered <- rNSP::FilterNodes(nodes, country = opt$country, years = opt$years)

disc_levels = c("Arts and Humanities", "Social Sciences", "Engineering", "Medical Sciences", "Natural Sciences", "Other")
net <- rNSP::BuildNetwork(nodes.filtered,
                          edges,
                          node.colors = nodes.filtered$level_3,
                          node.color.levels = disc_levels,
                          node.sizes = nodes.filtered$total_papers,
                          edge.size = 0.35,
                          edge.alpha = 0.2,
                          max.node.size = 15,
                          node.show = nodes.filtered$high_rca)


ggplot2::ggsave(opt$out, net, height = opt$width, width = opt$height)
sprintf("Saved to file %s", opt$out)
