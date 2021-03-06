import csv
import json
import math
import os

from xlsxwriter import Workbook

import utils
import xlscolumn
from dashreq import get_dash_data, get_dash_req

dashrequest = get_dash_req()
for r in dashrequest['requests']:
    print(r['id'], r['queryName'])
# print(json.dumps(dashrequest, indent=4, sort_keys=True))
# exit()
sheets = list(map(lambda x: x['queryName'], dashrequest['requests']))

dashjson = get_dash_data()
datas = list(map(lambda x: x['data'], dashjson))
# datas = list(range(len(sheets)))

sheet2data = utils.group_sheet_data(sheets, datas)

deadPatientsPerDate = [data for sheetname, data in sheet2data if sheetname == 'deadPatientsPerDate']
if len(deadPatientsPerDate) > 0:
    sheet2data.append(('deadWeekly_computed', utils.computeWeekly(deadPatientsPerDate[0])))
    sheet2data.append(('deadDelta_computed', utils.computeDelta(deadPatientsPerDate[0], 'out/csv/deadPatientsPerDate.csv')))

os.makedirs('out', exist_ok=True)
os.makedirs('out/csv', exist_ok=True)
with open('out/covid.csv', 'w') as csvall:
    with Workbook('out/covid.xlsx') as workbook:
        for i, (sheetname, data) in enumerate(sheet2data):
            data, fields = utils.data2fields(data)
            print(i, sheetname, fields)

            xlscolumn.write_data_worksheet(data, fields, workbook, sheetname)

            with open('out/csv/' + sheetname + '.csv', 'w') as csvfile:
                utils.writeToCsv(data, fields, csvfile)

            print(f'{("-" * len(sheetname))}\n{sheetname}\n{("-" * len(sheetname))}', file=csvall)
            utils.writeToCsv(data, fields, csvall)
            print('\n', file=csvall)
