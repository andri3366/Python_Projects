# Assignment 5
# National Address Registry

"""
---
title: 26W_CST2112 GA5 Load NAR
---
erDiagram

    ga5_raw {
        int id PK, UK
        varchar LOC_GUID
        varchar ADDR_GUID
        varchar APT_NO_LABEL
        varchar CIVIC_NO
        varchar CIVIC_NO_SUFFIX
        varchar OFFICIAL_STREET_NAME
        varchar OFFICIAL_STREET_TYPE
        varchar OFFICIAL_STREET_DIR
        varchar PROV_CODE
        varchar CSD_ENG_NAME
        varchar CSD_FRE_NAME
        varchar CSD_TYPE_ENG_CODE
        varchar CSD_TYPE_FRE_CODE
        varchar MAIL_STREET_NAME
        varchar MAIL_STREET_TYPE
        varchar MAIL_STREET_DIR
        varchar MAIL_MUN_NAME
        varchar MAIL_PROV_ABVN
        varchar MAIL_POSTAL_CODE
        varchar BG_DLS_LSD
        varchar BG_DLS_QTR
        varchar BG_DLS_SCTN
        varchar BG_DLS_TWNSHP
        varchar BG_DLS_RNG
        varchar BG_DLS_MRD
        varchar BG_X
        varchar BG_Y
        varchar BU_N_CIVIC_ADD
        varchar BU_USE
        varchar SOURCE_FILE 
    }

    ga5_master{
        int id PK, UK
        varchar LOC_GUID
        varchar ADDR_GUID
        varchar APT_NO_LABEL
        varchar CIVIC_NO
        int CIVIC_NO_SUFFIX FK
        varchar OFFICIAL_STREET_NAME
        int OFFICIAL_STREET_TYPE FK
        int OFFICIAL_STREET_DIR FK
        varchar PROV_CODE
        varchar CSD_ENG_NAME
        varchar CSD_FRE_NAME
        int CSD_TYPE_ENG_CODE FK
        int CSD_TYPE_FRE_CODE FK
        varchar MAIL_STREET_NAME
        varchar MAIL_STREET_TYPE
        int MAIL_STREET_DIR FK
        varchar MAIL_MUN_NAME
        int MAIL_PROV_ABVN FK
        varchar MAIL_POSTAL_CODE
        varchar BG_DLS_LSD
        varchar BG_DLS_QTR
        varchar BG_DLS_SCTN
        varchar BG_DLS_TWNSHP
        varchar BG_DLS_RNG
        varchar BG_DLS_MRD
        varchar BG_X
        varchar BG_Y
        varchar BU_N_CIVIC_ADD
        varchar BU_USE
        int SOURCE_FILE FK
    }

    ga5_lookup_info{
        integer id_column PK,UK
        string code1 FK "code1+code2"
        string code2 FK "code1+code2"
        string descr
    }
    
    ga5_master ||--o{ ga5_lookup_info : "" 
"""

import os
import csv
import pyodbc
import pandas as pd
import glob
from hidden_code import uid, driver, server, database, pwd

conn = pyodbc.connect(
    Driver=driver,
    Server=server,
    Database=database,
    UID=uid,
    PWD=pwd
)
cur = conn.cursor()


# prepare RAW table

print("Reset RAW table")
cur.execute('DROP TABLE IF EXISTS ga5_raw;')
conn.commit()

