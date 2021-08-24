import requests
import csv
import json
import pandas as pd
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import time

DataToProcess = []
FinalData = []

def SendDataRequest(alldatatoprocess):
    ProcessData = alldatatoprocess['Processor']
    LogBytesData = alldatatoprocess['LogBytes']
    DiskReadsData = alldatatoprocess['DiskRead']
    DiskWritesData = alldatatoprocess['DiskWrite']
    for (p,l,dw,dr) in zip(ProcessData,LogBytesData,DiskWritesData,DiskReadsData):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        params = (
            ('cores', '16'),
        )
        combinedData = [{'diskReads':dr,
                        'diskWrites':dw,
                        'logBytesFlushed':l,
                        'processorTime':p
                    }]
        response = requests.post('https://dtucalculator.azurewebsites.net/api/calculate', headers=headers, params=params, json=combinedData)
        json_data = json.loads(response.content)
        ServiceTierData = json_data['SelectedServiceTiers']
        for each in ServiceTierData:
            FinalData.append({
                'Processor Time':p,
                'LogBytesFlushedSec':l,
                'DiskWrites':dw,
                'DiskReads':dr,
                'CPU-DTU-Value':each['CpuServiceTier']['SelectedLevel']['Dtu'],
                'CPU-True-DTU-Value':each['CpuServiceTier']['DtuValue'],
                'CPU-DTU-Name':each['CpuServiceTier']['SelectedLevel']['Name'],
                'IOP-DTU-Value':each['IopsServiceTier']['SelectedLevel']['Dtu'],
                'IOP-True-DTU-Value':each['IopsServiceTier']['DtuValue'],
                'IOP-DTU-Name':each['IopsServiceTier']['SelectedLevel']['Name'],
                'LogBytes-DTU-Value':each['LogServiceTier']['SelectedLevel']['Dtu'],
                'LogBytes-True-DTU-Value':each['LogServiceTier']['DtuValue'],
                'LogBytes-DTU-Name':each['LogServiceTier']['SelectedLevel']['Name'],
                'TotalServiceTierName':each['TotalServiceTier']['SelectedLevel']['Dtu']
            })




def ReadCSVData():
    with open('SQLPerformance.csv', 'r') as data:
        file = csv.DictReader(data)
        for col in file:
            DataToProcess.append({
                'Processor':col['Processor'],
                'LogBytes':col['LogBytes'],
                'DiskRead':col['DiskRead'],
                'DiskWrite':col['DiskWrite']
            })  



start_time = time.time()

ReadCSVData()

if __name__ == '__main__':
    pool = ThreadPoolExecutor()
    with ThreadPoolExecutor() as exec:
        exec.map(SendDataRequest,DataToProcess)




df = pd.DataFrame(FinalData)
df.to_csv('CompletedParse.csv')
print("--- %s seconds ---" % (time.time() - start_time))

