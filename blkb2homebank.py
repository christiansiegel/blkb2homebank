#! /usr/bin/env python3

import argparse
import csv
import os
import io
from datetime import datetime


class BlkbDialect(csv.Dialect):
    delimiter = ";"
    quotechar = '"'
    doublequote = False
    skipinitialspace = False
    lineterminator = "\n"
    quoting = csv.QUOTE_MINIMAL


class HomebankDialect(csv.Dialect):
    delimiter = ";"
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_MINIMAL


blkb_fieldnames = [
    "Buchungsdatum",
    "Text",
    "Betrag Einzelzahlung",
    "Belastung",
    "Gutschrift",
    "Valuta",
    "Saldo",
]

homebank_fieldnames = [
    "date",
    "paymode",
    "info",
    "payee",
    "memo",
    "amount",
    "category",
    "tags",
]


def convert_csv(in_filename, out_filename):
    with io.open(in_filename, "r", newline="", encoding="iso-8859-1") as in_file, io.open(
        out_filename, "w", newline="", encoding="utf-8"
    ) as out_file:
        lines = in_file.readlines()
        headers = lines[0].strip().split(";")
        for idx, expected_header in enumerate(blkb_fieldnames):
            if headers[idx] != expected_header:
                print(f"Missing CSV column {expected_header}")
                exit(1)
        transaction_lines = lines[3:-1]

        reader = csv.DictReader(
            transaction_lines, dialect=BlkbDialect, fieldnames=blkb_fieldnames
        )
        writer = csv.DictWriter(
            out_file, dialect=HomebankDialect, fieldnames=homebank_fieldnames
        )

        for row in reader:
            date = convert_to_homebank_date(row["Valuta"], "%d.%m.%Y")
            paymode = 8  # = Electronic Payment
            memo = row["Text"].strip().replace("\r\n", "\n").replace("\n", " ")
            if row["Gutschrift"]:
                amount = row["Gutschrift"]
            else:
                amount = "-" + row["Belastung"]
            amount = amount.replace("'", "")
            writer.writerow(
                {"date": date, "paymode": paymode, "memo": memo, "amount": amount}
            )
    print("Successfully converted to file: '%s'" % out_filename)


def append_to_filename(filename, text):
    root, ext = os.path.splitext(filename)
    return root + text + ext


def convert_to_homebank_date(date_string, input_format):
    date = datetime.strptime(date_string, input_format)
    return date.strftime("%d-%m-%Y")


def filename_cli():
    parser = argparse.ArgumentParser(
        description="Convert a BLKB CSV export file to the Homebank CSV format."
    )
    parser.add_argument("filename", help="The CSV file to convert.")
    parser.set_defaults(auto=True)
    return parser.parse_args().filename


def blkb2homebank():
    in_filename = filename_cli()
    out_filename = append_to_filename(in_filename, "-homebank")
    convert_csv(in_filename, out_filename)


if __name__ == "__main__":
    blkb2homebank()
