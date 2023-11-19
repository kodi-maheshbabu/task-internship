import pandas as pd
def strategy(data):
    p = 0
    pos = None
    l_p = 0.5 / 100    
    for index, row in data.iterrows():
        timestamp = pd.to_datetime(row['Timestamp'])
        op = row['Open']
        hp = row['High']
        lp = row['Low']
        cp = row['Close']
        if timestamp.time() >= pd.to_datetime('09:15:00').time() and timestamp.time() <= pd.to_datetime('09:30:00').time():
            if hp > op:
                if pos is None:
                    pos = {'type': 'buy', 'entry_price': hp, 'stop_loss': op * (1 - l_p)}
                else:
                    if pos['stop_loss']< op * (1 - l_p):
                        pos = {'type': 'buy', 'entry_price': hp, 'stop_loss': op * (1 - l_p)}
            elif lp < op:
                if pos is None:
                    pos = {'type': 'sell', 'entry_price': lp, 'stop_loss': op * (1 + l_p)}
                else:
                    if pos['stop_loss'] < op * (1 + l_p):
                        pos = {'type': 'sell', 'entry_price': lp, 'stop_loss': op * (1 + l_p)}
        elif pos is not None:
            if pos['type'] == 'buy' and lp < pos['stop_loss']:
                p += pos['entry_price'] - pos['stop_loss']
                pos = None
            elif pos['type'] == 'sell' and hp > pos['stop_loss']:
                p += pos['entry_price'] - pos['stop_loss']
                pos = None
            elif timestamp.time() >= pd.to_datetime('15:15:00').time():
                if pos['type'] == 'buy':
                    p += cp - pos['entry_price']
                elif pos['type'] == 'sell':
                    p += pos['entry_price'] - cp
                pos = None
    return p
file_path = 'data.csv'  
b_data = pd.read_csv(file_path)
print(b_data)
b_data['Timestamp'] = pd.to_datetime(b_data['Date']+" "+b_data['Timestamp'])
b_data = b_data[(b_data['Timestamp'].dt.year == 2020)]
p_2020 = strategy(b_data)
print("Profit and Loss for 2020:", p_2020)