sql = """
CREATE TABLE ga5_raw (
    id int primary key,
    LOC_GUID VARCHAR(300),
    ADDR_GUID VARCHAR(300),
    APT_NO_LABEL VARCHAR(300),
    CIVIC_NO VARCHAR(300),
    CIVIC_NO_SUFFIX VARCHAR(300),
    OFFICIAL_STREET_NAME VARCHAR(300),
    OFFICIAL_STREET_TYPE VARCHAR(300),
    OFFICIAL_STREET_DIR VARCHAR(300),
    PROV_CODE VARCHAR(300),
    CSD_ENG_NAME VARCHAR(300),
    CSD_FRE_NAME VARCHAR(300),
    CSD_TYPE_ENG_CODE VARCHAR(300),
    CSD_TYPE_FRE_CODE VARCHAR(300),
    MAIL_STREET_NAME VARCHAR(300),
    MAIL_STREET_TYPE VARCHAR(300),
    MAIL_STREET_DIR VARCHAR(300),
    MAIL_MUN_NAME VARCHAR(300),
    MAIL_PROV_ABVN VARCHAR(300),
    MAIL_POSTAL_CODE VARCHAR(300),
    BG_DLS_LSD VARCHAR(300),
    BG_DLS_QTR VARCHAR(300),
    BG_DLS_SCTN VARCHAR(300),
    BG_DLS_TWNSHP VARCHAR(300),
    BG_DLS_RNG VARCHAR(300),
    BG_DLS_MRD VARCHAR(300),
    BG_X VARCHAR(300),
    BG_Y VARCHAR(300),
    BU_N_CIVIC_ADD VARCHAR(300),
    BU_USE VARCHAR(300),
    SOURCE_FILE VARCHAR(300)
);
"""
cur.execute(sql)
conn.commit()

# prepare master table
print("Reset Master table")
cur.execute('DROP TABLE IF EXISTS ga5_master;')
conn.commit()

sql = """
    CREATE TABLE ga5_master (
        id_column int primary key,
        LOC_GUID VARCHAR(300),
        ADDR_GUID VARCHAR(300),
        APT_NO_LABEL VARCHAR(300),
        CIVIC_NO VARCHAR(300),
        CIVIC_NO_SUFFIX int,
        OFFICIAL_STREET_NAME VARCHAR(300),
        OFFICIAL_STREET_TYPE int,
        OFFICIAL_STREET_DIR int,
        PROV_CODE int,
        CSD_ENG_NAME VARCHAR(300),
        CSD_FRE_NAME VARCHAR(300),
        CSD_TYPE_ENG_CODE int,
        CSD_TYPE_FRE_CODE int,
        MAIL_STREET_NAME VARCHAR(300),
        MAIL_STREET_TYPE VARCHAR(300),
        MAIL_STREET_DIR int,
        MAIL_MUN_NAME VARCHAR(300),
        MAIL_PROV_ABVN int,
        MAIL_POSTAL_CODE VARCHAR(300),
        BG_DLS_LSD VARCHAR(300),
        BG_DLS_QTR VARCHAR(300),
        BG_DLS_SCTN VARCHAR(300),
        BG_DLS_TWNSHP VARCHAR(300),
        BG_DLS_RNG VARCHAR(300),
        BG_DLS_MRD VARCHAR(300),
        BG_X VARCHAR(300),
        BG_Y VARCHAR(300),
        BU_N_CIVIC_ADD VARCHAR(300),
        BU_USE int,
        SOURCE_FILE int
    );
"""
cur.execute(sql)
conn.commit()

# prepare Lookup table
print("Reset Lookup Table")
cur.execute('DROP TABLE IF EXISTS ga5_lookup_info;')
conn.commit()

sql = """
    CREATE TABLE ga5_lookup_info (
    lookup_id integer not null identity(1,1) primary key,
    code1 varchar(100),
    code2 varchar(100),
    descr varchar(200)
    );
"""
cur.execute(sql)
conn.commit()

# helper function for loading data
def pushlist(cur,sql,data):
    
    element = 0   
    rows = ''
    comma = ''    
    
    for row in data:
    
        values = "('" + "','".join(str(val).replace("'", "`" ) for val in row) + "')"
        rows = rows + comma + values
        comma = ','
        element += 1
        
        if element > 999:
        
            element = 0
            cur.execute(sql + ' ' + rows)
            cur.commit()
            rows = ''
            comma = ''
            
    if rows != '':
        cur.execute(sql + ' ' + rows)
        cur.commit()

