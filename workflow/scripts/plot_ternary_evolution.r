#Plot temporal density change with selected time periods

library(ggplot2)
library(ggtern)
library(dplyr)

args = commandArgs(T)
RCA_PATH = args[1]
#GROUP = args[2]
PLOT_PATH = args[2]

select_period = c('1973-1977','1983-1987','1993-1997', '2003-2007','2013-2017')

rca_df = read.csv(RCA_PATH)
rca_df$ST[rca_df$ST=="Others"] = "Lagging"
rca_df[rca_df==0] <- 0.001
rca_df <- rca_df %>%
  filter(YEAR %in% select_period) %>%
  mutate(
    ST = factor(ST, levels = c('Lagging','Developing','Proficient','Advanced'))
  )

# Build the plot
p <- rNSP::PlotTernary(rca_df, text.size = 10, title.size = 12, plot.legend = TRUE) +
  facet_grid(ST ~ YEAR, switch = "y") +
  theme(
    strip.background = element_blank(),
    strip.text = element_text(face = "bold", size = 14),
    strip.text.y = element_text(angle = 180, hjust = 1),
    legend.position = "none"
  )

# Save the output
ggsave(PLOT_PATH, p, width = 10.5, height = 8, device = "pdf")
