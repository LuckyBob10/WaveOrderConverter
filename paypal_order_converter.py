import argparse
import csv
import os
import pdb

version = 1.0
print('PayPal Order Converter v{}'.format(version))
print('---------------------------')

parser = argparse.ArgumentParser(
    description='Convert PayPal CSV sales data to Wave CSV format'
)
parser.add_argument(
    'input_csv',
    type=argparse.FileType('r'),
    help='Full path to PayPal input file'
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

        values = [
            float(row['Gross'])
        ]
        if float(row['Fee']) != 0:
            values.append(abs(float(row['Fee'])) * -1)
            if float(row['Shipping and Handling Amount'] or 0) > 0:
                values.append(float(row['Shipping and Handling Amount']))
        for value in values:
            date = 'ERROR - UNABLE TO FIND DATE COLUMN IN SOURCE'
            if 'Date' in row:
                date = row['Date']
            elif 'date' in row:
                date = row['date']
            desc = row['Type']
            if row['Name']:
                desc += ' - {}'.format(row['Name'])
            csv_outdata.append(
                {
                    'date': date,
                    'amount': value,
                    'description': desc
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