# load raw data
root_folder = "C:/cst2112_data/ga5/"
file = root_folder + "combined_source_with_id.csv"

with open(file, 'r', encoding='utf-8') as f:

    data = csv.reader(f, delimiter='|')
    
    # f.seek(0)
    next(data)

    sql = """
        insert into ga5_raw(
            id,
            LOC_GUID,
            ADDR_GUID,
            APT_NO_LABEL,
            CIVIC_NO,
            CIVIC_NO_SUFFIX,
            OFFICIAL_STREET_NAME,
            OFFICIAL_STREET_TYPE,
            OFFICIAL_STREET_DIR,
            PROV_CODE,
            CSD_ENG_NAME,
            CSD_FRE_NAME,
            CSD_TYPE_ENG_CODE,
            CSD_TYPE_FRE_CODE,
            MAIL_STREET_NAME,
            MAIL_STREET_TYPE,
            MAIL_STREET_DIR,
            MAIL_MUN_NAME,
            MAIL_PROV_ABVN,
            MAIL_POSTAL_CODE,
            BG_DLS_LSD,
            BG_DLS_QTR,
            BG_DLS_SCTN,
            BG_DLS_TWNSHP,
            BG_DLS_RNG,
            BG_DLS_MRD,
            BG_X,
            BG_Y,
            BU_N_CIVIC_ADD, 
            BU_USE,
            SOURCE_FILE
        ) VALUES
    """

    batch = []
    batch_size = 1000
    rows_loaded = 0
    # batch_count = 0

    for row in data:
        batch.append(row)

        if len(batch) == batch_size:
            pushlist(cur, sql, batch)
            rows_loaded += batch_size
            print("Loaded: ", rows_loaded)
            batch = []
            # batch_count += 1

            # if batch_count == 8:
            #     break

    # insert remaining rows
    if batch:
        pushlist(cur, sql, batch)

print('Loaded raw table')

# Tuncate reference tables
sql = """
TRUNCATE TABLE ga5_lookup_info;

-- CIVIC_NO_SUFFIC
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'civic_no_suffix'
	,row_number() over(order by civic_no_suffix asc)
    ,r.civic_no_suffix
FROM ga5_raw r
GROUP BY r.civic_no_suffix;

-- OFFICIAL_STREET_TYPE
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'official_street_type'
	,row_number() over(order by official_street_type asc)
    ,r.official_street_type
FROM ga5_raw r
GROUP BY r.official_street_type;

-- OFFICIAL_STREET_DIR
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'official_street_dir'
	,row_number() over(order by official_street_dir asc)
    ,r.official_street_dir
FROM ga5_raw r
GROUP BY r.official_street_dir;

-- CSD_TYPE_ENG_CODE
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'csd_type_eng_code'
	,row_number() over(order by csd_type_eng_code asc)
    ,r.csd_type_eng_code
FROM ga5_raw r
GROUP BY r.csd_type_eng_code;

-- CSD_TYPE_FRE_CODE
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'csd_type_fre_code'
	,row_number() over(order by csd_type_fre_code asc)
    ,r.csd_type_fre_code
FROM ga5_raw r
GROUP BY r.csd_type_fre_code;


-- MAIL_STREET_DIR
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'mail_street_dir'
	,row_number() over(order by mail_street_dir asc)
    ,r.mail_street_dir
FROM ga5_raw r
GROUP BY r.mail_street_dir;

-- MAIL_PROV_ABVN
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'mail_prov_abvn'
	,row_number() over(order by mail_prov_abvn asc)
    ,r.mail_prov_abvn
FROM ga5_raw r
GROUP BY r.mail_prov_abvn;

-- SOURCE_FILE
INSERT INTO ga5_lookup_info
	(code1,code2,descr)
SELECT 
	'source_file'
	,row_number() over(order by source_file asc)
    ,r.source_file
FROM ga5_raw r
GROUP BY r.source_file;
"""
cur.execute(sql)
conn.commit()

