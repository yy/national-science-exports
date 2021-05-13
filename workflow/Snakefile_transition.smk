'''rule transition_plot:
    input:
        density=expand(DENSITY_AND_TIMEFLAG, type="full", startyear=1973, endyear=2017),
        income_group=CNTRY_YEAR_INCOMEGROUP,
    params:
        ensembles=20,
    output:
        dens2prob=expand(DENSITY2PROB_PARAMS, type="full", startyear=1973, endyear=2017),
        plot=TRANSITION_PLOT,
    shell:
        """
        papermill scripts/incomegroup_density2prob.ipynb \
            scripts/outputs/incomegroup_density2prob.ipynb \
            -p N_ENSEMBLES {params.ensembles} \
            -p DENSITY_FILE {input.density} \
            -p INCOME_GROUP_FILE {input.income_group} \
            -p DENSITY2PROB_PARAMS {output.dens2prob} \
            -p FIGURE_PATH {output.plot}
        """
'''
