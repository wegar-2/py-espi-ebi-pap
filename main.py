from datetime import date

from pyespiebipap.common import scrape_date_entries


def run_scrape_date_entries():
    scrape_date_entries(d=date(2026, 2, 6))


def main():
    run_scrape_date_entries()


if __name__ == '__main__':
    main()
