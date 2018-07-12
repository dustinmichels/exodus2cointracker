import os
import json
from datetime import datetime
import pandas as pd


def find_exodus_folder():
    """Returns name of first folder beginning with 'exodus-report-SAFE...'
    within current directory, or raises an error."""
    try:
        exodus_folder = [f for f in os.listdir() if f.startswith('exodus-report-SAFE-')].pop()
    except IndexError:
        print('ERROR: exodus-report-SAFE... export folder could not be found.')
        raise
    return exodus_folder


def load_txs(exodus_folder):
    """Iterate over json files in exodus folder, return list of tx dicts"""
    txs = []
    path = os.path.join(exodus_folder, 'v1', 'txs')
    json_files = [f for f in os.listdir(path) if f.endswith('.json')]
    for file in json_files:
        filepath = os.path.join(path, file)
        with open(filepath) as f:
            txs += json.load(f)
    return txs


def remove_duplicates(all_txs):
    """If two transactions share a shapeshiftOrderId, removes the second"""
    ids = set()
    txs = all_txs[:]
    remove_txs = []
    for tx in all_txs:
        order_id = tx.get('meta').get('shapeshiftOrderId')
        if order_id in ids:
            remove_txs.append(tx)
        if order_id:
            ids.add(order_id)
    [txs.remove(t) for t in remove_txs]  # remove each item in remove_txs from txs
    return txs


def parse_tx(tx):
    """Given single tx (from json), returns dict of relevant information"""
    # determine date
    dt = datetime.strptime(tx['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date = dt.strftime('%m/%d/%Y %H:%M:%S')

    # determine sent/recieved fields
    amnt, coin = tx['coinAmount'].split(' ')

    # if amnt pos, received
    if float(amnt) > 0:
        rec_amnt, rec_coin = amnt, coin
        from_coin = tx.get('fromCoin')
        if from_coin:
            sent_amnt, sent_coin = from_coin['coinAmount'].split(' ')
        else:
            sent_amnt, sent_coin = '', ''
    # if amnt neg, sent
    else:
        sent_amnt, sent_coin = str(float(amnt) * -1), coin
        to_coin = tx.get('toCoin')
        if to_coin:
            rec_amnt, rec_coin = to_coin['coinAmount'].split(' ')
        else:
            rec_amnt, rec_coin = '', ''

    return dict(
        date=date, sent_amnt=sent_amnt, sent_coin=sent_coin,
        rec_amnt=rec_amnt, rec_coin=rec_coin)


def parse_txs(txs):
    """Parse each tx in txs, returning list of dicts."""
    return [parse_tx(t) for t in txs]


def tx_dicts_to_csv(tx_dicts, filename='cointracker_output.csv'):
    """Write parsed txs (list of dicts) to csv"""
    df = pd.DataFrame.from_dict(tx_dicts)
    df = df.rename(index=str, columns={
        'date': 'Date',
        'rec_amnt': 'Received Quantity',
        'rec_coin': 'Currency',
        'sent_amnt': 'Sent Quantity',
        'sent_coin': 'Currency'})
    df.to_csv(filename, index=False)
    return filename


def main():
    exodus_folder = find_exodus_folder()
    print(f'> Found exodus folder "{exodus_folder}"')

    all_txs = load_txs(exodus_folder)
    print(f'> Loaded {len(all_txs)} transactions')

    txs = remove_duplicates(all_txs)
    print(f'> Removed {len(all_txs) - len(txs)} duplicate transactions')

    tx_dicts = parse_txs(txs)
    print(f'> Parsed all transactions into CoinTracker format')

    file = tx_dicts_to_csv(tx_dicts)
    print(f'> Wrote csv to "{file}"')


if __name__ == "__main__":
    main()
