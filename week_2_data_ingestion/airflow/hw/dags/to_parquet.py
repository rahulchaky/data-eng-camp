import pyarrow.csv as pv
import pyarrow.parquet as pq


# Takes a csv file and outputs a parquet file
def format_to_parquet(csv_file):
    table = pv.read_csv(csv_file)
    pq.write_table(table, csv_file.replace('.csv', '.parquet'))
