"""Group observed, unique shipping charges. Input: [{group_id, amount}]."""
import json
import sys
from collections import Counter
from decimal import Decimal


def group_shipping(charges):
    seen = set()
    grouped = Counter()
    for charge in charges:
        key = charge['group_id']
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError('Shipping group_id must be nonempty and unique')
        seen.add(key)
        raw = charge['amount']
        if raw is None or isinstance(raw, bool):
            raise ValueError('Shipping amount is unresolved or invalid')
        amount = Decimal(str(raw))
        if not amount.is_finite() or amount < 0 or amount != amount.to_integral_value():
            raise ValueError('Shipping amount must be a nonnegative whole KRW value')
        if amount:
            grouped[int(amount)] += 1
    return [['배송비', '', '', count, amount] for amount, count in grouped.items()]


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as stream:
        charges = json.load(stream)
    print(json.dumps(group_shipping(charges), ensure_ascii=False))
