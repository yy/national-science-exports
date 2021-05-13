library("plm")
library("stargazer")
library("dplyr")
library("data.table")

rca_change <- read.csv("~/Dropbox/Research/NSP-dropbox/Data/Derived/Publication_based/RCA_REGRESSION/STATIC/full/rca_regress_full_1973-2017.csv")
panel_data <- read.csv("~/Dropbox/Research/NSP-dropbox/Data/Derived/Publication_based/RCA_REGRESSION/PANEL_DATA/full/rca_regress_panel_full_1973-2017.csv")
#panel_data_li <- panel_data %>% filter(IncomeGroup == "L" | IncomeGroup == "LM")

run_models <- function(panel_data) {
  m.1 <- plm(growth_rate ~ Income_t0_log, 
			 data=panel_data, 
             index=c("Code", "date"),
             model="within")
  m.2.pooled <- plm(growth_rate ~ Income_t0_log + nm_change + ne_change + shm_change, 
                    data=panel_data, index=c("Code", "date"), 
                    model="pooling")
  m.2.fixed <- plm(growth_rate ~ Income_t0_log + nm_change + ne_change + shm_change, 
                   data=panel_data, index=c("Code", "date"), 
                   model="within", effect="twoways")
  return(list(m1=m.1, m.2.pooled=m.2.pooled, m.2.fixed=m.2.fixed))

}

result.all <- run_models(panel_data)
#result.li <- run_models(panel_data_li)

plm::plmtest(result.all$m.2.pooled, effect="individual")
plm::phtest(result.all$m.2.fixed, result.all$m.2.random)

latex.table <- stargazer(result.all, dep.var.labels=c("GDP growth (log-ratio)"), ci=TRUE, single.row=TRUE, omit_stat=c(""))
#stargazer(result.li, dep.var.labels=c("GDP growth (log-ratio)"), type="text", ci=TRUE, single.row=TRUE, omit_stat=c(""))

out.file <- file("regression_table.tex")
writeLines(c("\\documentclass{article}", "\\begin{document}", latex.table, "\\end{document}"), 
		   out.file)
close(out.file)

