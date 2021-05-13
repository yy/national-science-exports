library(ggplot2)

args = commandArgs(trailingOnly=TRUE)

ZSCORE_FILE_PATH = args[1]
PLOT_PATH = args[2]

zscore = read.csv(ZSCORE_FILE_PATH)

g = ggplot(zscore, aes(x=ZNEST, y=ZMODU, group=1))+
  geom_point(aes( fill=YEAR),shape=21, size=3)+
  geom_path(aes(color=as.factor(YEAR)),show.legend=FALSE)+
  scale_color_manual(values = c("#94f4df","#00CDC0",'#06A7B7','#0D8FBE','#1377C4','#1A5FCB',
                                '#2047D1','#272FD8','#311A65'))+
  scale_fill_manual(values = c("#94f4df","#00CDC0",'#06A7B7','#0D8FBE','#1377C4','#1A5FCB',
                                 '#2047D1','#272FD8','#311A65'))+
  theme_bw()+
  xlab("Z-score of Nestedness")+
  ylab("Z-score of Modularity")+
  theme(
    text = element_text(family="Arial",size=15)
  )

  ggsave(PLOT_PATH,g,width = 7, height=5,device=cairo_pdf)
