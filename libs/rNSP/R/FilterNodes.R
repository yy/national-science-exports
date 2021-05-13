#' Filters the NSP node dataframe to that of a select country or year, or,
#' aggregates data over a range of conutries and years
#'
#' @description In the case that a list of countries or years are provided,
#' the RCA is calculated as a mean of all the RCA values of the countries,
#' weighted by the total number of papers.
#'
#' @export
#' @param node_table The node datafile to filter or aggregate, in NSP long
#' format
#' @param country A select country or vector of countries to filter by or
#' aggregate over
#' @param years A select year interval to vector of intervals to filter by
#' or aggreegate over. All intervals must also appear in the in the
#' @param showWarnings Boolean, whetehr to show warnings.
#' @import dplyr
#'
#' @examples
#' # aggregates over all countries and years
#' filter_nsp_nodes(nodes)
#'
#' # aggregates USA data over all years
#' filter_nsp_nodes(nodes, country = "United States")
#'
#' # Aggregate over all countries for a specified time interval
#' filter_nsp_data(nodes, years = "2012-2016")
#'
#' # Filter to a single country and year
#' filter_nsp_data(nodes, country = "United States", years = "2012-2016")
#'
#' # Filter to a list of countries and a list of years
#' filter_nsp_data(nodes, years = c("2008-2011", "2012-2016"), conutry = c("Germany", "France"))
#'
FilterNodes <- function(node_table, country = NULL, years = NULL, showWarnings = TRUE) {

  # If the node table doesn't have the necesary information, stop the function
  if (! all(c("Country", "Specialty", "Year",
              "sum_N_paper", "x", "y", "level_3",
              "RCA") %in% names(node_table))) {
    stop("Please make sure that the node data table follows the correct naming
          format and includes all necessary variables.")
  }

  # --- Filter by year --------------------------------------------------------
  node_table <- .FilterByYear(node_table, years, showWarnings)

  # --- Filter by country -----------------------------------------------------
  node_table <- .FilterByCountry(node_table, country, showWarnings)

  # --- Aggregate and Return --------------------------------------------------
  return(.Aggregate(node_table))
} # End filter_nsp_nodes

# --- Helper Functions --------------------------------------------------------
# Check if a year interval is provided. If so, check if a valid interval.
# If so, filter accordingly. Do the same if a list of intervals is provided,
# except aggregate over all intervals in the list. If no intervals are
# provided, then aggregate all.
.FilterByYear <- function(node_table, years, showWarnings) {
  if (is.null(years)) {
    if (showWarnings) {
      warning("No year interval provided, calculating for entire time period\n")
    }
  } else {
    if (any(!years %in% node_table$Year)) {
      stop(paste0("The stated year interval, ", years,
                  ", does not exist in the node table"))
    } else {
      if (length(years) == 1) {
        # A country was provided, and the country exists in the data table.
        # Complete the filtering.
        node_table <- node_table %>% filter(Year == years)
      } else if (length(years) > 1) {
        node_table <- node_table %>% filter(Year %in% years)
      } else {
        stop("Encountered error from the specified years vector")
      }
      node_table <- node_table %>% filter(Year == years)
    }
  }
  return(node_table)
} # End .FilterByYear

# Check if counrty is provided. If so, check if its a single coutry or a list
# of countries. If a single country, filter. If a list, filter and aggregate
# over all countries. If no country is provided, aggregate over all countries
.FilterByCountry <- function(node_table, country, showWarnings) {
  if (is.null(country)) {
    if (showWarnings) {
      warning("No country provided, calculating for entire time perion\n")
    }

  } else {
    # If the country name does not appear in the table..
    if (any(!country %in% node_table$Country)) {
      stop(paste0("The stated country name, ", country,
                  ", does not exist in the node table"))
    } else {
      if (length(country) == 1) {
        # A country was provided, and the country exists in the data table.
        # Complete the filtering.
        node_table <- node_table %>% filter(Country == country)
      } else if (length(country) > 1) {
        node_table <- node_table %>% filter(Country %in% country)
      } else {
        stop("Encountered error from the specified country vector")
      }
    }
  }
  return(node_table)
} # End .FilterByCountry

# Aggregastes the node_table over the specialties. Calculates the sum of the
# total publications, and the weighted mean of the RCA for the countries/
# intervals, weighted by the total publication count.
.Aggregate <- function(node_table) {
  return(node_table %>%
           group_by(Specialty) %>%
           summarize(
             # Sumamrize the total number of papers ofer the disciplines
             total_papers = sum(sum_N_paper),
             # Carry through the other relevant variables
             level_3 = first(level_3),
             x = first(x),
             y = first(y),
             RCA = weighted.mean(RCA, sum_N_paper)
           ) %>%
           mutate(
             high_rca = RCA > 1
           )
         ) # end return
} # end .Aggregate


