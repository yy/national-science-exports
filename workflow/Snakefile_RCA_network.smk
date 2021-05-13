################################################################################
# Snakefile_RCA_network.smk
#
# Contains rules relating calculation, aggregation, analysis, and visualization
# of RCA data, both in the form of world maps and as a disciplinary network.
# Rules are roughly organized along the following sections:
#
# - Data Processing: RCA and Proximity
# - Data Processing: Aggregation
# - Visualization: RCA
# - Data Processing: Networks
# - Visualization: Networks
# - Null models: RCA Net transition probabilities
################################################################################


# Data Processing: RCA and Proximity
rule cal_rca:
    input:
        PUBCNT_CSVS,
    output:
        RCA_CSVS,
    shell:
        "python scripts/cal_rca.py {input} {output}"


rule cal_prox:
    input:
        RCA_PROX_CSVS,
    output:
        PROX_CSVS,
    shell:
        "python scripts/cal_prox.py {input} {output}"


rule cal_prox_snapshot:
    input:
        RCA_CSVS,
    output:
        PROX_PERIOD,
    shell:
        "python scripts/cal_prox.py {input} {output}"


# Replaced by the rule below (plot_prox_stability)
# rule cal_prox_similarity:
#     input:
#         PROX_CSVS,
#         PROX_PERIOD,
#     output:
#         PROX_SIMILARITY,
#     shell:
#         "python scripts/cal_prox_similarity.py {input} {output}"


# calculate the stability of the RCA-based proximity matrix and plot the correlation coeff.
rule plot_prox_stability:
    input:
        PROX_WHOLE_TIMEPERIOD_CSV,
    output:
        PROX_STABILITY_PLOT,
    shell:
        """
        papermill scripts/cal_prox_similarity.ipynb \
            scripts/outsputs/cal_prox_similarity.ipynb \
            -p prox_all {input} -p figure_file {output}
        """


# Data Processing: Aggregation
rule agg_rca:
    input:
        STTABLE,
        expand(RCA_CSVS, type=TYPES, period=PERIODS),
    params:
        RCA_TYPE,
    output:
        RCA_AGG,
    shell:
        "python scripts/agg_rca.py {params} {input[0]} {output}"


# Visualization: RCA
rule plot_rca:
    input:
        rules.agg_rca.output,
        FLAG_TABLE,
        SHP_FILE,
    output:
        directory(RCA_PLOT_DIR),
    shell:
        "python scripts/plot_rca.py {input} {output}"


rule plot_proxmatrix:
    input:
        PROX_CSVS,
    output:
        PROXMATRIX_PLOT,
    shell:
        "python scripts/plot_proxmatrix.py {input} {output}"


rule plot_nestedness:
    input:
        rules.cal_rca.output,
        LEIDEN_GROUP, #BACKBONE_DIR+expand("group_smb_{type}_alpha02_1973-2017.csv", type=TYPES)
         #expand("../data/dropbox/Data/Derived/Publication_based/Backbone/group_smb_{type}_alpha02_1973-2017.csv", type=TYPES)
    output:
        plot=NESTEDNESS_PLOT,
        mat=NESTEDNESS_MATRIX,
    shell:
        "python scripts/nestedness.py {input} {output.plot} {output.mat}"


rule cal_nestedness:
    input:
        rules.plot_nestedness.output.mat,
    output:
        NESTEDNESS_MEASURE,
    shell:
        "Rscript scripts/MeasureNestedness.R {input} {output}"


rule cal_nest_modu:
    input:
        rules.plot_nestedness.output.mat,
    output:
        NESTEDNESS_NULL,
    shell:
        "Rscript scripts/cal_nest_modu.r {input} {output}"


rule agg_NestModu:
    input:
        [expand(rules.cal_nest_modu.output, type="full", period=PERIODS)], #params: NESTEDNESS_NULL_DIR
    output:
        NESTEDNESS_NULL_AGG,
    shell:
        "python scripts/agg_NestModu.py {input} {output}"


rule cal_zscore_nestmodu:
    input:
        LEIDEN_GROUP,
        CNTRY_GROUP,
        RCA_AGG,
    output:
        FF_NESTMODU,
    shell:
        "python scripts/Null_NestModu.py {input} {output}"


rule plot_global_specialization:
    input:
        RCA_AGG,
        LEIDEN_GROUP,
        CNTRY_GROUP,
    output:
        GLOBAL_SPECIALIZATION_PLOT,
    shell:
        "python scripts/plot_global_specialization.py {input} {output}"


rule cal_modularity_by_adv:
    input:
        rules.agg_rca.output,
        rules.cal_prox.output,
    output:
        MODULARITY_INDIVIDUAL,
    shell:
        "python scripts/cal_modularity_by_adv.py {input} {output}"


rule cal_cc_by_adv:
    input:
        rules.agg_rca.output,
        rules.cal_prox.output,
    output:
        CLUSTERCOEFFIENCE_INDIVIDUAL,
    shell:
        "python scripts/cal_cc_by_adv.py {input} {output}"


