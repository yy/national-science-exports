#' Plot a network in NSP style given NSP node and edge data
#'
#' @export
#'
#' @importFrom dplyr %>% select mutate
#' @import ggplot2
#' @import ggtern
#'

PlotTernary <- function(
  data,
  n = 100,
  point.size = 0.3,
  plot.legend = FALSE,
  gradient.max = NA,
  text.size = 30,
  title.size = 30
  ) {

  lines <- data.frame(x = c(0.5, 0, 0.5),
                      y = c(0.5, 0.5, 0),
                      z = c(0, 0.5, 0.5),
                      xend = c(1, 1, 1)/3,
                      yend = c(1, 1, 1)/3,
                      zend = c(1, 1, 1)/3)


  p <- ggtern(data=data, aes(x=NM, y=SHM, z=NE)) +
      #geom_segment(data = lines, aes(x, y, z,
                   #xend = xend, yend = yend, zend = zend),
                 #color = 'lightgrey', size = 0.3) +
      stat_density_tern(
        aes(fill = ..level..),
        geom='polygon',
        n = n
      ) + #now you need to use stat_density_tern
      geom_point(size = point.size, color = 'black')+
      scale_fill_gradient2(high = "red",
        name = "Level"
      ) +
      guides(color = F, alpha = F)+
      xlab("N")+
      ylab("S")+
      zlab("P")+
      scale_T_continuous(breaks = c()) +
      scale_L_continuous(breaks = c()) +
      scale_R_continuous(breaks = c()) +
      theme_bw() +
      theme(text = element_text(size=text.size, family = "Helvetica"),
            axis.title = element_text(size = title.size),
            panel.grid.major = element_blank(),
            panel.grid.minor = element_blank(),
            plot.margin=grid::unit(c(0,0,0,0), "mm"),
            panel.border = element_rect(colour = "black", fill=NA, size=0.3),
            tern.axis.title.T  = element_text(vjust=0.8),
            tern.axis.title.R  = element_text(hjust=0.8),
            tern.axis.title.L  = element_text(hjust=0.2)
      )

    if (plot.legend == TRUE){
      p <- p +
        theme(
          legend.position=c(0.87,0.6),
        )
    } else {
      p <- p + theme(
        legend.position = "none"
      )
    }

    return(p)
}
