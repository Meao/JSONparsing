from flatten_json import flatten
import json
import os
import pandas as pd
# for files in os.listdir('../promo'):
#     print(files)
with open('export_20210913-1652_792_7129.json') as f:
    d = json.load(f)
flat_list = []
for sublist in d['Information']['GoodsLists']:
    for prices in sublist['Prices']:
        new_list = []
        for data in prices['Data']:
            di = {}
            for i, col_name in enumerate(prices['ColumnsName']):
                # print("i, col_name", i, col_name)
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
            # print('di', di)
            # print('data', data)
            new_list.append(di)
            # print('*')
        # print('new_list', new_list)
        # print('*')
        flat_list.extend(new_list)
    # print('flat_list', flat_list)
    # print('sublist', sublist)
    # print('*')


print("---------------------------------------------------------------------------")

# print(df.head())
# print("---------------------------------------------------------------------------")
# items_data.to_excel("output.xlsx")  

df = pd.DataFrame(flat_list)
print(df.head(50))
# df['GoodsLists'] = df['GoodsLists'].apply(lambda x:eval(x)) # KeyError: 'GoodsLists'
# print(json_normalize(df).head(50)) # AttributeError: 'str' object has no attribute 'values'