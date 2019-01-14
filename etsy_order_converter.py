import argparse
import csv
import os
import pdb

version = 1.0
print('Etsy Order Converter v{}'.format(version))
print('-------------------------')

parser = argparse.ArgumentParser(
    description='Convert Etsy CSV sales data to Wave CSV format'
)
parser.add_argument(
    'input_csv',
    type=argparse.FileType('r'),
    help='Full path to Etsy input file'
)
parser.add_argument(
    '-f',
    '--force_overwrite',
    action='store_true',
    help='Forcibly overwrites existing CSV output file'
)
parser.add_argument(
    '-o',
    '--output_csv',
    default='[input_csv]_processed.csv',
    help=(
        'Full path to the output CSV file - defaults to '
        '`[input_csv]_processed.csv`'
    )
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Enable verbose output for diagnosics'
)
args = parser.parse_args()

csv_outheader = ['date', 'amount', 'description']
csv_outdata = []
row_count_match = 0
row_count_discard = 0
total_value = 0

print('- Reading CSV files: `{}`...'.format(args.input_csv.name))
with args.input_csv as csv_fh:
    reader = csv.DictReader(
        csv_fh,
        delimiter=',',
        quotechar='"'
    )
    for row in reader:
        if args.verbose:
            print('  - Row data: {}'.format(row))

        # Test if row fails criteria for inclusion
        if (
                row['Full Name'] is None or
                row['Full Name'] == ''
        ):
            row_count_discard += 1
            continue

        # Calculate values
        values = [
            float(row['Order Value']) - float(row['Discount Amount']),
            float(row['Shipping']),
            float(row['Card Processing Fees']) * -1
        ]
        for value in values:
            csv_outdata.append(
                {
                    'date': row['Sale Date'],
                    'amount': value,
                    'description': row['Full Name']
                }
            )
            total_value += value
        row_count_match += 1


print('- Finished reading CSV successfully')
print(
    '- Matched {} rows ({} rows skipped)'.format(
        row_count_match,
        row_count_discard
    )
)
print(
    '- Total value of all matched rows: ${}'.format(
        round(total_value, 2)
    )
)
if args.verbose:
    print('  - Output data:\n{}'.format(csv_outdata))

# Parse output file name
if '[input_csv]' in args.output_csv:
    args.output_csv = args.output_csv.replace(
        '[input_csv]',
        args.input_csv.name.replace('.csv', '')
    )
print('- Output file: `{}`'.format(args.output_csv))
if args.force_overwrite:
    print('WARNING: Output file may be overwritten due to usage of `--force_overwrite`')
elif os.path.exists(args.output_csv):
    print('ERROR: Output file already exists: {}'.format(args.output_csv))
    raise FileExistsError

print('- Writing CSV data...')
with open(args.output_csv, 'w', newline='') as csv_fh:
    writer = csv.DictWriter(csv_fh, fieldnames=csv_outheader)
    writer.writeheader()
    writer.writerows(csv_outdata)
print('- Finished!')
