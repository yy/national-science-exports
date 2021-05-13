#!/usr/bin/env Rscript

# Aggregate RCA datafiles
# Author: Dakota Murray
#
# takes as input the:
# @input folder: Path of folder containing the files to parse
# @input pattern: Regex pattern of files to process, within the designated
# directory
# @input out: path to save output file
# @input type: String specifying type of file to save, RCA or Prox
#

# Load optparse, which we use to parse command line arguments python style
library("optparse")

# Produce
option_list = list(
  make_option(c("-f", "--folder"), type="character", default=NULL,
              help="Path to folder containing files to load", metavar="character"),
  make_option(c("-p", "--pattern"), type="character", default=NULL,
              help="regex pattern of files to load from designated folder", metavar="character"),
  make_option(c("-o", "--out"), type="character", default="out.txt",
              help="output file name [default= %default]", metavar="character"),
  make_option(c("-t", "--type"), type="character", default=NULL,
              help="Type of input file, RCA or proximity", metavar="character")
)

# Complete parsing
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

# Load files from folder
files <- list.files(opt$folder, pattern=opt$pattern, full.names=TRUE)

# Process each individual file, producing a single data table
output <- data.table::rbindlist(lapply(files, rNSP::LoadFile, type = opt$type))

# Save the aggregate data table to the output file
write.csv(output, file = opt$out)


