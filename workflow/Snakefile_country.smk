################################################################################
# Snakefile_country.smk
#
# Contains rules relating the creating of miscellaneous country-level data and
# plots and which are not directly related to the RCA, Ternary, or GINI analyses
################################################################################

rule aggregate_country_data:
    input: rules.build_node_file.output,
           GROUPS_SBM,
           INCOME_FILE,
           ECI_FILE,
           TER_DATA,
           GINI_AGG.format(norm = "Raw", type = "{type}"),
           GINI_AGG.format(norm = "normalized", type = "{type}"),
           FLAG_TABLE
    output: COUNTRY_AGGREGATED_CSV
    shell: "Rscript scripts/AggregateAllCountryData.R {input} {output}"

rule plot_gdp_against_specialization:
    input: COUNTRY_AGGREGATED_CSV.format(type = '{type}', alpha = '{alpha}', startyear = 1973, endyear = 2017)
    output: GDP_SPECIALIZATION_PLOTS
    shell: "Rscript scripts/PlotGDPAgainstSpec.R {input} \"{wildcards.sbm}\" \"{wildcards.period}\" {output}"
