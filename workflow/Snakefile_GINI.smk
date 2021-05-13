################################################################################
# Snakefile_GINI.smk
#
# Contains rules relating calculation, aggregation, analysis, and visualization
# of the GINI data for each country and time period. Rules are roughly organized
# along the following sections:
#
# - Data Processing: GINI
# - Data Processing: GINI Bootstrap
# - Regression: GINI
# - Visualization: Gini
################################################################################


# Data Processing: GINI
rule cal_gini:
    input:
        PUBCNT_CSVS,
    output:
        GINI_RAW_CSVS,
    shell:
        "python scripts/cal_gini.py {input} {output}"


rule cal_gini_norm:
    input:
        PUBCNT_CSVS,
    output:
        GINI_NORM_CSVS,
    shell:
        "python scripts/cal_gini_norm.py {input} {output}"


rule agg_gini:
    input:
        STTABLE,
        expand(GINI_RAW_CSVS, type=TYPES, period=PERIODS),
        expand(GINI_NORM_CSVS, type=TYPES, period=PERIODS),
    params:
        GINI_TYPE,
    output:
        GINI_AGG,
    shell:
        "python scripts/agg_gini.py {params} {input[0]} {output}"


# Data Processing: GINI Bootstrap
rule gini_resampling:
    input:
        rules.consolidate_country_changes.output, #params: PERIODS[:-1]
    output:
        BOOT_CSVS,
    shell:
        "python scripts/gini_resampling.py {input} {output}"



rule agg_bootstrap_gini:
    input:
        STTABLE,
    params:
        BOOT_GINI_PATH,
    output:
        AGG_GINI_BOOT,
    shell:
        "python scripts/agg_gini.py {params} {input} {output}"



# Visualization: Gini
rule plot_corr_gini_eci_income:
    input:
        GINI_CSVS,
        ECI_FILE,
        CNTRY_YEAR_GDP,
        FLAG_TABLE,
        PUBCNT_CSVS,
    output:
        GINI_ECI,
        GINI_INCOME,
        INCOME_ECI,
        PUBCNT_GINI_PLOT,
        PUBCNT_INCOME_PLOT,
        PUBCNT_ECI_PLOT,
    shell:
        "python scripts/plot_corr_gini_eci_income.py {input} {output}"


rule plot_gini_st_time:
    input:
        rules.agg_gini.output,
    output:
        GINI_ST_PLOT,
    shell:
        "python scripts/plot_gini_st_time.py {input} {output}"


rule worldmaps:
    input:
        expand(GINI_WORLDMAP, norm=NORMS, type=TYPES, period=PERIODS),


rule plot_gini_worldmap:
    input:
        GINI_CSVS,
        FLAG_TABLE,
        SHP_FILE,
    output:
        GINI_WORLDMAP,
    shell:
        """
        papermill scripts/plot_gini_worldmap.ipynb \
            scripts/outputs/plot_gini_worldmap.ipynb \
            -p GINI_FILE {input[0]} \
            -p FLAG_TABLE {input[1]} \
            -p WORLD_GEO {input[2]} \
            -p PLOT_PATH {output}
        """ # "python scripts/plot_gini_worldmap.py {input} {output}"


rule plot_gini_sample_actual:
    input:
        GINI_RAW_FULL,
        rules.gini_resampling.output,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        SAMPLED_ACTUAL_PLOT,
    shell:
        "python scripts/plot_sample_actual.py {input} {output}"


rule plot_gini_income_time:
    input:
        rules.agg_gini.output,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        INCOMEGROUP_GINI,
    shell:
        "python scripts/plot_gini_income_time.py {input} {output}"


rule plot_adv_num:
    input:
        RCA_AGG,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        INCOMEGROUP_ADVNUM,
    shell:
        "python scripts/plot_adv_num.py {input} {output}"


rule plot_income_diversity_flow:
    input:
        rules.agg_gini.output,
        CNTRY_YEAR_GDP,
        FLAG_TABLE,
        INTERVAL_FILE,
    output:
        GDP_DIVERSITY_FLOW_PLOT,
    shell:
        """
        papermill scripts/plot_income_diversity_flow.ipynb \
            scripts/outputs/plot_income_diversity_flow.ipynb \
            -p GINI_FILE {input[0]} \
            -p INCOME_FILE {input[1]} \
            -p CNTRY_CODES {input[2]} \
            -p PERIODS_FILE {input[3]} \
            -p PLOT_FILE {output}
        """

'''
# Regression: GINI
rule prepare_reg_table:
    input:
        rules.agg_gini.output,
        ECI_FILE,
        CNTRY_YEAR_GDP,
        FLAG_TABLE,
        INTERVAL_FILE,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        REG_TABLE,
    shell:
        "python scripts/prepare_reg_table.py {input} {output}"


rule run_reg_gini:
    input:
        rules.prepare_reg_table.output,
    output:
        REG1_RESULT,
        REG2_RESULT,
        REG3_RESULT,
    shell:
        "python scripts/run_reg_gini.py {input} {output}"


rule run_reg_gini_incomegroup:
    input:
        rules.prepare_reg_table.output,
    output:
        REG_GINI_INCOMEGROUP,
    shell:
        "python scripts/run_reg_gini_incomegroup.py {input} {output}"


rule run_reg_gini_re:
    input:
        rules.prepare_reg_table.output,
    output:
        REG1_RESULT_RE,
        REG2_RESULT_RE,
        REG3_RESULT_RE,
    shell:
        "python scripts/run_reg_gini_re.py {input} {output}"


rule run_reg_gini_incomegroup_re:
    input:
        rules.prepare_reg_table.output,
    output:
        REG_GINI_INCOMEGROUP_RE,
    shell:
        "python scripts/run_reg_gini_incomegroup_re.py {input} {output}"
'''
