# github.com/c0nfuz/nahmii2csv_koinly
import urllib.request
import datetime
import json
import sys
import re

walletAddress = ""
symbols = ['NIIFI-NIINIIFI','NIIFI-WBTCNII','NIIFI-NIIETH','NIIFI-ETHNII']

if len(sys.argv) == 1:
    walletAddress = "0x8219A4a2820B9dde2c9124Ae13528113eF3bc212"
    print ("Fetching from wallet address: " + walletAddress)
    print ("To use other wallet address, update walletAddress in script or use: python3 nahmii2csv.py <wallet address>")
    #sys.exit(1)
else:
    print ("Fetching from wallet address: " + sys.argv[1])
    walletAddress = sys.argv[1]

def fixnum(n): return float(str(n).replace(',',''))

csv = []

# Swaps and Liquidity Mining
r = urllib.request.urlopen('https://explorer.nahmii.io/api?module=account&sort=asc&action=txlist&address=' + walletAddress)

for tx in json.loads(r.read())['result']:

    gas = int(tx['gas']) * int(tx['gasPrice']) / (10**18)
    time = datetime.datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')

    r = urllib.request.urlopen('https://explorer.nahmii.io/tx/' + tx['hash'] + '/token-transfers?type=JSON')
    html = ''.join(json.loads(r.read())['items'])

    tokens = re.findall(r'class=\"tile-title\">\s*?(\S+)\s*?<a.*? href=\"/token/(.*?)\">(.*?)</a', str(html), re.M|re.I)
    #print (tx['hash'])
    #for t in tokens: print (t)

    # Skipping burning of non-LP associated tokens and non-swap transfers
    if len(tokens) < 2: continue
    
    

    if html.find('Token Minting') != -1:
        x = {'out1_sym': tokens[0][2], 'out1': fixnum(tokens[0][0]),
             'out2_sym': tokens[1][2], 'out2': fixnum(tokens[1][0]),
             'in_sym': (tokens[2][2].replace('V1','') + tokens[0][2] + tokens[1][2]),
             'in': "{:.18f}".format(fixnum(tokens[2][0])/2)}
     
        # Added by C0nfuz to change value of LP-token to LP1,LP2,LP3 etc (required by Koinly) 
        
        tempsym = x['in_sym']
        if x['in_sym'] in symbols:
            index = symbols.index(x['in_sym'])
            x['in_sym'] = 'LP' + str(index + 1)
        else:
            symbols.append(x['in_sym'])
            x['in_sym'] = 'LP' + str(len(symbols))
            
        # Required to put NIIETH and ETHNII into the same pool    
        match tempsym:
                case 'NIIFI-NIIETH':
                    x['in_sym'] = 'LP3'
                case 'NIIFI-ETHNII':
                    x['in_sym'] = 'LP3'
                
        # End of added by C0nfuz to change value of LP-token to LP1,LP2,LP3 etc (required by Koinly) 

        csv.append([time, tx['hash'], x['in'], x['in_sym'], x['out1'], x['out1_sym'], gas, 'ETH', 'NiiFi', 'Liquidity in'])
        csv.append([time, tx['hash'], x['in'], x['in_sym'], x['out2'], x['out2_sym'], 0, 'ETH', 'NiiFi', 'Liquidity in'])
        #print ("Added %s %s and %s %s got %s %s" % (x['t1_amount'], x['t1'], x['t2_amount'], x['t2'], x['in_t'], x['in_amount']))

    elif html.find('Token Burning') != -1:
        x = {'in1_sym': tokens[2][2], 'in1': fixnum(tokens[2][0]),
             'in2_sym': tokens[3][2], 'in2': fixnum(tokens[3][0]),
             'out_sym': tokens[0][2].replace('V1','') + tokens[2][2] + tokens[3][2],
             'out': "{:.18f}".format(fixnum(tokens[0][0])/2)}
        
                
        # Added by C0nfuz to change value of LP-token to LP1,LP2,LP3 etc (required by Koinly) 
        tempsym = x['out_sym']
        if x['out_sym'] in symbols:
            index = symbols.index(x['out_sym'])
            x['out_sym'] = 'LP' + str(index + 1)
            
        else:
            symbols.append(x['in_sym'])
            x['out_sym'] = 'LP' + str(len(symbols))
        
        # Required to put NIIETH and ETHNII into the same pool    
        match tempsym:
                case 'NIIFI-NIIETH':
                    x['out_sym'] = 'LP3'
                case 'NIIFI-ETHNII':
                    x['out_sym'] = 'LP3'
                    
        # End of added by C0nfuz to change value of LP-token to LP1,LP2,LP3 etc (required by Koinly)
                
        
        csv.append([time, tx['hash'], x['in1'], x['in1_sym'], x['out'], x['out_sym'], gas, 'ETH', 'NiiFi', 'Liquidity out'])
        csv.append([time, tx['hash'], x['in2'], x['in2_sym'], x['out'], x['out_sym'], 0, 'ETH', 'NiiFi', 'Liquidity out'])
        #print ("Removed %s %s and %s %s returned %s %s" % (x['in1'], x['in1_sym'], x['in2'], x['in2_sym'], x['out_sym'], x['out']))

    elif html.find('Token Transfer') != -1:
        x = {'out_sym': tokens[0][2], 'out': fixnum(tokens[0][0]), 'in_sym': tokens[1][2], 'in': fixnum(tokens[1][0])}
        csv.append([time, tx['hash'], x['in'], x['in_sym'], x['out'], x['out_sym'], gas, 'ETH', 'NiiFi', 'Swap'])
        #print ("Swapped %s %s to %s %s" % (x['out'], x['out_sym'], x['in'], x['in_sym']))


