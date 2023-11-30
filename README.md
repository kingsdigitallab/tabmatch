A simple tool to match rows across multiple tables based on a set of columns.

# 1. Installation

Install Python 3 

## 1.1 Get the code

Clone this repository or [download the ZIP file](https://github.com/kingsdigitallab/tabmatch/archive/refs/heads/main.zip) and unzip it.

## 1.2 Set up the python environment

Go in the terminal/console and change to the tabmatch folder.

### 1.3 Create the virtual environment

`python -m venv venv`

### 1.4 Activate the environment:

On Windows:
`venv\Scripts\activate`

On other systems:
`source venv/bin/activate`

### 1.5 Install packages

`pip install -r requirements.txt`

# 2. Usage

* Copy your input files (in ODS format, .ods) anywhere under the data/in folder.
* Go to the terminal/console and change into the `tabmatch` folder.
* Activate the environment (See 1.4 above).
* Run the script to list rows with the same names among your input files.

`python tabmatch.py > matches.csv`

* open `matches.csv` with your spreadsheet editor (e.g. Excel).

# 3. Format of the output file

The output file is a CSV with one row per occurrence of a name in one of the input tables.

For instance if John Smith appears twice in file1.ods and once in file2.ods, the output file will contain three successive rows.

Columns:
* **normalised_name**: the normalised name 
* **table**: the name of the input file the name was found
* **row_index**: the index of the row the name was found

![image](https://github.com/kingsdigitallab/tabmatch/assets/3778106/3069cd5e-fabd-47a8-82d5-2f956d063220)


# 4. Format of the input files

The input files are ODS (.ods) workbooks. Only the first spreadsheet in each file is read by the tool. Others are ignored.

Each spreadsheet must have the following columns:
* The standardised name: 'FIRST NAME (STANDARDISE)', 'LAST NAME (STANDARDISE)', 'FATHER’S NAME (STANDARDISE)'
* The transcribed name: 'FIRST NAME', 'LAST NAME', 'FATHER’S NAME'

