# backend/blockchain/blockchain_interaction.py

from web3 import Web3
import json

# Connect to Ethereum blockchain (use Infura, Alchemy, or local Ganache)
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura/Alchemy/Ganache RPC URL
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum blockchain")
else:
    print("Failed to connect to Ethereum blockchain")

# Contract details
contract_address = "0xYourSmartContractAddress"  # Replace with deployed contract address
with open("contract_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to register intellectual property
def register_ip(ip_hash, sender_address, private_key):
    nonce = web3.eth.get_transaction_count(sender_address)
    txn = contract.functions.registerIP(ip_hash).build_transaction({
        'from': sender_address,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)

# Function to verify intellectual property
def verify_ip(ip_hash):
    owner, timestamp = contract.functions.verifyIP(ip_hash).call()
    return {"owner": owner, "timestamp": timestamp}

# Example usage
if __name__ == "__main__":
    ip_hash_example = "QmExampleHash"
    result = verify_ip(ip_hash_example)
    print(f"Owner: {result['owner']}, Timestamp: {result['timestamp']}")
