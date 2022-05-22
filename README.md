# nahmii2csv.py

Parses swaps, liquidity mining and airdrops from Nahmii v2 and converts it to CSV, especially formatted for kryptosekken.no for tax calculations.

## Usage

```
$ python3 nahmii2csv.py <wallet address>
Tidspunkt,Type,Inn,Inn-Valuta,Ut,Ut-Valuta,Gebyr,Gebyr-Valuta,Marked,Notat
2021-12-13 10:48:14,Handel,0.04,WBTC,100000.0,NII,0.00038065792,ETH,NiiFi,Swap,
2021-12-14 17:13:14,Handel,1.2389102,NIIFI-WBTCNII,0.04,WBTC,0.00052652906,ETH,NiiFi,Add liquidity,
2021-12-14 17:13:14,Handel,1.2389102,NIIFI-WBTCNII,224875.870,NII,0.0005146315,ETH,NiiFi,Add liquidity,
2021-12-15 12:11:45,Renteinntekt,13606.26786322117,NIIFI,,,,,NiiFi,Airdrop: Liquidity Mining,
```
