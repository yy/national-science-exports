#plot ternary plot overlapped by density estimation for st groups
#input: aggregated rca file, st group
#output: ternary density estimation plot of the specific st group

library(ggplot2)
library(tools)
library(ggtern)


args = commandArgs(trailingOnly=TRUE)
RCA_PATH = args[1]
#GROUP = args[2]
GROUP = args[2]
PERIOD = args[3]
PLOT_PATH = args[4]

rca_df = read.csv(RCA_PATH)
rca_df[rca_df==0] <- 0.01
rca_selected = subset(rca_df, IncomeGroup==GROUP & YEAR==PERIOD)

lines <- data.frame(x = c(0.5, 0, 0.5),
                    y = c(0.5, 0.5, 0),
                    z = c(0, 0.5, 0.5),
                    xend = c(1, 1, 1)/3,
                    yend = c(1, 1, 1)/3,
                    zend = c(1, 1, 1)/3)


plot <- rNSP::PlotTernary(rca_selected)


ggsave(PLOT_PATH, plot, device="pdf")
