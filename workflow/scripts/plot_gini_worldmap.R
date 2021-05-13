library(tidyverse)
library(ggplot2)
library(dplyr)
library(maps)
library(viridis)
theme_set(theme_void())



world_map <- map_data("world")
ggplot(world_map, aes(x = long, y = lat, group = group)) +
  geom_polygon(fill="lightgray", colour = "gre")

gini <- read_csv("../../data/Derived/Publication_based/Gini/Normalized/gini_full_1973-2017.csv") 
gini <- gini %>% 
  rename(region = COUNTRY) %>% 
  filter(!str_detect(region, "Antarctica")) %>% 
  mutate(
    region = ifelse(region == "United States", "USA", region),
    diversity = 1 - GINI
  )

gini_map <- left_join(gini, world_map, by="region")
ggplot(gini_map, aes(long, lat, group = group))+
  geom_polygon(aes(fill = diversity), color = "white", size = 0.1)+
  scale_fill_viridis() + coord_map()


#library(rgdal)
# my_spdf <- readOGR(
#  dsn=paste0("/Users/yy/git/national-science-production/data/Additional_data/world_shape_file/"), 
#  layer="TM_WORLD_BORDERS_SIMPL-0.3", 
#  verbose=FALSE
#)
