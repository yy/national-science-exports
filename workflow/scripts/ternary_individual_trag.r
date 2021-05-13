library(ggplot2)
library(ggtern)
library(tools)


# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)
rca_file=args[1]
country=args[2]
output=args[3]

rca_df = read.csv(rca_file)
rca_df[rca_df==0] <- 0.01

year=c("1973-1977","1978-1982","1983-1987","1988-1992","1993-1997","1998-2002","2003-2007","2008-2012","2013-2017")
f_df = subset(rca_df, COUNTRY==country)
#f_df = dplyr::filter(rca_df, (COUNTRY==country))
#f_df = f_df[match(year, f_df$YEAR),]




 lines <- data.frame(x = c(0.5, 0, 0.5),
                     y = c(0.5, 0.5, 0),
                     z = c(0, 0.5, 0.5),
                     xend = c(1, 1, 1)/3,
                     yend = c(1, 1, 1)/3,
                     zend = c(1, 1, 1)/3)


 g = ggtern::ggtern(data=f_df, aes(x=NM, y=SHM, z=NE)) +
   geom_path(color="grey60")+
   geom_point(aes(color=YEAR),size=2,guide=FALSE) +
   scale_color_brewer(palette="Blues")+
   geom_point(aes(x=0.5,y=0.5,z=0.5),color='gray40',size=0.3)+
   geom_segment(data = lines, aes(x, y, z,
                                  xend = xend, yend = yend, zend = zend),
                color = 'grey40', size = 0.5, linetype="dashed")+

   geom_point(size=0.2,color='black')+
   xlab("N")+
   ylab("S")+
   zlab("P")+
   scale_T_continuous(breaks = c(0.5)) +
   scale_L_continuous(breaks = c(0.5)) +
   scale_R_continuous(breaks = c(0.5)) +
   theme_bw()+
   theme(legend.position="none",
         text = element_text(size=30),
         panel.grid.major = element_blank(),
         panel.grid.minor = element_blank(),
         plot.margin=grid::unit(c(0,0,0,0), "mm"),
         panel.border = element_rect(colour = "black", fill=NA, size=0.3),
         tern.axis.title.T  = element_text(vjust=0.8),
         tern.axis.title.R  = element_text(hjust=0.8),
         tern.axis.title.L  = element_text(hjust=0.2)
         )

ggsave(args[3], g, device="pdf")
