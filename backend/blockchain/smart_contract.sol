// backend/blockchain/smart_contract.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IntellectualPropertyRegistry {
    struct IPRecord {
        string hash; // Hash of the content (image, text, etc.)
        address owner;
        uint256 timestamp;
    }

    mapping(string => IPRecord) private ipRecords;
    event IPRegistered(string hash, address owner, uint256 timestamp);

    function registerIP(string memory _hash) public {
        require(ipRecords[_hash].timestamp == 0, "IP already registered");

        ipRecords[_hash] = IPRecord({
            hash: _hash,
            owner: msg.sender,
            timestamp: block.timestamp
        });

        emit IPRegistered(_hash, msg.sender, block.timestamp);
    }

    function verifyIP(string memory _hash) public view returns (address, uint256) {
        require(ipRecords[_hash].timestamp != 0, "IP not found");
        return (ipRecords[_hash].owner, ipRecords[_hash].timestamp);
    }
}
