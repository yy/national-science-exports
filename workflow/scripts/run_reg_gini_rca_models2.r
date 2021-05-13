rm(list = ls())
library("plm")
library("stargazer")
library("dplyr")
library("data.table")

args = commandArgs(T)
PANEL_DATA_PATH = args[1]
RESULTS_PATH_BALANCED = args[2]

panel_data <- read.csv(PANEL_DATA_PATH)
run_models <- function(panel_data) {
  data.1 = panel_data[panel_data$period %in% c('2008-2012'),] %>%
  make.pbalanced(balance.type="shared.individuals")
  m1 <- plm(growth_rate ~ Income_t0_log + ECI+ diversity,
             data=data.1,
             index=c("Code", "date"),
             model="pooling")

  data.2 = panel_data[panel_data$period %in% c('2008-2012','2003-2007'),] %>%
  make.pbalanced(balance.type="shared.individuals")

  m2 <- plm(growth_rate ~ Income_t0_log + ECI+ diversity,
            data=data.2, index=c("Code", "date"),
            model="within", effect="individual")

  data.3 = panel_data[panel_data$period %in% c('2008-2012','2003-2007','1998-2002'),] %>%
  make.pbalanced(balance.type="shared.individuals")

  m3 <- plm(growth_rate ~ Income_t0_log + ECI+ diversity,
            data=data.3, index=c("Code", "date"),
            model="within", effect="individual")

  data.4 = panel_data[panel_data$period %in% c('2008-2012','2003-2007','1998-2002','1993-1997'),] %>%
  make.pbalanced(balance.type="shared.individuals")
  m4 <- plm(growth_rate ~ Income_t0_log + ECI+ diversity,
            data=data.4, index=c("Code", "date"),
            model="within", effect="individual")

  data.5 = panel_data[panel_data$period %in% c('2008-2012','2003-2007','1998-2002','1993-1997','1988-1992'),] %>%
  make.pbalanced(balance.type="shared.individuals")
  m5 <- plm(growth_rate ~ Income_t0_log + ECI+ diversity,
            data=data.5, index=c("Code", "date"),
            model="within", effect="individual")




  return(list(m1=m1,m2=m2,m3=m3,m4=m4,m5=m5))

}

result.all <- run_models(panel_data)
#result.li <- run_models(panel_data_li)

#plm::plmtest(result.all$m.2.pooled, effect="individual")
#plm::phtest(m6, m7)

latex.table <- stargazer(result.all, type='html',dep.var.labels=c("GDP growth (log-ratio)"), ci=TRUE, single.row=FALSE, omit.stat=c("f"),
                         column.sep.width = "0.5pt", no.space = TRUE,font.size="footnotesize",header=FALSE,title="",
                         notes.align="l",intercept.bottom = TRUE, covariate.labels = c('GDP','ECI','Diversity'),
                         add.lines=list(c("Num.Periods", "1", "2","3","4","5")
                         )

out.file <- file(RESULTS_PATH_BALANCED)
writeLines(latex.table, out.file)
close(out.file)
