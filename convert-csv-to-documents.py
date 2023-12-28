#!/usr/bin/env python3
import csv, os, json, argparse, shutil

parser = argparse.ArgumentParser(description='Convert a CSV file into a collection of JSON documents')

parser.add_argument(
    '--csv-file', type=str, required=False,
    help='the CSV file to be converted, the header line MUST be at the first line in the file'
)

parser.add_argument(
    '--output-dir', type=str, required=False, default='coll',
    help='the directory to store the generated JSON documents'
)

args = parser.parse_args()

with open(args.csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_id = -1
    headers = []
    
    if os.path.exists(args.output_dir):
        shutil.rmtree(args.output_dir)
    os.mkdir(args.output_dir)

    for row in csvreader:
        row_id+=1
        doc = {}
        col_id = -1
        for raw_col in row:
            col_id += 1
            col = raw_col.replace('"', '')
            if row_id == 0:
                headers.append(col)
            else:
                col_name = headers[col_id] 
                doc[col_name] = col
        if row_id > 0:
            doc_name = "doc-{}".format(row_id)
            doc_path = "{}/{}.json".format(args.output_dir, doc_name)
            with open(doc_path, 'w') as docfile:
                json.dump(doc, docfile, indent=4)
                docfile.close()
    
    csvfile.close()

        

