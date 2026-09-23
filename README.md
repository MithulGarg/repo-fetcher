# Repo Fetcher

Repo Fetcher is a Python CLI tool that fetches the top 5 most starred GitHub repositories created in the past 7 days. The information is saved in a Markdown file for easy viewing.

## Features

- Fetches the most starred repositories from GitHub.
- Outputs repository name, URL, and description.
- Saves the results in a `trending.md` file.

## Requirements

- Python 3.x
- `requests` library

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the script, execute the following command in your terminal:

```
python fetcher.py
```

This will create a `trending.md` file in the project directory containing the top 5 most starred repositories.

## License

This project is licensed under the MIT License.