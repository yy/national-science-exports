Workflow scripts that process data, run simulations, and draw figures.
Recommended workflow tool:
[`snakemake`](https://snakemake.readthedocs.io/en/stable/).

This `snakemake` workflow requires that the data directory be specified in a file titled `PROJ_HOME_DIR`.

The workflow will be executed by running the command `snakemake` in the workflow directory.

A "dryrun" can be performed by running the command `snakemake -n`.

Code to create the DAG diagram have been provided in the `makefile` in the workflow directory. Running `make` will generate and save the diagram as in SVG format in the workflow directory. Note that this requires that [`Graphviz`](http://www.graphviz.org/) be installed on the local machine.

Most packages for running scripts called during this workflow can be installed using `pipenv` and the Pipfile contained in the root project directory. However, some will require additional setup, particularity the `graph_tool` package, which must be installed manually. Given difficulties often arising from installing `graph-tool`, we have provided pre-computed output files for the `votingsbm` rule (the only rule which uses graph-tool); if this rule is removed, then these output files can be used for other rules in the Snakefile.

Included are also several R scripts which require the the following packages to be installed:

- tidyverse
- ggtern
- tools
