class TXSerializer:
    def __init__(self):
        self.tx_hashes = set()

    def serialize_tx_data(self, tx: dict) -> dict:
        hash_ = tx.get('hash')
        if hash_ in self.tx_hashes:
            return {}
        self.tx_hashes.add(hash_)
        return {
            'hash': hash_,
            'from_': tx.get('from'),
            'to_': tx.get('to'),
            'status': int(tx.get('txreceipt_status')),
            'confirmations': int(tx.get('confirmations'))
        }
