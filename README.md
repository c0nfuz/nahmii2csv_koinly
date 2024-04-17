# nahmii2csv_koinly.py

Parses swaps, liquidity mining, airdrops and Kiwii NFT Minting from Nahmii v2 and converts it to CSV, especially formatted for koinly.com for tax calculations (instead of kryptosekken.no - used by original Nahmii2csv https://github.com/dsolstad/nahmii2csv).

## Usage

Update the walletAddress inside the script.

```
$ python3 nahmii2csv_koinly.py
Fetching from wallet address: 0x1219A412820B9dde2c9122Be13528113eF6bf222
To use other wallet address, update walletAddress in script or use: $ python3 nahmii2csv_koinly.py <wallet address>
Date,TxHash,Received Amount,Received Currency,Sent Amount,Sent Currency,Fee Amount,Fee Currency,Description,Tag
2021-11-11 12:01:31,0xeca4b654ac654c65c46a46c54bc65b4a4c46c5a4c565c4c767c6c8c8a8882341,122.3,LP1,700000.0,NII,0.000536202925,ETH,NiiFi,Liquidity in,
2021-11-11 12:01:31,0xeca4b654ac654c65c46a46c54bc65b4a4c46c5a4c565c4c767c6c8c8a8882341,122.2,LP1,90000.182,NIIFI,0,ETH,NiiFi,Liquidity in,
```

or run with:
```
$ python3 nahmii2csv_koinly.py <wallet address>
Fetching from wallet address: 0x1219A432820B9dde3c9122Be13528113eF6bf222
Date,TxHash,Received Amount,Received Currency,Sent Amount,Sent Currency,Fee Amount,Fee Currency,Description,Tag
2021-11-11 12:01:31,0xeca4b654ac654c65c46a46c54bc65b4a4c46c5a4c565c4c767c6c8c8a8882341,122.3,LP1,700000.0,NII,0.000536202925,ETH,NiiFi,Liquidity in,
2021-11-11 12:01:31,0xeca4b654ac654c65c46a46c54bc65b4a4c46c5a4c565c4c767c6c8c8a8882341,122.2,LP1,90000.182,NIIFI,0,ETH,NiiFi,Liquidity in,
```

## Kiwii NFT Minting

The cost of minting an egg is by default 0.2 ETH, which is hardcoded in this script. If you payed less, e.g. being on the whitelist, you need to edit this in the script, or change it in the output.

## Trusted Bridge

The Nahmii team opened a trusted bridge where you could transfer nii tokens from nahmii mainnet v1 to v2. If you did this, then you had to leave 1000 nii on v1 (by design) and you would receive 1000 extra NII on v2. You also had to pay a fee of 0.5% of the total amount transferred.

nahmii2csv handles this transaction as a normal transaction of receiving 1000 nii with a fee of 0.5%. This works given that you have tracked activity on Nahmii v1 manually. 

Example: You transferred 10000 NII to the trusted bridge, and after paying 0.5% fee you got 9950 NII plus the 1000 extra, 10950 NII in total. Since it's not possible to know the original amount sent from Nahmii v1 to exactly know how much you payed in fee, we calculate 0.502513% of the amount received, which is very close to accurate.


| Description     | Calc                | Sum  |
| --------------- |:-------------------:| -----:|
| Received        | 10000 x (1 - 0.005) | 9950 |
| Fee payed       | 9950 × 0.00502513   | 50.0000435 |
| Original amount | 9950 x 1.00502513   | 10000.0000435 |

The entry will look like the following in CSV:
```
2022-03-11 23:16:08,0xda176396b61663b29306c30e8b2bb6a4bc8b39e95e17936c87b696a58ae74655,1000,NII,,,3152.48240,NII,NiiFi,Trusted Bridge Transfer,
```

Note: The Trusted Bridge was mostly complete at 2022/06/17, but a few transfers were still not complete. You need to edit the script if you received the funds from the trusted bridge at a later stage.

Read more about the Trusted Bridge:  
https://blog.nahmii.io/nahmii-1-0-to-nahmii-2-0-trusted-bridge-announced-661c0cac339  
https://blog.nahmii.io/nahmii-1-0-to-nahmii-2-0-trusted-bridge-payments-completed-e1b4bc1fc0b0

## Disclaimer
Please verify each transaction manually as nahmii2csv_koinly provide no guarentee that everything is correct.
