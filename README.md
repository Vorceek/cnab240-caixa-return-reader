# 📄 CNAB240 CAIXA Return File Reader (SIGCB)

This project reads **CNAB240 bank return files from Caixa Econômica Federal (SIGCB)**, extracts relevant billing information, and generates output files in **CSV or Excel (XLSX)** format.

The script is designed to identify **paid and unpaid titles**, making bank reconciliation and financial analysis easier.

---

## ✨ Features

- Reads `.ret` files following the **CNAB240 – Caixa** standard
- Processes **Segment T and Segment U**
- Extracts the following fields:
  - **Payer Name (Customer)**
  - **Your Number (Invoice / Title Identifier)**
  - **Paid Amount**
  - **Title Status** (`PAID` or `NOT PAID`)
- Generates output files in:
  - `CSV` (default)
  - `XLSX` (Excel)
- Automatic counting of paid and unpaid titles

---

## 🧾 Business Rules Applied

- A title is considered **PAID** when:
  - Return movement code = `06` (Settlement) or `46` (Online settlement)
  - **Paid amount > 0**
- Any other scenario is treated as **NOT PAID**
- Each record is built from a **Segment T + Segment U** pair

---

## 📂 Field Structure (CNAB240)

Based on the **CNAB240 Manual – Caixa Econômica Federal**:

### Segment T
- **Your Number**: positions `106–130`
- **Payer Name**: positions `149–188`

### Segment U
- **Return Movement Code**: positions `16–17`
- **Paid Amount**: positions `78–92`

---

## 🚀 How to Use

### Requirements

- Python **3.8+**
- Dependencies:
```bash
pip install openpyxl
```

---

### Execution

```bash
python read_caixa_return.py file.ret [csv|xlsx]
```

#### Examples

Generate CSV (default):
```bash
python read_caixa_return.py return.ret
```

Generate Excel:
```bash
python read_caixa_return.py return.ret xlsx
```

---

## 📤 Generated Files

- `file.csv` **or**
- `file.xlsx`

With the following columns:

| CUSTOMER | INVOICE | PAID_AMOUNT | STATUS |
|--------|--------|-------------|--------|

---

## 📊 Console Output

After processing, the script displays:

- Total records processed
- Number of **PAID** titles
- Number of **NOT PAID** titles

Example:
```
Processing completed!
Generated file: return.csv
Records: 120 | PAID: 85 | NOT PAID: 35
```

---

## 🔐 Privacy & Security

✅ **This repository DOES NOT contain any personal or sensitive data.**

- The code:
  - Does not hardcode **CPF, CNPJ, bank accounts, keys, passwords, or real names**
  - Only processes files provided by the user at runtime
- No data is sent to the internet, APIs, or external services
- Safe to publish as a public GitHub repository

⚠️ **Important:**  
Return files (`.ret`) and generated outputs (`.csv`, `.xlsx`) may contain sensitive data and **should not be committed** to version control.

Recommended `.gitignore`:
```gitignore
*.ret
*.csv
*.xlsx
```

---

## 🛠 Technologies Used

- Python
- `openpyxl`
- `decimal`
- `csv`
- Text file reading with `latin-1` encoding

---

## 📄 License

This project is free to use, modify, and distribute.  
If used in production or as a base for other projects, please keep reference to the CNAB240 Caixa standard.
