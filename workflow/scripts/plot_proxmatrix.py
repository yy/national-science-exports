import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

MATRIX_FILE = sys.argv[1]
PLOT_FILE = sys.argv[2]

proxmatrix = pd.read_csv(MATRIX_FILE, sep="\t", names=["DIS1","DIS2","PROX"])
proxmatrix = proxmatrix.pivot(index="DIS1",columns="DIS2",values="PROX")

g = sns.clustermap(proxmatrix,figsize=(20,20))
g.ax_heatmap.set_ylabel("")
g.ax_heatmap.set_xlabel("")
plt.savefig(PLOT_FILE, bbox_inches="tight")
