#!/usr/bin/env Rscript
#
# Plot GDP against Specialization measure
# Author: Dakota Murray
#
library(dplyr)
library(ggplot2)

# Plot parameters
PLOT_WIDTH = 7
PLOT_HEIGHT = 5

POINT.SIZE = 4


# Parse command line arguments
args = commandArgs(trailingOnly=TRUE)

country_data <- args[1]
sbm_group <- args[2]
period <- args[3]
output = args[4]

country_label_list = c("USA", "QAT", "SGP", "KWT", "CHE", "NOR", "GBA", "CA",
                       "RUS", "IND", "KOR", "AUS", "UKR", "BGD", "FRA", "JPN",
                       "CHN", "NGA", "GRC")

# Load the aggregate data file and filter to SBM group and period
country_data <- read.csv(country_data, stringsAsFactors = F) %>%
  filter(SBM == sbm_group & Period == period)

if (any(!is.na(country_data$mean.gdp))) {
  # Calculate an R squared value to show on the plot
  fit.sbm <- lm(data = country_data, log(`mean.gdp`) ~ prop.adv)
  r2.sbm <- summary(fit.sbm)$r.squared


  # Create the figure
  fig <- country_data %>%
    filter(!is.na(ST)) %>%
    mutate(ST = factor(ST, levels = c("Advanced", "Proficient", "Developing", "Lagging", "Others")),
           SBM = factor(SBM, levels = c("NM", "NE", "SHM"))
    ) %>%
    ggplot(aes(x = log(mean.gdp), y = prop.adv)) +
      geom_point(aes(fill = ST, alpha = ST), size = POINT.SIZE, shape = 21) +
      geom_smooth(method = "lm") +
      theme_minimal() +
      scale_fill_manual(values = c("#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000")) +
      scale_alpha_ordinal(range = c(1, 0.5)) +
      labs(x = "Log GDP",
           y = paste0("Cluster Strength: ", sbm_group),
           title = paste("r2 =", round(r2.sbm, 3)),
           parse = T
      ) +
      ggrepel::geom_text_repel(aes(label = ifelse(Code %in% country_label_list, Code, "")), min.segment.length = 0.1, nudge_x = 0.08, nudge_y = 0.08) +
      theme(
        plot.title = element_text(size = 12),
        legend.position = "bottom",
        legend.title = element_blank(),
        axis.title = element_text(size = 12)
      )
} else {
  fig <- ggplot2::ggplot() +
           ggplot2::geom_text(ggplot2::aes(label = paste0("No Data for ", sbm_group,
                                                          "\nduring period ", period),
                                  x = 1,
                                  y = 1),
                               size = 5)
}

# Save the plot
ggplot2::ggsave(output, fig, width = PLOT_WIDTH, height = PLOT_HEIGHT, useDingbats = FALSE)
