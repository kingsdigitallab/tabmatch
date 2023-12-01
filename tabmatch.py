import glob
import re
import csv
import sys
from pyexcel_odsr import get_data


DEFAULT_OPTIONS = {
    # the index (1-based) of the row which contains the column names
    'headers': 2,
    # the list of column names used to match rows
    'match': ['FIRST NAME (STANDARDISE)', 'LAST NAME (STANDARDISE)', 'FATHER’S NAME (STANDARDISE)'],
    # the list of column names returned in the output
    'return': ['ORDER NUMBER', 'FIRST NAME', 'LAST NAME', 'FATHER’S NAME', 'YEAR', 'PLACE'],
}


class CSVJoin:

    def __init__(self, options=None):
        self.set_default_options()
        if options:
            self.options.update(options)
        self.names = {}

    def run(self):
        for ods_path in glob.glob("**/*.ods", recursive=True):
            self.process_ods(ods_path)

        self.write_output()

    def write_output(self):
        # with open('matched.csv', 'w', newline='') as csvfile:
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

        writer.writerow([
            'normalised_name',
            'table',
            'row_index',
        ] + self.options['return'])

        for name, rows in self.names.items():
            if len(rows) > 1:
                for row in rows:
                    writer.writerow([
                        name,
                        row['table'],
                        row['row_index']
                    ] + [
                        row['data'].get(k, '')
                        for k in self.options['return']
                    ])

    def process_ods(self, ods_path):
        # print(ods_path)

        table_name = ods_path
        # remove path & extension
        table_name = re.sub(r'^.*/', '', table_name).replace('.ods', '')
        # extract bracketed code, if any
        table_name = re.sub(r'(\[.*?\]).*$', r'\1', table_name)

        sheets = get_data(ods_path)
        for rows in sheets.values():
            headers = rows[self.options['headers'] - 1]

            for row_idx in range(self.options['headers'], len(rows)):
                row = rows[row_idx]
                if len(row) < 2:
                    continue

                row_dict = dict(zip(headers, row + ([''] * (len(headers) - len(row)))))

                key = ' '.join([
                    row_dict.get(header, '').lower().strip()
                    for header in self.options['match']
                ])

                if key not in self.names:
                    self.names[key] = []
                self.names[key].append({
                    'table': table_name,
                    'row_index': row_idx + 1,
                    'data': row_dict
                })

            # break, we don't read other sheets
            break

    def set_default_options(self):
        self.options = DEFAULT_OPTIONS


if __name__ == '__main__':
    csvjoin = CSVJoin()
    csvjoin.run()