rule plot_Bipartite_Nest_Modu_Evolution:
    input:
        FF_NESTMODU,
    output:
        NESTEDNESS_ZSCORE,
        MODULARITY_ZSCORE,
    shell:
        "python scripts/plot_Bipartite_Nest_Modu_Evolution.py {input} {output}"


rule plot_modularity_by_adv:
    input:
        MODULARITY_INDIVIDUAL,
        STTABLE,
    output:
        MODULARITY_PLOT,
    shell:
        "python scripts/plot_modularity_by_adv.py {input} {output}"


rule plot_cc_by_adv:
    input:
        CLUSTERCOEFFIENCE_INDIVIDUAL,
        STTABLE,
    output:
        CLUSTERCOEFFICIENT_PLOT,
    shell:
        "python scripts/plot_cc_by_adv.py {input} {output}"


# Data Processing: Networks


rule id2node:
    input:
        PUBCNT_FULL,
    output:
        ID2NODE,
    shell:
        "python scripts/id2node.py {input} {output}"


rule extract_backbone:
    input:
        rules.cal_prox.output,
    output:
        BACKBONES,
    shell:
        "python scripts/extract_backbone.py {input} {output}"


rule extract_backbone_period:
    input: PROX_PERIOD
    output:BACKBONES_PERIOD
    shell: "python scripts/extract_backbone.py {input} {output}"

rule edge2idlist:
    input:
        rules.cal_prox.output,
        rules.id2node.output,
    output:
        EDGETRANS,
    shell:
        "python scripts/edgelist2idlist.py {input} {output}"


# This rule is "phony". it just copies the files because the layout
# was done via Gephi.
rule create_graph_layout:
    input:
        GRAPHS_ORIG,
    output:
        GRAPHS,
    shell:
        "cp {input} {output}"


rule build_edge_file:
    input:
        GRAPHS,
        rules.extract_backbone.output,
    output:
        EDGE_FILES,
    shell:
        "Rscript scripts/BuildEdgeFile.R {input} {output}"


rule build_node_file:
    input:
        GRAPHS,
        PUBCNT_CSVS,
        rules.agg_rca.output,
        DISC_CLASSIFICATION,
    output:
        NODE_FILES,
    shell:
        "Rscript scripts/BuildNodeFile.R {input} {output}"


#
# If you do not have graph-tool installed, comment out this rule so that it
# is not run. Instead, place the pre-computed SBM outputs in the correct path so
# that other rules that depend on this output can be executed.
#
rule votingsbm:
    input:
        BACKBONES,
    output:
        GROUPS_SBM_BACKBONE,
        GROUPSSBM_DETAIL_BACKBONE,
    shell:
        "python scripts/votingsbm.py {input} {output}"


# Visualization: Networks
rule plot_whole_network_with_labels:
    input:
        rules.build_node_file.output,
        rules.build_edge_file.output,
    output:
        NETWORK_PLOTS_ALL_LABELED,
    shell:
        "Rscript scripts/PlotWholeNetworkWithLabels.R {input} {output}"


rule plot_country_year_network:
    input:
        rules.build_node_file.output,
        rules.build_edge_file.output,
    output:
        NETWORK_PLOTS_COUNTRY_YEAR, # Here the quotes around the wildcards and output are important. otherwise
         # spaces in filenames will not be parsed properly (i.e., in 'Sri Lanka').
    shell:
        'Rscript scripts/PlotCountryYearNetwork.R {input} "{wildcards.country}" "{wildcards.period}" "{output}"'


rule plot_sbm_network:
    input:
        rules.build_node_file.output,
        rules.build_edge_file.output,
        LEIDEN_GROUP,
    output:
        NETWORK_SBM_PLOT,
    shell:
        "Rscript scripts/PlotSBMNetwork.R {input} {output}"


# Null models: RCA Net transition probabilities
# calculate the transition trend over discipline development
rule cal_transition:
    input:
        rules.agg_rca.output,
        rules.cal_prox.output,
    output:
        DENSITY_AND_TIMEFLAG,
    shell:
        "python scripts/cal_transition.py {input} {output}"


# plot the activation and inactivation probability plot
rule plot_transition_p:
    input:
        rules.cal_transition.output,
    output:
        ACT_PROB_PLOTS,
        INACT_PROB_PLOTS,
        PROB_DIS_PLOTS,
    shell:
        "python scripts/plot_transition_p.py {input} {output}"


rule cal_grouprca:
    input:
        PUBCNT_CSVS,
        LEIDEN_GROUP,
        INTERVAL_FILE,
    output:
        CNTRY_GROUP,
    shell:
        "python scripts/cal_grouprca.py {input} {output}"



rule plot_stgroup_density2prob:
    input:
        DENSITY_AND_TIMEFLAG,
        STTABLE,
    output:
        ST_DENSITY2PROB_PLOT,
    shell:
        "python scripts/stgroup_density2prob.py {input} {output}"


