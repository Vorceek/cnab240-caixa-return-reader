# -*- coding: utf-8 -*-
"""
CNAB240 RETURN FILE READER - CAIXA (SIGCB)

Extracts:
- Payer Name (customer)
- Your Number (invoice / title identifier)
- Paid Amount
- Title Status (PAID / NOT PAID)

Generates CSV or XLSX output.

Based on the CNAB240 CAIXA manual:
- Segment T: Your Number (106-130); Payer Name (149-188)
- Segment U: Return Movement Code (16-17); Paid Amount (78-92)
"""

import csv
import sys
from pathlib import Path
from decimal import Decimal
from openpyxl import Workbook


def fw(line: str, start: int, end: int) -> str:
    """CNAB fixed-width slice: 1-based positions (start..end inclusive)."""
    return line[start - 1:end]


def parse_caixa_cnab240_return(file_path: Path):
    records = []
    current = None  # holds Segment T until the matching Segment U is read

    with open(file_path, "r", encoding="latin-1") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.rstrip("\n")

            # CNAB240: each line must be 240 chars
            if len(line) < 240:
                continue

            record_type = line[7]   # position 8
            if record_type != "3":  # detail record
                continue

            segment = line[13]      # position 14

            # -------- SEGMENT T --------
            if segment == "T":
                current = {
                    "customer": fw(line, 149, 188).strip(),
                    "invoice": fw(line, 106, 130).strip(),
                    "paid_amount": Decimal("0.00"),
                    "status": "NOT PAID",
                }

            # -------- SEGMENT U --------
            elif segment == "U" and current is not None:
                movement_code = fw(line, 16, 17)
                paid_amount = Decimal(int(fw(line, 78, 92))) / 100

                current["paid_amount"] = paid_amount

                # PAID when settlement (06) or online settlement (46) and amount > 0
                if movement_code in {"06", "46"} and paid_amount > 0:
                    current["status"] = "PAID"
                else:
                    current["status"] = "NOT PAID"

                records.append(current)
                current = None  # close T/U pair

    return records


def generate_csv(records, output_path: Path):
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["CUSTOMER", "INVOICE", "PAID_AMOUNT", "STATUS"])

        for r in records:
            writer.writerow([
                r["customer"],
                r["invoice"],
                f"{r['paid_amount']:.2f}".replace(".", ","),
                r["status"]
            ])


def generate_excel(records, output_path: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Caixa Return"

    ws.append(["CUSTOMER", "INVOICE", "PAID_AMOUNT", "STATUS"])

    for r in records:
        ws.append([
            r["customer"],
            r["invoice"],
            float(r["paid_amount"]),
            r["status"]
        ])

    wb.save(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python read_caixa_return.py file.ret [csv|xlsx]")
        sys.exit(1)

    return_file = Path(sys.argv[1])

    if not return_file.exists():
        print("File not found.")
        sys.exit(1)

    output_format = "csv"
    if len(sys.argv) >= 3:
        output_format = sys.argv[2].lower()

    records = parse_caixa_cnab240_return(return_file)

    if output_format == "xlsx":
        output = return_file.with_suffix(".xlsx")
        generate_excel(records, output)
    else:
        output = return_file.with_suffix(".csv")
        generate_csv(records, output)

    print("Processing completed!")
    print(f"Generated file: {output}")
    print(
        f"Records: {len(records)} | "
        f"PAID: {sum(r['status'] == 'PAID' for r in records)} | "
        f"NOT PAID: {sum(r['status'] == 'NOT PAID' for r in records)}"
    )


if __name__ == "__main__":
    main()
