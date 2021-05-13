#!/usr/bin/env Rscript
#
# Build Node and Edge data files
# Author: Dakota Murray
#
# Requires the path to the .graphml file containing the coordinates of nodes
# in the graph along with the edge to the backbone-extracted edge weights and an
# output path.
#
library(rNSP)
library(dplyr)

args = commandArgs(trailingOnly=TRUE)

node_path <- args[1]
sbm_path <- args[2]
gdp_path <- args[3]
eci_path <- args[4]
ternary_path <- args[5]
raw_gini_path <- args[6]
norm_gini_path <- args[7]
country_name_path <- args[8]
output_path <- args[9]

# Load SBM data which assigns each discipline to a group
sbm <- read.delim(sbm_path,
                  sep = "\t",
                  header = F,
                  stringsAsFactors = F) %>%
  rename(Specialty = V1, SBM = V2)


# Load Node file which contains necessary information by country
nodes <- read.csv(node_path,
                  stringsAsFactors = F) %>%
  select(-X) %>%
  rename(Period = Year) %>%
  left_join(sbm, all.x = T, by = "Specialty") %>%
  group_by(Country, Period, SBM) %>%
  summarize(
    ST = first(ST),
    prop.adv = sum(RCA > 1) / n(),
    num.pub = sum(sum_N_paper, na.rm = T)
  )

# Load GDP data, aggregate by time period
gdp <- readxl::read_excel(gdp_path, trim_ws = T) %>%
  tidyr::gather(year, gdp, c(5:63)) %>%
  rename(Country = `Country Name`) %>%
  rowwise() %>%
  mutate(Period = rNSP::ReplaceYearWithYears(year)) %>%
  ungroup() %>%
  group_by(Country, Period) %>%
  summarize(
    mean.gdp = mean(gdp, na.rm = T)
  )

# Load ECI data, aggregate by time period
eci <- read.csv(eci_path,
                strip.white = TRUE,
                stringsAsFactors = F) %>%
  rename(ECI_Country = Country) %>%
  rowwise() %>%
  mutate(
    Period = rNSP::ReplaceYearWithYears(as.numeric(Year))
  ) %>%
  ungroup() %>%
  group_by(Period, ECI_Country) %>%
  summarize(
    mean.eci = mean(ECI)
  )

# Load the Ternary data which contains RCA density for each cluster
ternary <- read.csv(ternary_path,
                    strip.white = TRUE,
                    stringsAsFactors = F) %>%
  tidyr::gather(SBM, tern.density, NM, NE, SHM) %>%
  select(-ST, -Country.Code) %>%
  rename(Country = COUNTRY,
         Period = YEAR)

# Load the raw gini calculations
raw_gini_data <- read.csv(raw_gini_path,
                     strip.white = TRUE,
                     stringsAsFactors = F) %>%
 select(COUNTRY, GINI, YEAR) %>%
 rename(Country = COUNTRY,
        raw.gini = GINI,
        Period = YEAR)

# Load the normalized gini calculations
norm_gini_data <- read.csv(norm_gini_path,
                     strip.white = TRUE,
                     stringsAsFactors = F) %>%
 select(COUNTRY, GINI, YEAR) %>%
 rename(Country = COUNTRY,
        norm.gini = GINI,
        Period = YEAR)


# Load the country name crosswalk table
country_names <- read.csv(country_name_path,
                      strip.white = TRUE,
                      sep = "\t",
                      stringsAsFactors = F)

# Now merge all the files together
countries <- nodes %>%
  left_join(country_names, by = c('Country' = 'WoS')) %>%
  left_join(gdp, by = c("WB" = "Country", "Period")) %>%
  left_join(eci, all.x = T, by = c("Period", "ECI_Country")) %>%
  left_join(ternary, by = c("Country", "Period", "SBM")) %>%
  left_join(raw_gini_data, by = c("Country", "Period")) %>%
  left_join(norm_gini_data, by = c("Country", "Period"))

# write the file
write.csv(countries, file = output_path)
