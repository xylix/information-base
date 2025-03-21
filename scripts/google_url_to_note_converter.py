#!/usr/bin/env python3
"""
Script to convert Google search URLs to TODO notes.
Example:
https://www.google.com/search?client=firefox-b-d&q=pian-relevantteja+kouluasioita
becomes "TODO/note: pian relevantteja kouluasioita"
"""

import sys
from urllib.parse import urlparse, parse_qs

def google_url_to_note(url):
    """
    Convert a Google search URL to a TODO note format.

    Args:
        url (str): A Google search URL

    Returns:
        str: A formatted note string
    """
    try:
        # Parse the URL and extract query parameters
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Check if this is likely a Google search URL
        if 'google' not in parsed_url.netloc or 'q' not in query_params:
            return "not google url"

        # Extract the search query
        search_query = query_params['q'][0]

        # Clean up the query - replace + with spaces and remove hyphens
        search_query = search_query.replace('+', ' ').replace('-', ' ')

        # Convert to proper format
        note = f"TODO/note: {search_query}"

        return note

    except Exception as e:
        return f"Error processing URL: {e}"

def main():
    # Check if URL was provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        result = google_url_to_note(url)
        print(result)
    else:
        # Read URLs from standard input if no arguments are provided
        print("Enter Google URLs (one per line, press Ctrl+D when finished):")
        for line in sys.stdin:
            url = line.strip()
            if url:
                result = google_url_to_note(url)
                print(result)

if __name__ == "__main__":
    main()
