import requests
import pandas as pd

Data = []

def SendDataRequest():

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    params = (
        ('cores', '16'),
    )
    data = '[ { "diskReads": {}}, "diskWrites": {}}, "logBytesFlushed": {}}, "processorTime": {}} } ]'.format()
    response = requests.post('https://dtucalculator.azurewebsites.net/api/calculate', headers=headers, params=params, data=data)

    print(response.content)
    with open('data.json', 'wb') as f:
        f.write(response.content)


col_list = ['Seconds','Processor','DiskRead','DiskWrite','LogBytes']
df = pd.read_csv('SQLPerformance.csv',usecols=col_list)

Data.append({
    'Processor':df["Processor"]
})

print(Data)