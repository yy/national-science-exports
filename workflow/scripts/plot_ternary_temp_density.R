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
rca_df$ST[rca_df$ST=="Others"] = "Lagging"
rca_df[rca_df==0] <- 0.01
rca_selected = subset(rca_df, ST==GROUP & YEAR==PERIOD)

# Build the plot
p <- rNSP::PlotTernary(rca_selected)

# Save the output
ggsave(PLOT_PATH, p, device="pdf")
