#' Plot a network in NSP style given NSP node and edge data
#'
#' @export
#' @param nodes A dataframe containing the Specialty/Discipline labels of nodes,
#' along with corresponding x and y coordinates. The node labels should be
#' stored in a dataframe column titled "Specialty".
#' @param edges A dataframe containing the edges data for the network, in the
#' format returned from the igraph function \code{as_data_frame(g, what = "edges")}
#' @param node.color Color of all nodes, if no node-wise colors are defined
#' @param node.colors Vector containing factor values dictating colors of nodes,
#' in same order as nodes appear in the `nodes` dataframe
#' @param node.color.levels Factor levels for the `node.colors``variable
#' @param node.color.name The title of the color legend
#' @param node.size Size of all nodes, if no node-wise sizes are provided
#' @param node.sizes Vector containing sizes of all nodes, in same order as they
#' appesr in the `nodes` dataframe
#' @param max.node.size Maximum size, in regards to area, of nodes when plotting
#' @param node.size.breaks A vector of breaks to be used in the node size legend.
#' @param node.size.labels A vector of labels to be used in the node size legend.
#' Must be the same size as the `node.size.breaks` variable
#' @param node.size.name The title of the size legend
#' @param node.show A logical vector specifying whether each node should be made
#' visible, of the same size and orders of the `nodes` dataframe
#' @param node.stroke The size of the border of the nodes
#' @param node.alpha The alpha value of visible nodes
#' @param edge.color The color of edges
#' @param edge.size The size of edges
#' @param viridis.option For plotting with viridis colors. "A character string
#' indicating the colormap option to use. Four options are available: "magma"
#' (or "A"), "inferno" (or "B"), "plasma" (or "C"), "viridis" (or "D", the
#' default option) and "cividis" (or "E")."
#' @param show.legend.size Boolean value, whether or not to show size legend
#' @param show.legend.size Boolean value, whether or not to show color legend
#'
#' @return A ggplot2 object containing the NSP style network visualization
#'
#' @importFrom dplyr %>% select mutate
#' @import ggplot2
#' @import scales
#' @examples
#' nodes <- get_node_data()
#' edges <- get_edge_data()
#'
#' usa_nodes <- get_country_year_nodes(nodes)
#'
#' # Plot network with defaul options
#' build_nsp_network(usa_nodes, edges)
#'
#' # Plot network with custom colors
#' build_nsp_network(usa_nodes, edges, node.colors = usa_nodes$level_3, node.size = 3)

BuildNetwork <- function(
  nodes,
  edges,
  node.color = "black",
  node.colors = NULL,
  node.color.levels = NULL,
  node.color.name = "Discipline",
  node.size = 5,
  node.sizes = NULL,
  max.node.size = 10,
  node.size.breaks = NULL,
  node.size.labels = NULL,
  node.size.name = "Publication Count",
  node.show = NULL,
  node.stroke = 1.1,
  node.alpha = 1.0,
  edge.color = "grey",
  edge.size = 0.2,
  edge.alpha = 0.4,
  viridis.option = "C",
  show.legend.size = TRUE,
  show.legend.color = TRUE
) {
  # -- Create network object --------------------------------------------------
  graph <- igraph::graph_from_data_frame(edges, directed = F, vertices = nodes)
  net = intergraph::asNetwork(graph)

  # -- Extract edges ----------------------------------------------------------
  edge.coords <- .GetEdgeCoordiantes(nodes, net)

  # -- Check for color args  --------------------------------------------------
  will.add.color.legend = TRUE

  # if no node-wise colors given, assign default color
  if (is.null(node.colors)) {
    will.add.color.legend = FALSE
    node.colors = rep(node.color, dim(nodes)[1])
  } else if (!is.null(node.show) & all(is.na(node.show))) {
    will.add.color.legend = FALSE
  }
  nodes$node.colors <- node.colors

  # Assign levels to the color, if its a factor variable
  nodes <- .AddColorLevels(nodes, node.colors, node.color.levels)

  # -- Check for size args ----------------------------------------------------
  will.add.size.legend <- TRUE
  if (is.null(node.sizes)) {
    will.add.size.legend <- FALSE
    node.sizes <- rep(node.size, dim(nodes)[1])
  }
  nodes$node.sizes <- node.sizes

  # -- Prepare GGplot object  -------------------------------------------------
  base <- nodes %>%
    ggplot(aes(x = x, y = y))

  # -- Add nodes and edges  ---------------------------------------------------
  base <- .AddEdgesToNet(base, edge.coords, edge.size, edge.alpha)
  #return(base)
  base <- .AddNodesToNet(base, nodes, node.show, node.sizes, node.colors,
                         node.stroke, node.alpha)

  # -- Add color info, if given  ----------------------------------------------
  base <- .AddColorLegendToNet(base, show.legend.color, will.add.color.legend,
                               node.color.name, viridis.option)


  # -- Add size info, if given  -----------------------------------------------
  base <- .AddSizeLegendToNet(base, show.legend.size, will.add.size.legend,
                              node.size.name, max.node.size,
                              node.alpha, node.stroke,
                              node.size.breaks, node.size.labels)

  # -- Add theme info  --------------------------------------------------------
  base <- .AddThemeToNet(base)

  # -- return  ----------------------------------------------------------------
  return(base)
}


