from tinkoff.invest import MoneyValue

from loguru import logger

from src.algotrading.utils import to_float
from src.algotrading import utils


def get_sandbox_accounts(client):
    sandbox_accounts = {}
    accounts = client.sandbox.get_sandbox_accounts()
    for account in accounts.accounts:
        sandbox_accounts[account.id] = {}
        sandbox_accounts[account.id]['info'] = {}
        sandbox_accounts[account.id]['info']['name'] = account.name
        sandbox_accounts[account.id]['info']['status'] = " ".join(account.status._name_.split('_')[2:])
        sandbox_accounts[account.id]['info']['opened_date'] = account.opened_date.strftime("%Y-%m-%d %H:%M")
        sandbox_accounts[account.id]['info']['access_level'] = " ".join(account.access_level._name_.split('_')[3:])

    return sandbox_accounts


def delete(uuid):
    api_client = utils.api_client_configure()
    with api_client as client:
        client.sandbox.close_sandbox_account(account_id=uuid)


def payin(uuid, amount, cur='rub'):
    if cur == 'rub':
        pay_in_cur(uuid, amount, cur)
    elif cur == 'usd':
        pay_in_cur(uuid, amount, cur)


def pay_in_cur(uuid, amount, cur):
    money = MoneyValue(cur, amount, 0)
    api_client = utils.api_client_configure()
    with api_client as client:
        logger.info(client.sandbox.sandbox_pay_in(account_id=uuid, amount=money))


def open():
    api_client = utils.api_client_configure()
    with api_client as client:
        client.sandbox.open_sandbox_account()


def get_sandbox_positions(client, account_id):
    positions = {}
    sandbox_positions = client.sandbox.get_sandbox_positions(account_id=account_id)
    for val in ['money', 'blocked']:
        positions[val] = []
        for money in sandbox_positions.__getattribute__(val):
            positions[val].append({"currency": money.currency,
                                   "val": to_float(money)
                                   })

    return positions


def get():
    api_client = utils.api_client_configure()
    with api_client as client:
        sandbox_accounts = get_sandbox_accounts(client)
        for account_id in sandbox_accounts:
            positions = get_sandbox_positions(client, account_id)

            sandbox_accounts[account_id]['positions'] = positions

    return sandbox_accounts


if __name__ == "__main__":
    print(get())
