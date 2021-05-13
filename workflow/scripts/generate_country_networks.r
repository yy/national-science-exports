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

# Outer folder to save the disciplinary folder
# make a link vs. absolute path????/
base_path <- "../../figures/RCA_network/RCA_network_backbone_by_country/"

# Factor levels to order the color of nodes in the proximity netowrk
disc_levs = c("Arts and Humanities", "Social Sciences", "Engineering",
              "Medical Sciences", "Natural Sciences")

# Function to plot a single network for a single year/country combination
plot_one_network <- function(nodes, edges, base_path, country, year) {
  # build the networl using the rNSP package
  fig <- BuildNetwork(nodes,
                      edges,
                      max.node.size = 20,
                      node.color.levels = disc_levs,
                      node.colors = filtered$level_3,
                      node.sizes = filtered$total_papers,
                      node.show = filtered$high_rca)

  # build the path to the folder for the specific country
  country_path <- paste0(base_path, country, "/")

  # Create the folder, if it doesn't already exist
  dir.create(file.path(country_path), showWarnings = FALSE)

  # Build the save path of the figure, base + country + filename
  save_path <- paste0(country_path, year, "-", country, fig_ext)

  # Save the output
  ggplot2::ggsave(save_path, fig, width = 15, height = 10)
}

print("------------------------------")
print('Output by country, year')
countries <- unique(nodes$Country)
years <- unique(nodes$Years)
# iterate through all country/year combos
for (country in countries) {
  print(country) # for monitoring progress
  for (year in years) {
    print(year) # monitoring progress

    # filter to specific country/year combination
    filtered <- FilterNodes(nodes, country = country, years = year,
                                  showWarnings = FALSE)
    # If data exists for that combination, plot and save result
    if (any(filtered$total_papers > 0) & any(!is.na(filtered$high_rca))) {
      plot_one_network(filtered, edges, base_path, country, year)
    }
  }

  # Produce another result for all time intervals for that country.
  filtered <- FilterNodes(nodes, country = country, showWarnings = F)
  plot_one_network(filtered, edges, base_path, country, "all_years")
}

print("------------------------------")
print('Output for all countries, year interval')
# Finally, produce a main network for whole world, each period
for (year in years) {
  print(year)
  filtered <- FilterNodes(nodes, years = year, showWarnings = FALSE)
  plot_one_network(filtered, edges, base_path,
                   country = "all_countries", year = year)
}

# Create final set of network for all countries, all years
filtered <- FilterNodes(nodes, showWarnings = F)
plot_one_network(filtered, edges, base_path, country = "all_countries",
                 year = "all_years")
