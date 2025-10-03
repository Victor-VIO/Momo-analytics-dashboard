import xml.etree.ElementTree as ET
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XML_PATH = ROOT / "data" / "raw" / "momo.xml"
OUT_JSON = ROOT / "data" / "processed" / "transactions.json"

def parse_transaction(elem):
    # helpers to get text safely
    def t(p, tag):
        node = p.find(tag)
        return node.text.strip() if node is not None and node.text else None

    tx = {}
    tx['transaction_id'] = int(t(elem, 'transaction_id'))
    tx['type'] = t(elem, 'type')
    tx['amount'] = float(t(elem, 'amount')) if t(elem, 'amount') else None
    tx['timestamp'] = t(elem, 'timestamp')
    tx['status'] = t(elem, 'status')

    # sender
    s = elem.find('sender')
    tx['sender'] = {
        'user_id': int(t(s, 'user_id')),
        'name': t(s, 'name'),
        'phone': t(s, 'phone')
    }
    # receiver
    r = elem.find('receiver')
    tx['receiver'] = {
        'user_id': int(t(r, 'user_id')),
        'name': t(r, 'name'),
        'phone': t(r, 'phone')
    }
    # category stored as 'type'
    tx['category'] = {
        'category_name': tx['type']
    }
    return tx

def run_parser():
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    transactions = []
    for tr in root.findall('transaction'):
        transactions.append(parse_transaction(tr))
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2)
    print(f"Parsed {len(transactions)} transactions -> {OUT_JSON}")

if __name__ == "__main__":
    run_parser()