rule cal_similarity:
    input:
        DENSITY_AND_TIMEFLAG,
    output:
        SIMILARITY,
    shell: "python scripts/cal_dissimilarity.py {input} {output}"

rule prepare_regression_data:
    input:
        cntry_year_gdp=CNTRY_YEAR_GDP,
        flag_df=FLAG_TABLE,
        gini=rules.agg_gini.output,
        pub=PUBCNT_CSVS,
        group=LEIDEN_GROUP,
        sim=SIMILARITY,
        eci=ECI_FILE,
    output:
        REG_DATA,
    shell:
        """
        papermill scripts/regression_data.ipynb \
            scripts/outputs/regression_data.ipynb \
            -p income_df_path {input.cntry_year_gdp} \
            -p flag_df_path {input.flag_df} \
            -p gini_df_path {input.gini} \
            -p pub_cnt_path {input.pub} \
            -p dscp_df_path {input.group} \
            -p dissim_df_path {input.sim} \
            -p eci_df_path {input.eci} \
            -p meta_output_path {output[0]}
        """
