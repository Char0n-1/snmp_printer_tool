# 📨 SNMP Printer Toner Checker

A Python-based async SNMP utility to check printer toner levels (remaining and maximum capacity), supporting multiple printers and tabular output.

## 📦 Features

* Async SNMP querying using `pysnmp` v7.1+
* Reads printer IPs and optional comments from a CSV file
* Displays toner info in a clean terminal table (`tabulate`)
* Skips disabled devices based on comment field
* Supports black toner or other consumables via index

---

## 📁 Project Structure

```
printer-checker/
├── printers.csv          # List of printer IPs and optional comments
├── check_toner.py        # Main script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🔧 Requirements

* Python 3.8+
* `pysnmp >= 7.1.0` (LexStudio)
* `tabulate`

---

## 🧺 Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/printer-checker.git
cd printer-checker
```

### 2. Create and activate virtual environment

```bash
python3 -m venv snmp-env
source snmp-env/bin/activate  # On Windows: snmp-env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare `printers.csv`

```csv
ip,comment
192.168.1.97,
192.168.1.114,test lab
192.168.1.121,main office
192.168.1.122,disabled   # will be skipped
```

### 5. Run the script

```bash
python check_toner.py
```

---

## 🧾 Sample Output

```
+------------------+----------------+-------------+-----------+---------------+-----------+
| IP Address       | Description    | Comment     | Remaining | Max Capacity  | Toner %   |
+------------------+----------------+-------------+-----------+---------------+-----------+
| 192.168.1.97     | Black Toner    |             | 8727      | 10000         | 87%       |
| 192.168.1.114    | Black Toner    | test lab    | -3        | 10000         | Unknown   |
| 192.168.1.121    | Drum Cartridge | main office | 5000      | 5000          | 100%      |
+------------------+----------------+-------------+-----------+---------------+-----------+
```

---

## 🛠️ Customization

* To check other consumables (e.g., Drum, Color toner), change the `index` in the script.
* You can export to CSV or schedule the script as a cron job if needed.

---

## 📜 License

MIT License. See `LICENSE` for details.
