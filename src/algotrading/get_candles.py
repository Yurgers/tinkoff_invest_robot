import time
from datetime import timedelta

from tinkoff.invest import (
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
    CandleInterval,
)

from tinkoff.invest.utils import now


def get_all_candles(client, figi, periud_day):
    candles = client.get_all_candles(
        figi=figi,
        from_=now() - timedelta(days=periud_day),
        interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
    )

    return candles


def request_iterator(figi):
    yield MarketDataRequest(
        subscribe_candles_request=SubscribeCandlesRequest(
            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
            instruments=[
                CandleInstrument(
                    figi=figi,
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ],
        )
    )
    while True:
        time.sleep(10)
