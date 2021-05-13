#' Builds the node and edge datafiles from raw datafiles
#'
#' @export
#' @param path_to_graph Path to the graph file contianing the node labels and
#' coordiantes
#' @param path_to_count Path the the .csv file contianing the bibliometric counts
#' @param path_to_rca Path to the .csv file contianing the calculated RCA values
#' @param path_to_disciplines Path to the .csv file conitaning the disciplinary
#' classification hierarchy
#' @param outfile Path to save output node data file
#' @param showProgress Boolean, whether to show progress when loading using
#' the fread function.
#'
#' @import dplyr
#' @importFrom igraph V
#'
BuildNodeFile <- function(
  path_to_graph,
  path_to_edge_weights,
  path_to_count,
  path_to_rca,
  path_to_disciplines,
  mirror.nodes.x = FALSE,
  mirror.nodes.y = FALSE,
  showProgress = F
) {
  # --- load data files -------------------------------------------------------
  # This file contains our disciplinary taxonomy
  discipline <- data.table::fread(path_to_disciplines, header = T, showProgress = showProgress)

  # This one containts the RCA data for each country/discipline
  pub.rca <- data.table::fread(path_to_rca, showProgress = showProgress, header = T)

  # The publication counts for each country and disciplianry specialty
  paper.count <- data.table::fread(path_to_count, showProgress = showProgress) %>%
    rename(Country = COUNTRY, Specialty = SPECIALTY, Papers = PAPER_CNT, Year = YEAR) %>%
    select(-DISCIPLINE)

  # This file contains the actual graph, which was originally constructed with
  # gephi. I will be using the coordinates already stored in this file
  g <- igraph::read_graph(path_to_graph, format = "graphml")

  # --- Construct base network ------------------------------------------------


  # extract a base network from the graph—basically just the names of the
  # nodes and their positions
  nodes.with.coords <- .GetBaseNodeDataFrame(g)

  # If set, mirror the node positions
  if (mirror.nodes.x) {
    nodes.with.coords$x = -nodes.with.coords$x
  }

  if (mirror.nodes.y) {
    nodes.with.coords$y = -nodes.with.coords$y
  }
  # Now lets merge the discipline data onto the node list
  nodes.with.disc <- nodes.with.coords %>%
    left_join(discipline, by = c("label" = "level_1"))

  # --- populate RCA and Pub Count values for ndoes ---------------------------
  indicators <- .GetAggregatedIndicators(nodes.with.disc, paper.count)

  # Now, merge this new data into the original one
  nodes.pub.count.agg <- indicators %>%
    left_join(nodes.with.disc,
              by = c("Specialty" = "label")) %>%
    distinct() # remove duplicated rows

  # --- Finish constructing nodes ---------------------------------------------
  # First, flip the years if necessary
  pub.rca$YEAR <- sapply(pub.rca$YEAR, .FlipYears)

  # Rename pub.rca fields to maintain concsistency
  #pub.rca <- pub.rca %>% rename(specialty = Discipline, RCA = Measure)

  # Finally, merge this with the node dataset
  nodes.with.pub.rca <- nodes.pub.count.agg %>%
    full_join(pub.rca, by = c("Country" = "COUNTRY", "Specialty" = "DIS", "Year" = "YEAR")) %>%
    rename(RCA = VALUES) %>%
    ungroup()

  # Fill in implicitely missing conutry/discipline/year combinations
  final.nodes <- nodes.with.pub.rca %>%
    tidyr::complete(Specialty, Country, Year,
             fill = list(sum_N_paper = 0, RCA = 0)) %>%
    group_by(Country) %>%
    # Arrange data and then fill missing ST values
    arrange(Country, ST, Specialty, Year) %>%
    tidyr::fill(ST) %>%
    select(-c(x, y, abbrev, level_2, level_3)) %>%
    left_join(nodes.with.disc, by = c("Specialty" = "label"))

  return(final.nodes)
} # end BuildNodeFile


# -----------------------------------------------------------------------------

