#Calculate nestedness indicator(NODF) and modularity for both
#original matrix and null model.
#Null model is generated with FF model.

library(bipartite)
source("scripts/nullmodel-FF.r")
source("scripts/NODF.R")
source("scripts/sortMATRIX.R")

args = commandArgs(trailingOnly=TRUE)

ACT_NEST_MATRIX_FILE = args[1]
NEST_MODU_OUTPUT = args[2]

act_nested_matrix = read.csv(ACT_NEST_MATRIX_FILE)

NumNulls = 20
NodfRes = c()
ModuRes = c()
Flag = c()
act_nodf = NODF(act_nested_matrix)
act_modu = computeModules(act_nested_matrix)
NodfRes = c(NodfRes, act_nodf)
ModuRes = c(ModuRes, act_modu@likelihood)
Flag = c(Flag,"Actual")


for (iter in 1:NumNulls){
  null_matrix = CREATEBINNULL2(act_nested_matrix,1,1)
  #print("null model is finished")
  null_nodf = NODF(null_matrix)
  #print("cal modu")
  null_modu = computeModules(null_matrix)
  #print("modu is finished")
  NodfRes = c(NodfRes,null_nodf)
  ModuRes = c(ModuRes,null_modu@likelihood)
  Flag = c(Flag,'Null')
}


result = data.frame(NodfRes, ModuRes,Flag)
write.csv(result, NEST_MODU_OUTPUT, row.names=FALSE)