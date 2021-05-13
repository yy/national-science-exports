rm(list = ls())
library(ggplot2)
library(tools)
library(ggtern)
library(Rmisc)
library(dplyr)

args = commandArgs(T)
RCA_PATH = args[1]
PLOT_PATH = args[2]


rca_df = read.csv(RCA_PATH)
rca_df$ST[rca_df$ST=="Others"] = "Lagging"
rca_df[rca_df==0] <- 0.001
sts_group=c('Sub-Saharan Africa','Middle East & North Africa','South Asia','East Asia & Pacific',
            'Europe & Central Asia','Latin America & Caribbean','North America')
#sts_group =c('Lagging','Developing','Proficient','Advanced')
#select_period = c('1988-1992','1993-1997','1998-2002', '2003-2007','2008-2012','2013-2017')
select_period = c('1973-1977','1983-1987','1993-1997', '2003-2007','2013-2017')

# out_list <- list()
# i = 1
# for(year in select_period){
#   for (group in sts_group){
#     data = subset(rca_df, Region==group & YEAR==year)
#     g = plot_ternary(data)
#     out_list[[i]] <- g
#     i = i+1
#
#   }
# }
rca_df <- rca_df %>%
  filter(YEAR %in% select_period)

p <- rNSP::PlotTernary(rca_df, text.size = 10, title.size = 12, plot.legend = TRUE) +
  facet_grid(Region ~ YEAR, switch = "y") +
  theme(
    strip.background = element_blank(),
    strip.text = element_text(face = "bold", size = 14),
    strip.text.y = element_text(angle = 180, hjust = 1),
    legend.position = "none"
  )


ggsave(PLOT_PATH, p, device = "pdf", width = 12.5, height = 16)

#pdf(PLOT_PATH, width=12.5, height=16)

#multiplot(plotlist = out_list,cols=5)

#dev.off()