sql = """
truncate table ga5_master;
insert into ga5_master (
            id_column,
            LOC_GUID,
            ADDR_GUID,
            APT_NO_LABEL,
            CIVIC_NO,
            CIVIC_NO_SUFFIX,
            OFFICIAL_STREET_NAME,
            OFFICIAL_STREET_TYPE,
            OFFICIAL_STREET_DIR,
            PROV_CODE,
            CSD_ENG_NAME,
            CSD_FRE_NAME,
            CSD_TYPE_ENG_CODE,
            CSD_TYPE_FRE_CODE,
            MAIL_STREET_NAME,
            MAIL_STREET_TYPE,
            MAIL_STREET_DIR,
            MAIL_MUN_NAME,
            MAIL_PROV_ABVN,
            MAIL_POSTAL_CODE,
            BG_DLS_LSD,
            BG_DLS_QTR,
            BG_DLS_SCTN,
            BG_DLS_TWNSHP,
            BG_DLS_RNG,
            BG_DLS_MRD,
            BG_X,
            BG_Y,
            BU_N_CIVIC_ADD, 
            BU_USE,
            SOURCE_FILE
)

select
    r.id,
    r.LOC_GUID,
    r.ADDR_GUID,
    r.APT_NO_LABEL,
    r.CIVIC_NO,
    l_suffix.code2,
    r.OFFICIAL_STREET_NAME,
    l_off_st_type.code2,
    l_off_st_dir.code2,
    r.PROV_CODE,
    r.CSD_ENG_NAME,
    r.CSD_FRE_NAME,
    l_eng_code.code2,
    l_fre_code.code2,
    r.MAIL_STREET_NAME,
    r.MAIL_STREET_TYPE,
    l_mail_st_dir.code2,
    r.MAIL_MUN_NAME,
    l_mail_prov_abvn.code2,
    r.MAIL_POSTAL_CODE,
    r.BG_DLS_LSD,
    r.BG_DLS_QTR,
    r.BG_DLS_SCTN,
    r.BG_DLS_TWNSHP,
    r.BG_DLS_RNG,
    r.BG_DLS_MRD,
    r.BG_X,
    r.BG_Y,
    r.BU_N_CIVIC_ADD,
    r.BU_USE,
    l_s_f.code2

FROM ga5_raw r

LEFT JOIN ga5_lookup_info l_suffix 
    ON l_suffix.code1 = 'civic_no_suffix' 
    AND l_suffix.descr = r.CIVIC_NO_SUFFIX

LEFT JOIN ga5_lookup_info l_off_st_type 
    ON l_off_st_type.code1 = 'official_street_type' 
    AND l_off_st_type.descr = r.OFFICIAL_STREET_TYPE

LEFT JOIN ga5_lookup_info l_off_st_dir 
    ON l_off_st_dir.code1 = 'official_street_dir' 
    AND l_off_st_dir.descr = r.OFFICIAL_STREET_DIR

LEFT JOIN ga5_lookup_info l_eng_code
    ON l_eng_code.code1 = 'csd_type_eng_code' 
    AND l_eng_code.descr = r.CSD_TYPE_ENG_CODE

LEFT JOIN ga5_lookup_info l_fre_code 
    ON l_fre_code.code1 = 'csd_type_fre_code' 
    AND l_fre_code.descr = r.CSD_TYPE_FRE_CODE

LEFT JOIN ga5_lookup_info l_mail_st_dir 
    ON l_mail_st_dir.code1 = 'mail_street_dir' 
    AND l_mail_st_dir.descr = r.MAIL_STREET_DIR

LEFT JOIN ga5_lookup_info l_mail_prov_abvn
    ON l_mail_prov_abvn.code1 = 'mail_prov_abvn' 
    AND l_mail_prov_abvn.descr = r.MAIL_PROV_ABVN

LEFT JOIN ga5_lookup_info l_s_f
    ON l_s_f.code1 = 'source_file' 
    AND l_s_f.descr = r.SOURCE_FILE
"""

