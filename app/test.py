from sdk.coingecko_service import CoingeckoService
from services.decode_input import decode_input

coingecko_service = CoingeckoService()

result = coingecko_service.fetch_historic_price('wbnb', '01-01-2022')

print(result['usd'])