# Algonquin College BISI Program
# Image File Metadata

# Mermaid code
# Mermaid code creator link: https://mermaid.live/
'''
---
title: 26W_CST2112 Group Assignment 3 - Image File Metadata
---
erDiagram

    ga3_raw{
      integer id_column PK,UK
      string filename
      string file_path
      int file_size
      string camera_make
      string camera_model
      string datetime_original
      string exif_metadata
      string iptc_metadata
      string xmp_metadata
    }

    ga3_master{
        integer image_id PK,UK,FK
        string filename
        string file_path
        int file_size
        datetime datetime_original
        camera_make int fk
        camera_model int fk
    }

    ga3_metadata{
        integer image_tag_id PK,UK
        int image_id FK
        string metadata_type
        string metadata_name
        string metadata_subname
        string metadata_value
    }

    ga3_camera_lookup{
        integer lookup_id PK,UK
        string code1 fk "code1+code2"
        int code2 fk "code1+code2"
        string description
    }
    
    ga3_master ||--|{ ga3_metadata : ""
    ga3_master ||--o{ ga3_camera_lookup : "" 
'''
# Imports

import os
# import csv
import pyodbc
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import iptcinfo3
from hidden_code import driver, server, database, uid, pwd

# Connect to SQL Server
conn = pyodbc.connect(
    Driver=driver,
    Server=server,
    Database=database,
    UID=uid,
    PWD=pwd
)
cur = conn.cursor()

# Create Raw Table
print("Creating RAW table....")
cur.execute('DROP TABLE IF EXISTS ga3_raw;')
conn.commit()

sql = """
    CREATE TABLE ga3_raw (
        id_column int identity(1,1) primary key,
        filename varchar(500),
        file_path varchar(500),
        file_size int,
        camera_make VARCHAR(200),
        camera_model VARCHAR(200),
        datetime_original VARCHAR(100),
        exif_metadata VARCHAR(MAX),
        iptc_metadata VARCHAR(MAX),
        xmp_metadata VARCHAR(MAX)
    );
"""
cur.execute(sql)
conn.commit()

# Create metadata table
print("Creating Metadata Table....")
cur.execute('DROP TABLE IF EXISTS ga3_metadata')
conn.commit()

sql = """
    CREATE TABLE ga3_metadata(
        image_tag_id int identity(1,1) primary key,
        image_id int not null,
        metadata_type VARCHAR(5) not null,
        metadata_name VARCHAR(200) not null,
        metadata_subname VARCHAR(200),
        metadata_value VARCHAR(MAX)
    );
"""
cur.execute(sql)
conn.commit()

# Create master Table
print("Creating Master Table....")
cur.execute('DROP TABLE IF EXISTS ga3_master')
conn.commit()

sql = """
    CREATE TABLE ga3_master (
        image_id int identity(1,1) primary key,
        filename VARCHAR(MAX),
        file_path VARCHAR(MAX),
        file_size INT,
        datetime_original DATETIME,
        camera_make int,
        camera_model int
    );
"""

cur.execute(sql)
conn.commit()

# Create camera lookup table
print("Creating Camera Lookup Table")
cur.execute('DROP TABLE IF EXISTS ga3_camera_lookup')
conn.commit()

sql = """
    CREATE TABLE ga3_camera_lookup (
        lookup_id int identity(1,1) primary key,
        code1 VARCHAR(50),
        code2 VARCHAR(50),
        description VARCHAR(100),
        constraint uq_lookup unique(code1, code2)
    );
"""
cur.execute(sql)
conn.commit()

print("All tables created successfully!")

# Extract metadata

