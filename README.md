# ClaimReview Text Extractor

ClaimReview Text Extractor is a Python script that reads a CSV file containing a list of URLs, fetches the content of these URLs, and extracts the main text from the web pages using BeautifulSoup. It then saves the results to a new CSV file.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python **>=3.9,<3.13** installed.
- [Poetry](https://python-poetry.org/) for dependency management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CIMPLE-project/claimreview-text-extractor
   cd claimreview-text-extractor
   ```

1. Install project dependencies using Poetry:

    ```bash
    poetry install
    ```

## Usage

1. Have a CSV file with two columns: `id` (URI of the ClaimReview) and `url` (URL of the page to extract the text from). For example, [this link](https://data.cimple.eu/sparql?default-graph-uri=&query=SELECT+DISTINCT+%3Fid+%3Furl+WHERE+%7B%0D%0A++GRAPH+%3Chttp%3A%2F%2Fdata.cimple.eu%2Fgraph%2Fclaim-review%3E+%7B%0D%0A++++%3Fid+a+%3Chttp%3A%2F%2Fschema.org%2FClaimReview%3E+.%0D%0A++++%3Fid+schema%3Aurl+%3Furl+.%0D%0A++%7D%0D%0A%7D%0D%0A&format=text%2Fcsv&should-sponge=&timeout=0&signal_void=on) will generate a CSV file for all claim reviews related to COVID. It is based on the following query:
    ```sparql
    SELECT DISTINCT ?id ?url WHERE {
        GRAPH <http://data.cimple.eu/graph/claim-review> {
            ?id a <http://schema.org/ClaimReview> .
            ?id schema:url ?url .
        }
    }
    ```
1. Run the script with the paths to the input CSV file and to the desired output CSV file as arguments:

    ```bash
    poetry run python main.py -i input.csv -o output.csv
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