#'
#' Builds a final edge datafile from the set of relevant data files
#'
#' @export
#' @param path_to_graph Path to the graph file contianing the node labels and
#' coordiantes
#' @param path_to_edge_weights Path to the .csv file contianing edge weights
#' @param outfile Path to save output edge data file
#' @param showProgress Boolean, whether to show progress when loading using
#' the fread function.
#' @import dplyr
#' @importFrom igraph V
#'

BuildEdgeFile <- function(
  path_to_graph,
  path_to_edge_weights,
  showProgress = F
) {

  # This file contains the actual graph, which was originally constructed with
  # gephi. I will be using the coordinates already stored in this file
  g <- igraph::read_graph(path_to_graph, format = "graphml")

  # Edge weightss
  edge.weights <- read.delim(path_to_edge_weights, sep = "\t", stringsAsFactors = F)

  # --- build edge data frame -------------------------------------------------
  edges <- .GetEdgeDataFrame(g, edge.weights)

  return(edges)
} # End BuildEdgeFile


# --- Define helper function ------------------------------------------------

# Some of the year intervals were reversed, so flip them if necessary.
# This helper function accomodates it.
.FlipYears <- function(years) {
  num1 = as.integer(substr(years, 1, 4))
  num2 = as.integer(substr(years, 6, 10))
  if (num2 > num1) {
    return(paste0(num1, "-", num2))
  } else {
    return(paste0(num2, "-", num1))
  }
}


# Helper function—extracts a base node dataframe from a NSP-style graph file.
# This works on .graphml files produced by gephi. I am unsure of whether this also
# works with other graph file formats.
.GetBaseNodeDataFrame <- function(g) {
  # Get node labels from graph
  node_labels <- data.frame(label = as.character(as.matrix(V(g)$id))) %>%
    mutate(label = as.character(label))

  # Extract coordiantes from graph
  coords <- cbind("x" = V(g)$x, "y" = V(g)$y)

  # Merge labels and coordinates into single dataframe
  nodes.with.coords <- cbind(node_labels, coords)

  return(nodes.with.coords)
}

# Helper function that takes the node data (wuth disciplinary hierarchy)
.GetAggregatedIndicators <- function(
  nodes,
  paper.count
) {
  # First, create the new `Years` field variable
  nodes <- paper.count %>%
    left_join(nodes, by = c("Specialty" = "label")) %>%
    rowwise() %>%
    # for every row, replace the "year" attribute with the appropriate
    # year interval
    mutate(Year = rNSP::ReplaceYearWithYears(Year)) %>%
    ungroup() %>%
    filter(!is.na(Year)) # Filter missing values

  # Now, aggregate, summing the total number of publications
  indicators_aggregated <- nodes %>%
    group_by(Country, Specialty, Year) %>%
    summarize(
      sum_N_paper = sum(Papers)
    )

  return(indicators_aggregated)
}

# Helper function to extract the edge data from the graph, and format it into a
# dataframe with weights.
.GetEdgeDataFrame <- function(g, weights) {

  ids <- as.data.frame(V(g)$id) %>%
    mutate(index= row_number())

  # extract the edges
  edges <- igraph::as_data_frame(g, what = "edges") %>%
    left_join(ids, by = c("from" = "index")) %>%
    left_join(ids, by = c("to" = "index")) %>%
    select(-from, -to) %>%
    dplyr::rename(from = `V(g)$id.x`,
                  to = `V(g)$id.y`) %>%
    mutate(from = as.character(from), to = as.character(to))


  # The order of the labels in the edge files, but doesn't matter in the weights
  # file. Thus, we have to merge twice, considering both vertex orders, and keep
  # the correct one.
  edges <- edges %>%
    select(-weight) %>%
    left_join(weights, by = c("from" = "source", "to" = "target")) %>%
    left_join(weights, by = c("from" = "target", "to" = "source")) %>%
    mutate(
      weight = ifelse(!is.na(weight.x), weight.x, weight.y)
    ) %>%
    filter(!is.na(weight)) %>%
    filter(weight > 0) %>%
    select(-weight.x, -weight.y) %>%
    select(to, from, `Edge Label`,	`id`,	weight)

  return(edges)
}