cur.execute(sql)
conn.commit()

# close the connection
cur.close()
conn.close()

# sample code for testing
'''
SELECT TOP 10
    m.id_column,
    m.LOC_GUID,
    m.ADDR_GUID,
    m.CIVIC_NO,
    m.OFFICIAL_STREET_NAME,

    l_suffix.descr       AS civic_no_suffix,
    l_st_type.descr      AS official_street_type,

    m.MAIL_MUN_NAME,
    m.MAIL_POSTAL_CODE,

    l_s_f.descr          AS source_file

FROM dbo.ga5_master m

LEFT JOIN dbo.ga5_lookup_info l_suffix
    ON l_suffix.code1 = 'civic_no_suffix'
    AND l_suffix.code2 = m.CIVIC_NO_SUFFIX

LEFT JOIN dbo.ga5_lookup_info l_st_type
    ON l_st_type.code1 = 'official_street_type'
    AND l_st_type.code2 = m.OFFICIAL_STREET_TYPE

LEFT JOIN dbo.ga5_lookup_info l_s_f
    ON l_s_f.code1 = 'source_file'
    AND l_s_f.code2 = m.SOURCE_FILE

ORDER BY m.id_column;
'''

# <-------- Pre-Analysis --------->

# get sample of all files

# input_folder = "c:/cst2112_data/ga5/data/Addresses"
# output_folder = "c:/cst2112_data/ga5/sample_data"
# os.makedirs(output_folder, exist_ok= True)

# csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

# get sample amount of rows in each data file for analysis
# csv_file = "combined_source_with_id.csv"
# sample_df = pd.read_csv(csv_file, nrows=100)
# base_name = os.path.basename(csv_file)
# output_file = os.path.join(output_folder, f"sample_{base_name}")

# sample_df.to_csv(output_file, index=True)

# print(f"Saved sample: {output_file}")
# for file in csv_files:
#     sample_df = pd.read_csv(file, nrows=100)
#     base_name = os.path.basename(file)
#     output_file = os.path.join(output_folder, f"sample_{base_name}")

#     sample_df.to_csv(output_file, index=True)

#     print(f"Saved sample: {output_file}")

# input_file = r"C:\cst2112_data\ga5\combined_source_split.csv"
# output_file = r"C:\cst2112_data\ga5\combined_source_with_id.csv"

# with open(input_file, "r", encoding="utf-8", newline="") as infile, \
#      open(output_file, "w", encoding="utf-8", newline="") as outfile:

#     reader = csv.reader(infile, delimiter="|")
#     writer = csv.writer(outfile, delimiter="|")

#     # Read original header
#     header = next(reader)

#     # Write new header with id column first
#     writer.writerow(["id"] + header)

#     # Write rows with index starting at 1
#     for i, row in enumerate(reader, start=1):
#         writer.writerow([i] + row)

#         # optional progress indicator for huge files
#         if i % 1000000 == 0:
#             print(f"{i} rows processed")

# check if the headers in each data file match
# reference = pd.read_csv(csv_files[0], nrows=0).columns.tolist()

# for file in csv_files:
#     header = pd.read_csv(file, nrows=0).columns.tolist()

#     if header != reference:
#         print(f"header mismatch in: {file}")

#         missing = set(reference) - set(header)
#         extra = set(header) - set(reference)

#         print("Missing cols: ", missing)
#         print("Extra cols: ", extra)

# print("Header check complete")

# combine all data files into one large file
# output_file = "combined_source_split.csv"
# first = True

# for file in csv_files:

#     filename = os.path.basename(file)

