################################################################################
# Snakefile_dataprocessing.smk
#
# Contains rules relating to the initial processing and formatting of all
# variations of raw data files, the first step of the NSP data pipeline.
################################################################################

rule convert_raw_excel_to_csv:
    input: RAW_XLSXS
    output: RAW_CSVS
    shell: "python scripts/convert_raw_xls_to_csv.py {input} {output}"

rule consolidate_country_changes:
    input: RAW_CSVS, COUNTRY_CONSOLIDATION_FILE
    output: PUBCNT_CSVS
    shell: "python scripts/raw_data_cleaning.py {input} {output}"

rule extract_pubtotal_by_year:
    input: PUBCNT_DIS_CSV
    output: PUBCNT_GLOBAL_CSV
    shell: "python scripts/extract_pubtotal.py {input} {output}"

rule extract_pubtotal_by_disciplines:
    input: PUBCNT_FULL
    output: PUBCNT_DIS_CSV
    shell: "python scripts/extract_dis_total.py {input} {output}"

rule cntry_year_incomegroup:
    input: INCOME_GROUP, INTERVAL_FILE, FLAG_TABLE
    output: CNTRY_YEAR_INCOMEGROUP
    shell: "python scripts/extract_cntry_year_incomegroup.py {input} {output}"

rule cntry_year_incomevalue:
    input: INCOME_FILE, INTERVAL_FILE
    output: CNTRY_YEAR_INCOMEVALUE
    shell: "python scripts/convert_WB_cntrylevel.py {input} {output}"

rule cntry_year_gdp:
    input: GDP_WB_FILE, INTERVAL_FILE
    output: CNTRY_YEAR_GDP
    shell: "python scripts/convert_WB_cntrylevel.py {input} {output}"
