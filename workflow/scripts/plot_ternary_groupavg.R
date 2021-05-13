rm(list = ls())
library(ggplot2)
library(ggtern)
library(tools)
library(dplyr)


args = commandArgs(T)
RCA_PATH = args[1]
PLOT_PATH = args[2]

rca_df = read.csv(RCA_PATH)
rca_df[rca_df==0] <- 0.01


groupavg=rca_df %>%
  select(IncomeGroup,YEAR,NM,NE,SHM) %>%
  group_by(IncomeGroup,YEAR) %>%
  summarise_all("mean")

lines <- data.frame(x = c(0.5, 0, 0.5),
                    y = c(0.5, 0.5, 0),
                    z = c(0, 0.5, 0.5),
                    xend = c(1, 1, 1)/3,
                    yend = c(1, 1, 1)/3,
                    zend = c(1, 1, 1)/3)
text.size = 30
title.size = 30

plot <- ggtern::ggtern(data=groupavg, aes(x=NM, y=SHM,z=NE,colour=YEAR)) +
  geom_path(aes(group=IncomeGroup),size=0.4)+
  geom_point(aes(shape=IncomeGroup),size=2,guide=FALSE)+
  scale_color_brewer(palette="Blues")+
  geom_point(aes(x=0.5,y=0.5,z=0.5),color='gray40',size=0.3)+
  annotate(geom="text",
           x=c(0.6,0.4,0.2,0.4),
           y=c(0.1,0.1,0.1,0.3),
           z=c(0.3,0.5,0.7,0.3),
           label=c('L','LM','UM','H'),size=6)+

  #geom_segment(data = lines, aes(x, y, z,
  #xend = xend, yend = yend, zend = zend),
  #color = 'grey40', size = 0.5, linetype="dashed")+
  #ggtern::stat_density_tern(aes(fill=..level.., alpha=..level..),geom='polygon',bins=10) +#now you need to use stat_density_tern
  #scale_fill_gradient2(high = "red")+
  #guides(color = "none", alpha = "none")+
  geom_point(size=0.2,color='black')+
  xlab("N")+
  ylab("S")+
  zlab("P")+
  scale_T_continuous(breaks = c()) +
  scale_L_continuous(breaks = c()) +
  scale_R_continuous(breaks = c()) +
  theme_bw()+
  theme(text = element_text(size=30, family = "Helvetica"),
        axis.title = element_text(size = 30),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.margin=grid::unit(c(0,0,0,0), "mm"),
        panel.border = element_rect(colour = "black", fill=NA, size=0.3),
        tern.axis.title.T  = element_text(vjust=0.9),
        tern.axis.title.R  = element_text(hjust=0.9),
        tern.axis.title.L  = element_text(hjust=0.1),
        legend.position = "none"
  )
ggsave(PLOT_PATH, plot, device="pdf")
