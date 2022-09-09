from blockfrost import ApiUrls, BlockFrostApi
import json

LOVELACE_PER_ADA = 1_000_000
NETWORK_URL = "https://cardano-preview.blockfrost.io/api"

# Get config options
with open("config.json", "r") as f:
    raw_config = f.read()
config = json.loads(raw_config)

# Read in the KYC file
kyc_addresses = set()
with open(config["kyc_file"], "r") as f:
    next(f)
    for line in f:
        [address, _] = line.split(",")
        kyc_addresses.add(address)

# Set up blockfrost api
api = BlockFrostApi(project_id=config["blockfrost_key"], base_url=NETWORK_URL)

# Get addresses that have sent Ada
addresses = {}
utxos = api.address_utxos(address=config["payment_address"])
for utxo in utxos:
    tx_hash = utxo.tx_hash
    in_utxos = api.transaction_utxos(hash=tx_hash).inputs
    address = in_utxos[0].address
    amount = utxo.amount[0].quantity

    addresses.setdefault(address, 0)
    addresses[address] += int(amount)

# Write output file
lovelace_per_token = LOVELACE_PER_ADA * config["ada_per_token"]
with open(config["output_file"], "w") as f:
    f.write("Address,Lovelace Paid,Tokens Owed,Is KYC\n")
    for address, lovelace in addresses.items():
        tokens = int(lovelace / lovelace_per_token)
        is_kyc = "NO"
        if address in kyc_addresses:
            is_kyc = "YES"

        f.write(f"{address},{lovelace},{tokens},{is_kyc}\n")
