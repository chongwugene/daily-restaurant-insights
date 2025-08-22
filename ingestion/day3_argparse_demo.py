import argparse

p = argparse.ArgumentParser(description="Demo of argparse")
p.add_argument("--term", type=str, required=True, help="Search term, e.g. 'korean bbq'")
p.add_argument("--max-records", type=int, default=150, help="How many records to fetch")
args = p.parse_args()

print("term:", args.term)
print("max:", args.max_records)
