import math


class TransactionDecoder:
    def __init__(
        self,
        coingecko_service,
        etherscan_service,
        web3_service,
    ):
        self.coingecko_service = coingecko_service
        self.etherscan_service = etherscan_service
        self.web3_service = web3_service

    def decode(
        self,
        next_tran,
        abi,
        coin_id_map,
        rates,
        currency_decimals,
        contract_volumes
    ):
        decoded = self.web3_service.decode_input(abi, next_tran["input"])
        currency = decoded["detail"][7]

        coin_id = None

        if currency == "0x0000000000000000000000000000000000000000":
            currency = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
            coin_id = "wbnb"
        else:
            if currency in coin_id_map:
                coin_id = coin_id_map[currency]

        date_str = next_tran["timestamp"].strftime("%d-%m-%Y")

        if (coin_id not in rates):
            rates[coin_id] = {}

        if (date_str not in rates[coin_id]):
            rates[coin_id][date_str] = self.coingecko_service.fetch_historic_price(
                coin_id, date_str)["usd"]

        if currency not in currency_decimals:
            currency_decimals[currency] = self.web3_service.get_currency_decimals(
                currency)

        rate = rates[coin_id][date_str]
        decimals = currency_decimals[currency]

        value = decoded["detail"][8]
        value = int(value) / math.pow(10, decimals)
        value_usd = value * rate

        contract_volume = next(
            (item for item in contract_volumes if item["date_str"] == date_str and item["address"] == next_tran["to"]), None)

        if contract_volume is None:

            contract_volume = {
                "date_str": date_str,
                "address": next_tran["to"],
                "name": self.etherscan_service.fetch_contract_name(next_tran["to"]),
                "volume": 0,
                "volume_usd": 0
            }

            contract_volumes.append(contract_volume)

        contract_volume["volume"] = contract_volume["volume"] + 1
        contract_volume["volume_usd"] = contract_volume["volume_usd"] + value_usd

        return {
            'hash': next_tran["hash"],
            'block_number': next_tran["block_number"],
            'gas_price': next_tran["gas_price"],
            'gas_used': next_tran["gas_used"],
            'nft_contract_address': next_tran["to"],
            'value': value,
            'currency': currency,
            'value_usd': value_usd,
            'timestamp': next_tran["timestamp"],
            'timestamp_unix': next_tran["timestamp_unix"],
        }
