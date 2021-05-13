#plot ternary plot overlapped by income level
#input: Ternary plot file contains countries position and their income level
#output: ternary plot with node colored by their income

library(ggplot2)
library(ggtern)
library(tools)

args = commandArgs(T)
Ternary_Income = args[1]
PERIOD = args[2]
PLOT_PATH = args[3]

data = read.csv(Ternary_Income)
data[data==0] <- 0.01
#data$Income = log10(data$INCOME)
data = subset(data, YEAR==PERIOD)

# Build the plot
p <- ggtern(data=data, aes(x=NM, y=SHM, z=NE))+
  geom_point(aes(color=INCOME),alpha = 0.8, size = 1)+
  scale_color_viridis_c()+
  xlab("N")+
  ylab("S")+
  zlab("P")+
  scale_T_continuous(breaks = c()) +
  scale_L_continuous(breaks = c()) +
  scale_R_continuous(breaks = c()) +
  theme_bw() +
  theme(
    text = element_text(size=16, family = "Helvetica"),
    axis.title = element_text(size = 30),
    legend.position=c(0.82,0.6),
    legend.text=element_text(size=15),
    legend.key.size=unit(1.5,"line"),
    legend.title=element_blank(),
    axis.ticks=element_blank(),
    panel.grid.minor = element_blank(),
    plot.margin=grid::unit(c(0,0,0,0), "mm"),
    panel.border = element_rect(colour = "black", fill=NA, size=0.3),
    tern.axis.title.T  = element_text(vjust=0.8),
    tern.axis.title.R  = element_text(hjust=0.8),
    tern.axis.title.L  = element_text(hjust=0.2)
  )

ggsave(PLOT_PATH, p, device="pdf")
