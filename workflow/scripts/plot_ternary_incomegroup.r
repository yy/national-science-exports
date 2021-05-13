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
income.levels = c('L','LM','UM','H')
select_period = c('1988-1992','1993-1997','1998-2002', '2003-2007','2008-2012','2013-2017')


rca_df <- rca_df %>%
  mutate(IncomeGroup = factor(IncomeGroup,
                              levels = income.levels,
                              labels = c("Lower", "Lower-Middle", "Upper-Middle", "High")
                      )
         )



p <- rNSP::PlotTernary(rca_df, text.size = 10, n = 100, title.size = 12, plot.legend = TRUE) +
  facet_grid(IncomeGroup ~ YEAR, switch = "y") +
  theme(
    strip.background = element_blank(),
    strip.text = element_text(size = 14),
    strip.text.y = element_text(angle = 180, hjust = 1),
    legend.position = "none"
  )

# Save the output
ggsave(PLOT_PATH, p, width = 8, height = 8)
