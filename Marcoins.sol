// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Marcoins is ERC20, Ownable {
    constructor(uint256 initialSupply) ERC20("MARCOINS", "MARCO") {
        _mint(address(0x34Cc4e3F424a4802260EC8F4089AA09C30491a1F), initialSupply * 10 / 100);
        _mint(address(0x680Dc4b2148Dc6B5d1d6E41358d2F1A09fea4f4B), initialSupply * 20 / 100);
        _mint(address(0x5766a8334a7E8f7F8d47e7EDaa00A6C0330A93cC), initialSupply * 50 / 100);
        _mint(address(0x2a2d585Aaf4E937fC1D66788762837f68105F4DF), initialSupply * 20 / 100);
    }

    function mint(address _to, uint256 _amount) public onlyOwner {
        _mint(_to, _amount);
    }
}