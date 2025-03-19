#!/usr/bin/env python3
"""
This script checks if all URLs from a reference file appear somewhere in a target file.
The target file may contain other content besides the URLs.
"""

import sys

def extract_reference_urls(filename):
    """
    Extract URLs from the reference file, one per line.
    Returns a set of URLs exactly as they appear in the file.
    """
    urls = set()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                # Strip whitespace
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                urls.add(line)

        return urls

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

def check_urls_in_file(reference_urls, target_filename):
    """
    Check if each URL from the reference set appears somewhere in the target file.
    Returns a set of URLs that were not found in the target file.
    """
    missing_urls = set()

    try:
        # Read the entire content of the target file
        with open(target_filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check each reference URL
        for url in reference_urls:
            if url not in content:
                missing_urls.add(url)

        return missing_urls

    except FileNotFoundError:
        print(f"Error: File '{target_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{target_filename}': {e}")
        sys.exit(1)

def main():
    """
    Main function to check if all reference URLs appear in the target file.
    """
    if len(sys.argv) != 3:
        print("Usage: python url_checker.py reference_urls.txt target_file.txt")
        sys.exit(1)

    reference_file = sys.argv[1]
    target_file = sys.argv[2]

    print(f"Checking if URLs from '{reference_file}' appear in '{target_file}'...")

    reference_urls = extract_reference_urls(reference_file)
    missing_urls = check_urls_in_file(reference_urls, target_file)

    # Report results
    if not missing_urls:
        print(f"SUCCESS: All {len(reference_urls)} URLs from the reference file were found in the target file.")
        return 0
    else:
        print(f"\nFAILURE: {len(missing_urls)} out of {len(reference_urls)} URLs were not found in the target file:")
        for url in sorted(missing_urls):
            print(f"  - {url}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
