import pandas as pd
import requests
import trafilatura
import argparse
from tqdm import tqdm
import signal
import os


# Define a flag to indicate if Ctrl+C was received
ctrl_c_received = False

# Signal handler to intercept Ctrl+C
def signal_handler(signal, frame):
    global ctrl_c_received
    ctrl_c_received = True


# Function to fetch and extract text from a URL
def fetch_and_extract_text(url):
    try:
        # Download the URL and extract the main text
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            # Try again with a different user agent
            downloaded = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'}).text
        main_text = trafilatura.extract(downloaded)
        return main_text
    except Exception as e:
        return str(e)


def main():
    parser = argparse.ArgumentParser(description="CSV URL Text Extractor")
    parser.add_argument("-i", "--input", help="Input CSV file path", required=True)
    parser.add_argument("-o", "--output", help="Output CSV file path", required=True)
    args = parser.parse_args()

    # Read the input CSV
    df = pd.read_csv(args.input)

    # Create an empty column for the extracted text
    df['text'] = ""

    # Load the existing output file if it exists
    if os.path.isfile(args.output):
        existing_df = pd.read_csv(args.output)
        # Mark rows that have already been processed
        df = df.merge(existing_df[['id', 'text']], on='id', how='left', suffixes=('', '_existing'))
        # Update the 'text' column with the values from existing data
        df['text'] = df['text_existing'].fillna(df['text'])
        # Drop the extra column
        df = df.drop(columns=['text_existing'])

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Loop through the URLs and fetch/extract text with tqdm
    for index, row in tqdm(df.iterrows(), total=len(df)):
        url = row['url']

        # Skip rows that already have text in the 'text' column
        if row['text'] != "":
            continue

        try:
            extracted_text = fetch_and_extract_text(url)
            df.at[index, 'text'] = extracted_text
        except Exception as e:
            # Handle the error, e.g., print an error message
            print(f"Error processing URL {url}: {str(e)}")

        # Check if Ctrl+C was received
        if ctrl_c_received:
            print("Ctrl+C received. Saving the CSV and exiting.")
            break

    # Write the results to a new CSV file
    df.to_csv(args.output, index=False)

    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
