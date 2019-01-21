# Install Instructions
1. Install the latest version of Python3 via Brew: https://docs.python-guide.org/starting/install3/osx/
2. Download this repository as a `.zip` file
3. Extract to an easy to find location such as `~/Documents/WaveOrderConverter`

# Usage Instructions
1. Copy the source CSV data into `Documents/WaveOrderConverter-master`
2. Go to `Applications` > `Utilities` > `Terminal`
3. `cd Documents/WaveOrderConverter`
4. `python3 name_of_order_converter.py source_data.csv`

## Usage Hints and Tricks
* For usage instructions run: `python3 name_of_order_converter.py -h`
* To show verbose output run: `python3 name_of_order_converter.py -v source_data.csv`
* To allow overwrite of destination file (**DANGEROUS**) run: `python3 name_of_order_converter.py -f source_data.csv`
