#' Plot the RCA world maps in NSP-style
#'
#' @export
#' @param nodes A dataframe containing the Specialty/Discipline labels of
#' nodes, along with corresponding bibliometric data. The node labels
#' should be stored in a dataframe column titled "Specialty".
#' @param discipline A string mapping to a discipline to represent on
#' the world map
#' @param years A string mapping to a year interval to use to filter
#' RCA values. Defaulta to the most recent time period
#' @param mapping data file containing mapping between the country names
#' used in the Web of Science, and those expected by ggplot. Expected to
#' have two columns: `region` and `Mapping`, where `region` is the
#' ggplot name, and `Mapping` is the web of science name.
#' @param high.rca.alpha The alpha value for countries with high RCA
#' @param low.rca.alpha The alpha value for countries with low RCA
#' @param plot.viridis Boolean, whether or not to plot with viridis. Requires
#' that the viridis package is installed
#' @param viridis.option For plotting with viridis colors. "A character string
#' indicating the colormap option to use. Four options are available: "magma"
#' (or "A"), "inferno" (or "B"), "plasma" (or "C"), "viridis" (or "D", the
#' default option) and "cividis" (or "E")."
#' @param show.color.legend Boolean, whether or not to show the color legend
#'
#' @import ggplot2 dplyr
#'
#' @examples
#'
#' # Use default parameters
#' build_nsp_worldmap(nodes, discipline = "Sociology")
#'
#' # Plot for older interval
#' build_nsp_worldmap(nodes, discipline = "Sociology", years = "2008-2011")
#'
BuildWorldMap <- function(
  nodes,
  discipline,
  years = NULL,
  mapping = NULL,
  high.rca.alpha = 1.0,
  low.rca.alpha = 0.3,
  min.log.rca = -2,
  max.log.rca = 4,
  plot.viridis = F,
  viridis.option = "C",
  show.color.legend = TRUE,
  rca.threshold = FALSE,
  legend.title = "Log Revealed Comparative Advantage"
) {

  # Get the data of the world map
  thismap = ggplot2::map_data("world")

  # Filter by the provided discipline
  if (discipline %in% nodes$Specialty) {
    nodes <- nodes %>% filter(Specialty == discipline)
  } else {
    stop (paste0("Discipline '", discipline, "' is not found in the nodes datafile"))
  }

  # Filter by years, if provided
  if (!is.null(years)) {
    if (years %in% nodes$Years) {
      nodes <- nodes %>% filter(Years == years)
    } else {
      stop(paste0("Provided year interval, '", years, "' is not a valid interval"))
    }
  } else {
    nodes <- nodes %>% filter(Years == "2013-2017")
  }

  # --- Apply custom mapping --------------------------------------------------
  if (!is.null(mapping)) {
    nodes <- .GetNodeMapping(nodes, mapping)
  }

  # Define the threshold, 0 if the parameter is set to false, 1 if true
  threshold = ifelse(rca.threshold, 1, 0)

  # --- Merge with world map data ---------------------------------------------
  disc_map <- thismap %>%
    #group_by(region) %>%
    left_join(nodes, by = c("region")) %>%
    mutate(RCA = ifelse(RCA > threshold, log(RCA), NA)) %>%
    mutate(RCA = ifelse(RCA > max.log.rca, max.log.rca, RCA)) %>%
    mutate(RCA = ifelse(RCA < min.log.rca, min.log.rca, RCA))

  # --- Build ggplot object ----------------------------------------- ----------
  map <- .GetBaseMap(disc_map, low.rca.alpha, high.rca.alpha) +
    labs(title = discipline)

  # --- Add Theme info to map -------------------------------------------------
  map <- .AddThemeToMap(map)

  # --- Viridis colors --------------------------------------------------------
  map <- .AddColorsToMap(map, plot.viridis,
                         min.log.rca = min.log.rca, max.log.rca = max.log.rca,
                         rca.threshold = rca.threshold,
                         legend.title = legend.title)

  # --- Apply legend (or not) -------------------------------------------------
  map <- .AddLegendToPlot(map, show.color.legend)

  # Return final map
  return(map)
}

# --- Helper function ---------------------------------------------------------

# Helper function to load a mapping file and apply it to the node dataframe
.GetNodeMapping <- function(nodes, mapping) {
  # Merge mapping informaion and aggregate
  nodes <- nodes %>%
    mutate(Country = as.character(Country)) %>%
    left_join(mapping, by = c("Country" = "Mapping")) %>%
    group_by(Country) %>%
    mutate(
      RCA = weighted.mean(RCA, sum_N_paper, na.rm = T),
      paper = sum_N_paper,
      sum_N_paper = sum_N_paper
    )

  return(nodes)
}

# Builds the base world map from the filtered disciplinary data
.GetBaseMap <- function(disc_map, low.rca.alpha, high.rca.alpha) {
  map <- ggplot(disc_map, aes(long, lat, group=group, fill = RCA)) +
    geom_polygon(colour="black", size = 0.1,
                 aes(alpha = ifelse(!is.na(RCA) & !is.null(RCA),
                                    high.rca.alpha,
                                    low.rca.alpha))) +
    coord_map(xlim=c(-180,180), ylim = c(-60, 90))

  return(map)
}

# Add theme information to plot
.AddThemeToMap <- function(map) {
  map <- map +
    theme_minimal() +
    theme(legend.position = "bottom",
          plot.title = element_text(size = 14, hjust = 0.5),
          axis.title.x = element_blank(),
          axis.title.y = element_blank(),
          axis.text.x = element_blank(),
          axis.text.y = element_blank(),
          panel.grid = element_blank()) +
    guides(alpha = F)

  return(map)
}

# Adds colors to the map—wither viridis (if installed and `plot.viridis` is true)
# or base R.
.AddColorsToMap <- function(map, plot.viridis, min.log.rca, max.log.rca, rca.threshold, legend.title) {
  if (!rca.threshold) {
    return(map + scale_fill_gradient2(limits = c(min.log.rca, max.log.rca),
                                      low = "#91bfdb",
                                      mid = "#ffffbf",
                                      high = "#fc8d59",
                                      name = legend.title)
           )
  } else if (plot.viridis) {
    if (requireNamespace("viridis", quietly = TRUE)) {
      return(map + viridis::scale_fill_viridis(limits = c(0, max.log.rca),
                                               name = legend.title))
    } else {
      warning("Package \"viridis\" needed to plot in viridis colors. Using
            default ggplot color scheme")
    }
  } else {
    return(map + scale_fill_gradient(limits = c(0, max.log.rca),
                                     low = "#ffffbf",
                                     high = "#fc8d59",
                                     name = legend.title))
  }
}

# Adds a legend to the plot, if `show.color.legend` is true
.AddLegendToPlot <- function(map, show.color.legend) {
  if (show.color.legend) {
    return(map + theme(legend.position = "bottom"))
  } else {
    return(map + theme(legend.position = "none"))
  }
}
