# CIS Benchmark Data Fetcher

[Overview](#cis-benchmark-data-fetcher) | [Prerequisites](#prerequisites) | [Usage](#usage) | [Code Explanation](#code-explanation) | [License](#license) | [Acknowledgments](#acknowledgments)

This Python script fetches CIS benchmark data from the CIS WorkBench website and stores it as local JSON files.

## Prerequisites

- Python 3.x
- Requests library (`pip install requests`)
- Beautiful Soup library (`pip install beautifulsoup4`)

Or

- `pip install -r requirements.txt`

## Usage

1. Clone or download the repository to your local machine.
2. Install the required dependencies mentioned in the prerequisites section.
3. Generate a standard Netscape format `cookies.txt` file containing valid session cookies for the [CIS WorkBench website](https://workbench.cisecurity.org/). This file contains the necessary authentication cookies to access the benchmark data. Save the `cookies.txt` file in the same directory as the script.
4. Get a `navtree.json` JSON file for the benchmarks you wish to download and place it in the same directory as the script.
    - The file is requested by the browser when you visit a benchmarke page on cisworkbench.org. 
    - For example, If you visit [Microsoft Azure Foundations Benchmark v1.5.0](https://workbench.cisecurity.org/benchmarks/8528) the page will make a request for a `navtree.json` at [https://workbench.cisecurity.org/api/v1/benchmarks/8528/navtree](https://workbench.cisecurity.org/api/v1/benchmarks/8528/navtree)
    - Download the file and place it in the same directory as the script.
5. Run the script using the command: `python fetch_cis_data.py`
6. The script will fetch the benchmark data and store it as a local JSON file in the same directory as the script `./output/{cis_version}`.

## Code Explanation

The script consists of the following main functions:

1. `fetch_data(url, session)`: Sends an HTTP GET request to the specified URL using the provided session object and returns the response text if the request is successful.

2. `parse_json(json_data)`: Extracts specific data from the provided JSON representation of the CIS benchmark navigation tree. The function retrieves recommendation details such as ID, title, and URL, and adds them to a list of dictionaries.

3. `fetch_webpage_data(data)`: Fetches additional data from the webpages of CIS benchmark recommendations. It loads the authentication cookies from the `cookies.txt` file, retrieves the HTML content of the recommendation webpage, and uses Beautiful Soup to parse the HTML and extract specific elements. The extracted data is added to the input dictionary and returned.

4. The script reads the `navtree.json` file, parses its JSON content, and fetches the webpage data for the first recommendation. The resulting data is written to the `output.py` file.

For more information, refer to the comments within the script.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This script is based on CIS WorkBench's publically available resources and leverages the Requests and Beautiful Soup libraries. Special thanks to the CIS community for their contributions and collaboration.