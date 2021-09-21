import json
import os
import pandas as pd
jsonfiles = []
for files in os.listdir('../promo'):
    if '.json' in files:
        jsonfiles.append(files)
print(jsonfiles)
def parse_json(file):
    with open(file) as f:
        d = json.load(f)

    flat_list = []
    for sublist in d['Information']['GoodsLists']:
        for prices in sublist['Prices']:
            new_list = []
            for data in prices['Data']:
                di = {}
                for i, col_name in enumerate(prices['ColumnsName']):
                    di[col_name] = data[i]
                di['ObjCode'] = prices["StoreCode"]
                di['DiscountType'] = sublist["DiscountType"]
                di['DiscountValue'] = sublist["DiscountValue"]
                di['DateBegin'] = d['GeneralInfo']['DateBegin']
                di['DateEnd'] = d['GeneralInfo']['DateEnd']
                di['PWCcode'] = d['GeneralInfo']['PWCcode']
                if 'GoodsComposition' in sublist:
                    di['Value'] = sublist['GoodsComposition'][0]['Value']
                elif sublist['PriceOptions'] is not None:
                    if 'Value' in sublist['PriceOptions'][0]:
                        di['Value'] = sublist['PriceOptions'][0]['Value']
                    else:
                        di['Value'] = None
                else:
                    di['Value'] = None
                if sublist['PriceOptions'] is not None:
                    if 'FirstValue' in sublist['PriceOptions'][0]:
                        di['FirstValue'] = sublist['PriceOptions'][0]['FirstValue']
                    else:
                        di['FirstValue'] = None
                else:
                    di['FirstValue'] = None
                if sublist['PriceOptions'] is not None:
                    if 'Operator' in sublist['PriceOptions'][0]:
                        di['LessOrEqual'] = sublist['PriceOptions'][0]['Operator']
                    else:
                        di['LessOrEqual'] = None
                else:
                    di['LessOrEqual'] = None
                new_list.append(di)
            flat_list.extend(new_list)
    print("---------------------------------------------------------------------------")

    df = pd.DataFrame(flat_list)
    print(df.head(50))

for file in jsonfiles:
    try:
        parse_json(file)
    except:
        print(file)

# df.to_excel("result.xlsx")  