rule plot_incomegroup_density2prob_all:
    input:
        DENSITY_AND_TIMEFLAG,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        INCOMEGROUP_DENSITY2PROB_ALL_PLOT,
        DENSITY2PROB_PARAMS,
    shell:
        "python scripts/incomegroup_density2prob_all.py {input} {output}"


rule proximity_null_all:
    input:
        expand(PROXIMITY_NULL, type="full", startyear=1973, endyear=2017),


rule proxmity_null:
    input:
        DENSITY_AND_TIMEFLAG,
        DENSITY2PROB_PARAMS,
        INTERVAL_FILE,
    output:
        PROXIMITY_NULL,
    shell:
        "python scripts/proximity_null.py {input} {output}"


rule plot_actual_null_ternary:
    input:
        PROXIMITY_NULL,
        LEIDEN_GROUP,
        TER_DATA,
        INTERVAL_FILE,
    output:
        TERNARY_ACTUAL_NULL_PLOT,
    shell:
        "python scripts/plot_actual_null_ternary.py {input} {output}"


rule plot_comparision_actual_null:
    input:
        PROXIMITY_NULL,
        DENSITY_AND_TIMEFLAG,
        LEIDEN_GROUP,
        CNTRY_GROUP,
    output:
        COMPARISION_ACTUAL_NULL_PLOT,
    shell:
        "python scripts/plot_actual_null_boxplot.py {input} {output}"

rule community_louvain:
    input:
        PROX_CSVS,
    output:
        LOUVAIN_GROUP,
    shell:
        "python scripts/community_louvain.py {input} {output}"


rule community_leiden:
    input:
        PROX_CSVS,
    output:
        LEIDEN_GROUP,
    shell:
        "python scripts/community_Leiden.py {input} {output}"


rule leiden_diff_countingmethod:
    input: LEIDEN_FULL,LEIDEN_FRAC,LEIDEN_CORR
    output:LEIDEN_COMPARISON
    shell:"python scripts/compare_counting.py {input} {output}"

rule community_infomap:
    input:
        PROX_CSVS,
    output:
        INFOMAP,
    shell:
        "python scripts/infomap.py {input} {output}"

rule leiden_period:
    input:PROX_PERIOD,LEIDEN_GROUP
    output: LEIDEN_PERIOD
    shell: "python scripts/community_Leiden_period.py {input} {output}"

rule leiden_whole_period_diff:
    input: LEIDEN_PERIOD
    output: LEIDEN_DIFF
    shell: "python scripts/leiden_whole_period.py {input} {output}"

"""
rule cal_nest_modu:
    input: rules.plot_nestedness.output.mat
    output: NESTEDNESS_NULL
    shell: "Rscript scripts/cal_nest_modu.r {input} {output}"

rule prepare_rca_regression_data:
    input:
        rules.agg_rca.output,
        LEIDEN_GROUP,
        CNTRY_YEAR_GDP,
        FLAG_TABLE,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        RCA_REGRESSION_DATA,
    shell:
        "python scripts/rca_regression_data.py {input} {output}"


rule run_rca_regression:
    input:
        RCA_REGRESSION_DATA,
    output:
        RCA_REGRESSION_RESULT,
    shell:
        "python scripts/rca_regression.py {input} {output}"


rule run_rca_regression_incomegroup:
    input:
        RCA_REGRESSION_DATA,
    output:
        RCA_REGRESSION_INCOMEGROUP,
    shell:
        "python scripts/rca_regression_incomegroup.py {input} {output}"



rule prepare_rca_regression_panel_data:
    input:
        rules.agg_rca.output,
        LEIDEN_GROUP,
        CNTRY_YEAR_GDP,
        FLAG_TABLE,
        CNTRY_YEAR_INCOMEGROUP,
    output:
        RCA_REGRESSION_PANEL_DATA,
    shell:
        "python scripts/rca_regression_panel_data.py {input} {output}"


rule rca_panel_regression:
    input:
        RCA_REGRESSION_PANEL_DATA,
    output:
        RCA_REGRESSION_PANEL_FE,
    shell:
        "python scripts/rca_regression_panel.py {input} {output}"


rule rca_panel_regression_incomegroup:
    input:
        RCA_REGRESSION_PANEL_DATA,
    output:
        RCA_REGRESSION_PANEL_INCOMEGROUP_FE,
    shell:
        "python scripts/rca_regression_panel_incomegroup.py {input} {output}"


rule rca_panel_regression_re:
    input:
        RCA_REGRESSION_PANEL_DATA,
    output:
        RCA_REGRESSION_PANEL_RE,
    shell:
        "python scripts/rca_regression_panel_re.py {input} {output}"


rule rca_panel_regression_incomegroup_re:
    input:
        RCA_REGRESSION_PANEL_DATA,
    output:
        RCA_REGRESSION_PANEL_INCOMEGROUP_RE,
    shell:
        "python scripts/rca_regression_panel_incomegroup_re.py {input} {output}"


"""
