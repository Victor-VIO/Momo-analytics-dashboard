# dsa/dsa_compare.py
import json, timeit, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "transactions.json"

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def linear_search(transactions, tid):
    for t in transactions:
        if t.get('transaction_id') == tid:
            return t
    return None

def dict_lookup(trans_map, tid):
    return trans_map.get(tid)

def run_compare():
    transactions = load_data()
    # Ensure at least 20 records by duplicating if necessary (testing only)
    while len(transactions) < 20:
        # create clone with new id
        new = dict(transactions[-1])
        new_id = transactions[-1]['transaction_id'] + 1
        new['transaction_id'] = new_id
        transactions.append(new)

    # build dict
    trans_map = {t['transaction_id']: t for t in transactions}

    # pick 1000 random ids to measure cost
    ids = [random.choice(transactions)['transaction_id'] for _ in range(1000)]

    # time linear search
    def ls():
        for i in ids:
            linear_search(transactions, i)
    def dl():
        for i in ids:
            dict_lookup(trans_map, i)

    t_ls = timeit.timeit(ls, number=1)
    t_dl = timeit.timeit(dl, number=1)

    print(f"Records used: {len(transactions)}")
    print(f"Linear search time (1000 lookups): {t_ls:.6f} sec")
    print(f"Dict lookup time (1000 lookups):   {t_dl:.6f} sec")
    print("Average per lookup (linear): {:.6f} ms".format((t_ls/1000)*1000))
    print("Average per lookup (dict):   {:.6f} ms".format((t_dl/1000)*1000))

    return {'records': len(transactions), 'linear': t_ls, 'dict': t_dl}

if __name__ == "__main__":
    run_compare()
