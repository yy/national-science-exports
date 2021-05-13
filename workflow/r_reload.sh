#!/bin/bash

cwd="$PWD"

Rscript -e "devtools::document(\"$cwd/../libs/rNSP\")"
Rscript -e "devtools::install(\"$cwd/../libs/rNSP\")"
