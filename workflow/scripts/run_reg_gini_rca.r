rm(list = ls())
library("plm")
library("stargazer")
library("dplyr")
library("data.table")

args = commandArgs(T)
PANEL_DATA_PATH = args[1]
RESULTS_PATH = args[2]
RESULTS_PATH_BALANCED = args[3]
RESULTS_PATH_BOTH = args[4]

panel_data <- read.csv(PANEL_DATA_PATH)



run_write_models <- function(panel_data, outpath, effect="individual") {
  m1 <- plm(growth_rate ~ Income_t0_log + ECI,
             data=panel_data,
             index=c("Code", "date"),
             model="within", effect=effect)

  m2 <- plm(growth_rate ~ Income_t0_log + diversity,
            data=panel_data,
            index=c("Code", "date"),
            model="within", effect=effect)

  m3 <- plm(growth_rate ~ Income_t0_log + ECI + diversity,
            data=panel_data,
            index=c("Code", "date"),
            model="within", effect=effect)

  m4 <- plm(growth_rate ~ Income_t0_log + nm_change + ne_change + shm_change,
                    data=panel_data, index=c("Code", "date"),
                    model="within", effect=effect)

  m5 <- plm(growth_rate ~ Income_t0_log + ECI + diversity + nm_change + ne_change + shm_change,
                   data=panel_data, index=c("Code", "date"),
                   model="within", effect=effect)
  result.all <- list(m1=m1,m2=m2,m3=m3,m4=m4,m5=m5)

  latex.table <- stargazer(result.all, type='html',dep.var.labels=c("GDP growth (log-ratio)"), ci=TRUE, single.row=FALSE, omit.stat=c("f"),
                           column.sep.width = "0.5pt", no.space = TRUE,font.size="small",header=FALSE,title="",
                           notes.align="l",covariate.labels = c('GDP','ECI','Diversity',"Natural","Physical","Societal"))

  out.file <- file(outpath)

  writeLines(latex.table, out.file)
  close(out.file)

}

run_write_models(panel_data, RESULTS_PATH)


balance_data=make.pbalanced(panel_data,balance.type="shared.individuals")
run_write_models(balance_data, RESULTS_PATH_BALANCED)
run_write_models(balance_data, RESULTS_PATH_BOTH, effect="twoways")