def stringify_metadata(data):

    if isinstance(data, dict):
        return {str(k): stringify_metadata(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [stringify_metadata(v) for v in data]
    elif isinstance(data, bytes):
        return repr(data)   
    else:
        return str(data)
    
def flatten_dict(data, parent_key=''):
    items = []

    if isinstance(data, dict):
        for k, v in data.items():
            k = str(k)
            new_key = f"{parent_key}_{k}" if parent_key else k
            items.extend(flatten_dict(v, new_key))
    elif isinstance(data, (list, tuple)):
        for i, v in enumerate(data):
            new_key = f"{parent_key}_{i}"
            items.extend(flatten_dict(v, new_key))
    else:
        items.append((parent_key, str(data)))
    
    return items
    
def extract_all_metadata(file_path):
    """Extract all metadata and return as dictionaries"""
    exif_data = {}
    iptc_data = {}
    xmp_data = {}
    camera_make = ''
    camera_model = ''
    datetime_original = ''

    # Extract EXIF
    try:
        image = Image.open(file_path)
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)

                exif_data[tag_name] = value
                
                if tag_name == 'Make':
                    camera_make = str(value)
                elif tag_name == 'Model':
                    camera_model = str(value)
                elif tag_name == 'DateTimeOriginal':
                    datetime_original = str(value)
    except Exception as e:
        print(f"EXIF error for {file_path}: {e}")
    
    # Extract IPTC
    try:
        iptc = iptcinfo3.IPTCInfo(file_path, force=True)
        for key in iptc._data:
            value = iptc[key]
            if value:
                    if isinstance(value, bytes):
                        value = value.decode(errors='ignore')
                    iptc_data[key] = str(value)
    except Exception as e:
        print(f"IPTC error for {file_path} {e}")
    
    # Extract XMP
    try:
        with Image.open(file_path) as img:
            xmp = img.getxmp()

            if xmp:
                for key, value in xmp.items():
                    xmp_data[key] = value
            
    except Exception as e:
        print(f"XMP error for {file_path}: {e}")
    
    return {
        'exif' : exif_data,
        'iptc' : iptc_data,
        'xmp' : xmp_data,
        'camera_make': camera_make,
        'camera_model': camera_model,
        'datetime_original': datetime_original
    }


folder = "C:/cst2112_data/ga3/data"

for filename in os.listdir(folder):

    if filename.lower().endswith((".jpg",".jpeg",".png",".bmp",".tiff")):

        file_path = os.path.join(folder,filename)
        file_size = os.path.getsize(file_path)

        print("Processing:", filename)

        metadata = extract_all_metadata(file_path)

        with open(file_path,"rb") as f:
            image_bytes = pyodbc.Binary(f.read())


        cur.execute("""
        INSERT INTO ga3_raw
        (filename,file_path,file_size,camera_make,camera_model,datetime_original,exif_metadata,iptc_metadata,xmp_metadata)
        OUTPUT INSERTED.id_column
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            filename,
            file_path,
            file_size,
            metadata["camera_make"],
            metadata["camera_model"],
            metadata["datetime_original"],
            json.dumps(stringify_metadata(metadata["exif"])),
            json.dumps(stringify_metadata(metadata["iptc"])),
            json.dumps(stringify_metadata(metadata["xmp"]))
        ))

        image_id = cur.fetchone()[0]

        sources = {
            "EXIF": metadata["exif"],
            "IPTC": metadata["iptc"],
            "XMP": metadata["xmp"]
        }

        for metadata_type,data_dict in sources.items():

            flat_items = flatten_dict(data_dict)

            for key,value in flat_items:

                parts = key.split("_",1)

                metadata_name = parts[0]
                metadata_subname = parts[1] if len(parts) > 1 else None

                cur.execute("""
                INSERT INTO ga3_metadata
                (image_id,metadata_type,metadata_name,metadata_subname,metadata_value)
                VALUES (?,?,?,?,?)
                """,
                (
                    image_id,
                    metadata_type,
                    metadata_name,
                    metadata_subname,
                    str(value)
                ))


conn.commit()

print("RAW and Metadata tables populated.")

# Build lookup table and master table
print("Building lookup table...")

cur.execute("TRUNCATE TABLE ga3_camera_lookup")

cur.execute("""
INSERT INTO ga3_camera_lookup(code1,code2,description)

SELECT
    'camera_make',
    ROW_NUMBER() OVER(ORDER BY camera_make),
    r.camera_make
FROM ga3_raw r
GROUP BY r.camera_make
""")


cur.execute("""
INSERT INTO ga3_camera_lookup(code1,code2,description)

SELECT
    'camera_model',
    ROW_NUMBER() OVER(ORDER BY camera_model),
    r.camera_model
FROM ga3_raw r
GROUP BY r.camera_model
""")

conn.commit()

print("Lookup table created.")


print("Building master table...")

cur.execute("TRUNCATE TABLE ga3_master")

cur.execute("""
INSERT INTO ga3_master
(filename,file_path,file_size,datetime_original,camera_make,camera_model)

SELECT
    r.filename,
    r.file_path,
    r.file_size,
    TRY_CONVERT(datetime,r.datetime_original),
    mk.code2,
    md.code2

FROM ga3_raw r

LEFT JOIN ga3_camera_lookup mk
ON mk.code1='camera_make'
AND mk.description=r.camera_make

LEFT JOIN ga3_camera_lookup md
ON md.code1='camera_model'
AND md.description=r.camera_model
""")

conn.commit()

print("Master table created.")

# Close connection

cur.close()
conn.close()

print("Database connection closed.")

# Example SQL code for querying

'''
SELECT
    m.image_id,
    m.filename,
    
    m.camera_make AS make_code,
    mk.description AS lookup_make,

    m.camera_model AS model_code,
    mk.description AS lookup_model,

    exif_make.metadata_value  AS exif_make,
    exif_model.metadata_value AS exif_model,

    xmp_make.metadata_value   AS xmp_make,
    xmp_model.metadata_value  AS xmp_model

FROM ga3_master m

LEFT JOIN ga3_camera_lookup mk
    ON mk.code1 = 'camera_make'
    AND mk.code2 = m.camera_make

LEFT JOIN ga3_camera_lookup md
    ON md.code1 = 'camera_model'
    AND md.code2 = m.camera_model

LEFT JOIN ga3_metadata exif_make
ON m.image_id = exif_make.image_id
AND exif_make.metadata_type = 'EXIF'
AND exif_make.metadata_name = 'Make'

LEFT JOIN ga3_metadata exif_model
ON m.image_id = exif_model.image_id
AND exif_model.metadata_type = 'EXIF'
AND exif_model.metadata_name = 'Model'

LEFT JOIN ga3_metadata xmp_make
ON m.image_id = xmp_make.image_id
AND xmp_make.metadata_type = 'XMP'
AND xmp_make.metadata_name = 'xmpmeta'
AND xmp_make.metadata_subname = 'RDF_Description_2_Make'

LEFT JOIN ga3_metadata xmp_model
ON m.image_id = xmp_model.image_id
AND xmp_model.metadata_type = 'XMP'
AND xmp_model.metadata_name = 'xmpmeta'
AND xmp_model.metadata_subname = 'RDF_Description_2_Model'

ORDER BY m.image_id;
'''