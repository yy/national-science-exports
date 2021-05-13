#!/usr/bin/env Rscript

# GenerateDisciplineWorldMap
# Author: Dakota Murray
#
# Takes as input the
# @input nodefile: The node datafile used to create the maps
# @input mapping: Path to the country mapping file
# @input discipline: The discipline to plot
# @input years: The year interval to plot
# @input out: Output path to save thse image




# Shuld take as input the node file to use
#
# Load optparse, which we use to parse command line arguments python style
library("optparse")

# Produce
option_list = list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="Path to input node datafile containing country-level infomration", metavar="character"),
  make_option(c("-m", "--mapping"), type="character", default=NULL,
              help="Path to the country mapping datafile that links NSP country names to the Map library country", metavar="character"),
  make_option(c("-o", "--out"), type="character", default="out.pdf",
              help="Output file name [default= %default]", metavar="character"),
  make_option(c("-d", "--discipline"), type="character", default=NULL,
              help="Discipline to plot", metavar="character"),
  make_option(c("-y", "--years"), type="character", default=NULL,
              help="Year interval to plot", metavar="character"),
  make_option("--width", type="numeric", default=7,
              help="Width of output plot", metavar="character"),
  make_option("--height", type="numeric", default=7,
              help="Height of output plot", metavar="character"),
  make_option("--threshold", action="store_true", default=FALSE,
              help="Applies an RCA cutoff, showing only colors for counrties with RCA > 1"),
  make_option("--viridis", action="store_true", default=FALSE,
              help="Attempts to plot with Viridis colors")
)

# Complete parsing
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# Load the files
# Supress warnings for this one command, as one column name is missing and
# loaded with a default name, resulting in a warning that we can
# safely ignore
options(warn=-1)
input <- readr::read_csv(opt$input, col_types = readr::cols())
mapping <- readr::read_csv(opt$mapping, col_types = readr::cols())

# Re-up the warnings
options(warn=0)

# Plot the world map
map <- rNSP::BuildWorldMap(
  nodes = input,
  discipline = opt$discipline,
  years = opt$years,
  mapping = mapping,
  rca.threshold = opt$threshold,
  plot.viridis = opt$viridis
)

# Save the plot
ggplot2::ggsave(opt$out, map, width = opt$width, height = opt$height)