team_fund = "0xe8575e787e28bcb0ee3046605f795bf883e82e84"
airdrop_contract = "0x7c32460499575481d8179fa74e8f95414e6be213"

# niifi Airdrops
niifi = "0x604efd2Ec4afc77ba9827685ecad54c8edca041b"
r = urllib.request.urlopen("https://explorer.nahmii.io/api?module=account&action=tokentx&address=" + walletAddress + "&contractaddress=" + niifi)

for tx in json.loads(r.read())['result']:
    if tx['from'] in (team_fund, airdrop_contract):
        amount = fixnum(tx['value']) / (10**15)
        time = datetime.datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
        csv.append([time, tx['hash'], amount, 'NIIFI', '', '', '', '', 'NiiFi', 'Airdrop'])


# nii Airdrops
nii = "0x595DBA438a1bf109953F945437c1584319515d88"
r = urllib.request.urlopen("https://explorer.nahmii.io/api?module=account&action=tokentx&address=" + walletAddress + "&contractaddress=" + nii)

for tx in json.loads(r.read())['result']:
    if tx['from'] in (team_fund, airdrop_contract):
        amount = fixnum(tx['value']) / (10**15)
        time = datetime.datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d')

        # If trusted bridge
        if date == '2022-06-17':
            #csv.append([time, 'Overføring-Inn', amount, 'NII', '', '', '', '', 'NiiFi', 'Trusted Bridge Transfer'])
            fee = amount * 0.00502513 # ~0.5% fee
            csv.append([time, tx['hash'], '1000', 'NII', '', '', fee, 'NII', 'NiiFi', 'Trusted Bridge Transfer'])
        else:
            csv.append([time, tx['hash'], amount, 'NII', '', '', '', '', 'NiiFi', 'Airdrop'])


# Kiwii NFT Minting
kiwii = "0xac4f2f204b38390b92d0540908447d5ed352799a"
r = urllib.request.urlopen("https://explorer.nahmii.io/api?module=account&action=tokentx&address=" + walletAddress + "&contractaddress=" + kiwii)

uniqhashes = {}
for tx in json.loads(r.read())['result']:

    gas = int(tx['gas']) * int(tx['gasPrice']) / (10**18)
    time = datetime.datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')

    # Add gas only for once for each unique tx hash
    if tx['hash'] not in uniqhashes:
        uniqhashes[tx['hash']] = 1
        csv.append([time, tx['hash'], 1, 'KWE-' + tx['tokenID'], '0.2', 'ETH', gas, 'ETH', 'KiwiiEggs', 'NFT Minting'])
    else:
        csv.append([time, tx['hash'], 1, 'KWE-' + tx['tokenID'], '0.2', 'ETH', '', 'ETH', 'KiwiiEggs', 'NFT Minting'])


# Print CSV
print ('Date,TxHash,Received Amount,Received Currency,Sent Amount,Sent Currency,Fee Amount,Fee Currency,Description,Tag', end='')
#print ('Tidspunkt,Type,Inn,Inn-Valuta,Ut,Ut-Valuta,Gebyr,Gebyr-Valuta,Marked,Tag', end='')

for row in csv:
    print("\n", end='')
    for i in row:
        print(i, end='')
        print(',', end='')
print("")
