from blockfrost import ApiUrls, BlockFrostApi
import json

LOVELACE_PER_ADA = 1_000_000
NETWORK_URL = "https://cardano-preview.blockfrost.io/api"

# Get config options
with open("config.json", "r") as f:
    raw_config = f.read()
config = json.loads(raw_config)

# Set up blockfrost api
api = BlockFrostApi(project_id=config["blockfrost_key"], base_url=NETWORK_URL)

# Get addresses that have sent Ada
address = api.address(config["payment_address"])
for amount in address.amount:
    print(amount)
