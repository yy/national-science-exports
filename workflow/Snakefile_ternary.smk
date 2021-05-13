################################################################################
# Snakefile_ternary.smk
#
# Contains rules relating calculation, aggregation, analysis, and visualization
# of ternary/simplex data. Rules are roughly organized along the following
# sections:
#
# - Data Processing: Ternary
# - Visualization: Ternary plots
################################################################################

# Data Processing: Ternary
rule prepare_ternary:
    input: rules.agg_rca.output, LEIDEN_GROUP, FLAG_TABLE
    output: TER_DATA
    shell: "python scripts/prepare_ternary.py {input} {output}"

rule agg_ternary_income:
    input: rules.prepare_ternary.output, GDP_WB_FILE
    output: TER_INCOME_DATA
    shell: "python scripts/agg_ternary_income.py {input} {output}"

rule reclassify_country_by_ternary:
    input: rules.prepare_ternary.output
    output: RECLASSIFY_BY_TERNARY_DATA
    shell: "python scripts/reclassify_country_by_ternary.py {input} {output}"

rule ternary_income:
    input: INCOME_GROUP, rules.prepare_ternary.output,INTERVAL_FILE
    output: TERNARY_INCOME_FILE
    shell: "python scripts/ternary_income.py {input} {output}"

rule ternary_geo:
    input: GEO_DATA, rules.prepare_ternary.output
    output: TERNARY_GEO_FILE
    shell: "python scripts/ternary_geo.py {input} {output}"


# Visualization: Ternary plots
rule plot_ternary_density:
    input: rules.prepare_ternary.output
    output: TERNARY_PLOT
    shell: "Rscript scripts/plot_ternary_density.R {input} {output}"


rule plot_ternary_temp_density:
    input: rules.prepare_ternary.output
    output: TERNARY_TEMP_DENSITY
    shell: "Rscript scripts/plot_ternary_temp_density.R {input} \"{wildcards.st}\" \"{wildcards.period}\" \"{output}\""

rule plot_ternary_evolution:
    input: TER_DATA
    output: TERNARY_TEMP_ALL
    shell: "Rscript scripts/plot_ternary_evolution.R {input} {output}"

rule plot_vectorfield:
    input: rules.prepare_ternary.output
    output: VECTOR_TERNARY
    shell: "python scripts/plot_vectorfield.py {input} {output}"

rule plot_ternary_income:
    input: TER_INCOME_DATA
    output: TERNARY_INCOME_PLOT
    shell: "Rscript scripts/plot_ternary_income.R {input} \"{wildcards.period}\" \"{output}\""

rule plot_reclassify_by_ternary:
    input: rules.reclassify_country_by_ternary.output
    output: TERNARY_CLASSIFY_BY_TERNARY_PLOT
    shell: "Rscript scripts/plot_reclassify_by_ternary.R {input} {output}"

rule plot_ternary_geo:
    input: rules.ternary_geo.output
    output: TERNARY_GEO_PLOT
    shell: "Rscript scripts/plot_ternary_geo.r {input} {output}"

rule plot_ternary_incomegroup:
    input: rules.ternary_income.output
    output: TERNARY_INCOME_GROUP_PLOT
    shell: "Rscript scripts/plot_ternary_incomegroup.r {input} {output}"

rule plot_ternary_density_incomegroup:
    input: TERNARY_INCOME_FILE
    output: TERNARY_INCOME_SINGLE
    shell: "Rscript scripts/plot_ternary_density_incomegroup.r {input} \"{wildcards.incomegroup}\" \"{wildcards.period}\" \"{output}\""

rule plot_ternary_individual:
    input: TER_DATA
    output:INDIVIDUAL_TRAGECTORY
    shell: "Rscript scripts/ternary_individual_trag.r {input} \"{wildcards.country}\" \"{output}\""

rule cal_ternary_increase:
    input: TER_DATA,CNTRY_YEAR_GDP
    output: TER_INCREASE
    shell: "python scripts/cal_ternary_increase.py {input} {output}"

rule plot_ternary_change:
    input: TER_INCREASE
    output: RESOURCE_PLOT, APPLIED_PLOT, SOCIAL_PLOT
    shell: "python scripts/plot_ternary_change.py {input} {output}"

rule plot_grouptransition:
    input: CNTRY_GROUP,CNTRY_YEAR_GDP,FLAG_TABLE
    output: GROUP_TRANSITION_PLOT
    shell: "python scripts/plot_grouptransition.py {input} {output}"

rule regress_ternarychange:
    input: TER_DATA,CNTRY_YEAR_GDP
    params: exog="log_income,net_change"
    output: TERREGRESSION_RA
    shell: "python scripts/ternarychange_regression.py {input} {params.exog} {output}"

rule plot_incometragectory:
    input: TERNARY_INCOME_FILE
    output: TERNARY_INCOME_TRAGECTORY
    shell: "Rscript scripts/plot_ternary_groupavg.R {input} {output}"
