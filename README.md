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
3. Generate a standard Netscape format `cookies.txt` file containing valid session cookies for the [CIS WorkBench website](https://workbench.cisecurity.org/). You can generate this file using the [ExportCookies](https://github.com/rotemdan/ExportCookies) browser plugin. Place the `cookies.txt` file in the same directory as the script.
4. Run the script using the command: `python fetch.py`
5. The script will fetch the benchmark data from urls inside `urls.txt` and store the result for each url as a local JSON file in the directory `./output/{output_file}`.

## Code Explanation

This section is outdated and might be inacurate.

The script consists of the following main functions:

1. `fetch_data(url, session)`: Sends an HTTP GET request to the specified URL using the provided session object and returns the response text if the request is successful.

2. `parse_json(json_data)`: Extracts specific data from the provided JSON representation of the CIS benchmark navigation tree. The function retrieves recommendation details such as ID, title, and URL, and adds them to a list of dictionaries.

3. `fetch_webpage_data(data)`: Fetches additional data from the webpages of CIS benchmark recommendations. It loads the authentication cookies from the `cookies.txt` file, retrieves the HTML content of the recommendation webpage, and uses Beautiful Soup to parse the HTML and extract specific elements. The extracted data is added to the input dictionary and returned.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This script is based on CIS WorkBench's publically available resources and leverages the Requests and Beautiful Soup libraries. Special thanks to the CIS community for their contributions and collaboration.