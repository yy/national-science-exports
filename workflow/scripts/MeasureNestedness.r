#Measure the nestedness metric and test the significance
#input: nestedness matrix
#output: nestedness measurement, significance plot
#library(falcon)

args = commandArgs(trailingOnly=TRUE)

NEST_MATRIX_FILE = args[1]
RESULT_FILE = args[2]


nested_matrix = read.csv(NEST_MATRIX_FILE)


setwd("scripts/NESTEDNESSR")
source("PERFORM_NESTED_TEST.R")
measure = 'NODF'
nulls = 2 #use the FF null model
ensNum = 50 #number of reshuffle


store <- PERFORM_NESTED_TEST(nested_matrix,1,1,measure,nulls,ensNum,1)

nodf = c(store$Bin_t2$NODF$Measure)
pvalue = c(store$Bin_t2$NODF$pvalue)
result = data.frame(nodf, pvalue)

setwd("../../")

#dev.copy(pdf,FIGURE_PATH)

write.csv(result,RESULT_FILE, row.names=FALSE)