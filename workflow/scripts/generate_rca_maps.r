# Generate rca world maps
# Author: Dakota Murray

# load all data
library(dplyr)
library(rNSP)

# file type to save the documents as
fig_ext = ".pdf"

print("------------------------------")
print('Loading data')

# Load the data...
# I am assuming that the working directory is the project folder
# in the libs, and so the relative path to the symbolic link in
# the main directory would be two steps above.
nodes <- read.csv("../../data/dropbox/Derived/Publication_based/Backbone/Visualization/pub_node_datafile.csv") %>%
  select(-X)
edges <- read.csv("../../data/dropbox/Derived/Publication_based/Backbone/Visualization/pub_edge_datafile.csv") %>%
  select(-X)

# Get the filename ready for the country-mapping
mapping <- read.csv("../../data/dropbox/Additional_data/Data_cleaning/ggplot_geo_mapping.csv",
                    stringsAsFactors = F)

# Outer folder to save the disciplinary folder
# make a link vs. absolute path????/
base_path <- "../../figures/Geo/RCA_worldmaps/Publication_based/"

# Function to plot a single network for a single year/country combination
plot_one_map <- function(nodes, base_path, discipline, year, mapping) {
  # build the networl using the rNSP package
  fig <- BuildWorldMap(nodes,
                       years = year,
                       discipline = discipline,
                       mapping = mapping,
                       plot.viridis = T)

  # build the path to the folder for the specific country
  disc_path <- paste0(base_path, discipline, "/")

  # Create the folder, if it doesn't already exist
  dir.create(file.path(disc_path), showWarnings = FALSE)

  # Build the save path of the figure, base + country + filename
  save_path <- paste0(disc_path, year, "-", discipline, fig_ext)

  # Save the output
  ggplot2::ggsave(save_path, fig, width = 10, height = 10)
}

print("------------------------------")
print('Output by country, year')
disciplines <- unique(nodes$Specialty)
years <- unique(nodes$Years)
# iterate through all country/year combos
for (disc in disciplines) {
  print(disc) # for monitoring progress
  for (year in years) {
    print(year) # monitoring progress

    # plot one map with given discipline and year parameters
    plot_one_map(nodes,
                 base_path,
                 discipline = disc,
                 year = year,
                 mapping = mapping)
  }
}
