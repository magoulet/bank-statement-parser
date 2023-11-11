# Bank Statement Parser

This Python script is designed to parse bank statement data from various investment accounts. Currently, it is tailored for analyzing dividends from Interactive Broker (IBKR) statements, CI Direct Investing statements, and closed account statements. Users are welcome to adapt this script to their needs by customizing it for their own data sources.

## Table of Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Dependencies

This script requires the following dependencies to be installed:

- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)

To install the required dependencies, run the following command:

```
pip install matplotlib pandas
```

## Installation

To use this script, follow these steps:

1. Clone or download the repository to your local machine.
2. Install the required dependencies as mentioned in the [Dependencies](#dependencies) section.

## Usage

To analyze dividend data from your investment accounts, follow these steps:

1. Create a file named `config.yml` in the same folder as the `main.py` script.

   The `config.yml` file should follow the following format:

   ```yaml
   ci:
     basedir: '<directory containing CI statement file>'
     filename: '<CI statement filename>'

   ibkr:
     basedir: '<directory containing IBKR statement file>'
     filename: '<IBKR statement filename>'

   closed:
     basedir: '<directory containing closed account statement file>'
     filename: '<closed account statement filename>'
   ```

   Replace `<directory containing statement file>` with the actual directory path and `<statement filename>` with the name of the statement file for each respective account. 

2. Open the script file `main.py` in a text editor or IDE.
3. Modify the file according to your specific use case. For example, update the parsing functions for different account statements.
4. Save the modifications and run the script using the following command:

   ```
   python main.py
   ```

   The script will analyze the dividend data and generate a plot showing the dividend amounts over time. It will also print the dividend data for each account and the combined dividends for the last 12 months.

5. Review the generated plot and printed data to analyze the dividends from your investment accounts.

## Configuration

The `config.yml` file is used to specify the file path and names of the account statements for the script to parse. 

Make sure to provide the correct directory paths and filenames for each account in the `config.yml` file. Double-check that the directory paths and filenames match your file system.

## Customization

This script can be customized to suit your needs. Here are some potential customization options:

- Modify the script to support additional account statement formats.
- Enhance the analysis by adding new metrics or calculations.
- Customize the plot by changing its style or adding additional visualizations.

Feel free to explore the code and adapt it to meet your requirements.

## Contributing

Contributions to this script are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Make your changes and improvements.
3. Test your changes to ensure they work correctly.
4. Commit your changes and submit a pull request.

Please provide a clear description of the changes you have made and the problem they address. Any feedback or suggestions are also appreciated!

## License

This project is licensed under the [MIT License](LICENSE).