#     for chunk in pd.read_csv(file, chunksize=10000):
#         chunk["SOURCE_FILE"] = filename
#         chunk.to_csv(output_file, mode="a", index=False, header=first, sep="|")
#         first = False

# print("All files combined!")

# get row count of the data and combined data to find a match
# total_rows = 0

# for file in csv_files:
#     with open(file, "r", encoding="utf-8") as f:
#         row_count = sum(1 for line in f) - 1
#     print(f"{file} : {row_count} rows")
#     total_rows += row_count

# print("Total rows: ", total_rows)

# with open("combined_source_with_id.csv", "r", encoding="utf-8") as f:
#     combined_rows = sum(1 for line in f) - 1

# print("combined_source_with_id.csv rows", combined_rows)

# if combined_rows == total_rows:
#     print("match")
# else:
#     print("no match")

# get data types, unique values, and null counts from the dataset
# file = "combined_source.csv"
# chunksize = 100000

# stats = {}
# total_rows = 0
# dtypes = None
# for chunk in pd.read_csv(file, chunksize=chunksize, dtype=str):

#     if dtypes is None:
#         dtypes = chunk.dtypes

#     total_rows += len(chunk)

#     for col in chunk.columns:

#         if col not in stats:
#             stats[col] = {
#                 "unique": set(),
#                 "nulls": 0
#             }

#         stats[col]["unique"].update(chunk[col].dropna().unique())
#         stats[col]["nulls"] += chunk[col].isna().sum()

# print(f"{'COLUMN':25} {'DTYPE':10} {'UNIQUE':10} {'NULLS':10} {'NULL %':10}")

# for col in stats:
#     unique_count = len(stats[col]["unique"])
#     null_count = stats[col]["nulls"]
#     null_pct = (null_count / total_rows) * 100

#     print(f"{col:25} {str(dtypes[col]):10} {unique_count:<10} {null_count:<10} {null_pct:.2f}")

# COLUMN                    DTYPE      UNIQUE     NULLS      NULL %
# LOC_GUID                  str        11772719   0          0.00
# ADDR_GUID                 str        17338205   0          0.00
# APT_NO_LABEL              str        28578      11375806   65.61
# CIVIC_NO                  str        124116     92         0.00
# CIVIC_NO_SUFFIX           str        29         17128477   98.79
# OFFICIAL_STREET_NAME      str        117817     93         0.00
# OFFICIAL_STREET_TYPE      str        174        301986     1.74
# OFFICIAL_STREET_DIR       str        11         14709381   84.84
# PROV_CODE                 str        13         0          0.00
# CSD_ENG_NAME              str        4045       15653      0.09
# CSD_FRE_NAME              str        4045       15653      0.09
# CSD_TYPE_ENG_CODE         str        51         15653      0.09
# CSD_TYPE_FRE_CODE         str        51         15653      0.09
# MAIL_STREET_NAME          str        104913     962383     5.55
# MAIL_STREET_TYPE          str        154        1363884    7.87
# MAIL_STREET_DIR           str        11         14822874   85.49
# MAIL_MUN_NAME             str        7548       40020      0.23
# MAIL_PROV_ABVN            str        13         12631      0.07
# MAIL_POSTAL_CODE          str        853955     58228      0.34
# BG_DLS_LSD                str        0          17338205   100.00
# BG_DLS_QTR                str        4          14971187   86.35
# BG_DLS_SCTN               str        36         14971187   86.35
# BG_DLS_TWNSHP             str        98         14971187   86.35
# BG_DLS_RNG                str        31         14971187   86.35
# BG_DLS_MRD                str        7          14971187   86.35
# BG_X                      str        9974964    1215861    7.01
# BG_Y                      str        9976719    1215861    7.01
# BU_N_CIVIC_ADD            str        8455       16607576   95.79
# BU_USE                    str        4          0          0.00
# SOURCE_FILE               str        28         0          0.00