# --- Helper functions --------------------------------------------------------

# helper function to extract and format edges
.GetEdgeCoordiantes <- function(nodes, net) {
  edge_list = network::as.matrix.network.edgelist(net)

  # Convert the edge list into a series of coordinates
  edge.coords <- data.frame(nodes[edge_list[, 1], ]$x,
                            nodes[edge_list[, 2], ]$x,
                            nodes[edge_list[, 1], ]$y,
                            nodes[edge_list[, 2], ]$y)

  # Set the names of this new edge.coords dataframe
  names(edge.coords) <- c("X1", "X2", "Y1", "Y2")

  return(edge.coords)
}

# Helper function to apply node color levels logic
.AddColorLevels <- function(nodes, node.colors, node.color.levels) {
  if (!is.null(node.color.levels)) {
    if (!is.null(node.colors)) {
      if (class(node.colors) == "factor" | class(node.colors) == "character") {
        nodes <- nodes %>%
          mutate(node.colors = factor(node.colors, levels = node.color.levels))
      } else {
        warning("If you define node color levels, then the node color variable
                should be continuous")
      }
    } else {
      warning("If you define node color levels, then you must also provide a column
              containing the colors.")
    }
    }
  return(nodes)
}

# Helper function to add the edges to the network
.AddEdgesToNet <- function(g, edge.coords, edge.size, edge.alpha) {
  g <- g +
    geom_segment(
      data = edge.coords,
      size = edge.size,
      alpha = edge.alpha,
      color = "grey",
      aes(x = X1, y = Y1, xend = X2, yend = Y2))

  return(g)
}

# Helper function to add the nodes to the network graph
.AddNodesToNet <- function(g, nodes, node.show, node.sizes, node.colors,
                           node.stroke, node.alpha) {
  # -- Check whether node.show was provided, set default
  if (is.null(node.show)) {
    node.show = rep(TRUE, dim(nodes)[1])
  } else if (all(is.na(node.show))) {
    node.show = rep(TRUE, dim(nodes)[1])
  } else {
    # fill in the missing node.show values
    node.show[is.na(node.show)] <- FALSE
  }

  # Add base layer of nodes
  g <- g +
    geom_point(alpha = ifelse(node.show, node.alpha, 0),
              shape = 21,
              color = "black",
              stroke = node.stroke,
              aes(fill = node.colors, size = node.sizes))

  # Add vanished points
  if (any(node.show)) {
    g <- g +
      geom_point(alpha = ifelse(node.show, 0, 1),
                 shape = 21,
                 color = "black",
                 stroke = node.stroke,
                 aes(size = node.sizes))
  }
  return(g)
}


# Helper function to add color legend
.AddColorLegendToNet <- function(g, show.legend.color, will.add.color.legend,
                                 node.color.name, viridis.option) {
  if (show.legend.color & will.add.color.legend) {
    # If viridis is not loaded, use default colors
    if (!requireNamespace("viridis", quietly = TRUE)) {
      warning("Package \"viridis\" needed to plot in viridis colors. Using
              default ggplot color scheme")

      g <- g +
        scale_fill_discrete(name = node.color.name,
                            palette = "Set1")
    } else {
      # If viridis is loaded, then use these colors
      g <- g +
        viridis::scale_fill_viridis(name = node.color.name,
                                    discrete = TRUE,
                                    option = viridis.option)
    }

    # add theme and guide to plot
    g <- g +
      theme(legend.key = element_rect(colour = NA, fill = NA)) +
      guides(fill = guide_legend(override.aes = list(size=5,
                                                     pch = 21,
                                                     alpha = 0.9)))
  } else {
    g <- g +
      guides(fill = FALSE)
  } # end will.add.color.legend

  return(g)
}


# Helper function to add a size legend
.AddSizeLegendToNet <- function(g, show.legend.size, will.add.size.legend,
                                node.size.name, max.node.size,
                                node.alpha, node.stroke,
                                node.size.breaks, node.size.labels) {
  # Assign default size breaks and labels
  if (is.null(node.size.breaks)) {
    node.size.breaks <- waiver()
  }

  # Assign default size breaks and labels
  if (is.null(node.size.labels)) {
    node.size.labels <- waiver()
  }

  if (show.legend.size & will.add.size.legend)  {
    g <- g +
      scale_size_area(name = node.size.name,
                      max_size = max.node.size,
                      breaks = node.size.breaks,
                      labels = comma) +
      guides(
        size = guide_legend(override.aes = list(pch = 21,
                                                fill = "grey",
                                                alpha = node.alpha,
                                                stroke = node.stroke))
      )
  } else {
    g <- g +
      guides(size = FALSE)
  } # end will.add.size.legend

  return(g)
}


# Add a theme to the network
.AddThemeToNet <- function(g) {
  g <- g +
    theme_minimal() +
    theme(axis.text = element_blank(),
          axis.title = element_blank(),
          panel.grid = element_blank(),
          legend.title = element_text(face = "bold", size = 14),
          legend.text = element_text(size = 14),
          legend.text.align = 1
      )

  return(g)
}
