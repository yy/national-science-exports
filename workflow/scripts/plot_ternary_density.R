#plot ternary plot overlapped by density estimation for st groups
#input: aggregated rca file, st group
#output: ternary density estimation plot of the specific st group

library(ggplot2)
library(tools)
library(dplyr)
library(ggtern)

args = commandArgs(T)
RCA_PATH = args[1]
#GROUP = args[2]
PLOT_PATH = args[2]

constant = 0.01
group = strsplit(file_path_sans_ext(basename(PLOT_PATH)), "_")[[1]][5]

rca_selected = read.csv(RCA_PATH, stringsAsFactors = F) %>%
  mutate(
    ST = ifelse(ST == "Others", "Lagging", ST),
    NM = ifelse(NM == 0, constant, NM),
    NE = ifelse(NE == 0, constant, NE),
    SHM = ifelse(SHM == 0, constant, SHM),
  )


rca_selected <- rca_selected %>% filter(ST == group)

# Get the plot
p <- rNSP::PlotTernary(rca_selected)

ggsave(PLOT_PATH, p, device="pdf")
