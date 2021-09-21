import json
import os
import pandas as pd


jsonfiles = []
for files in os.listdir('../promo'):
    if '.json' in files:
        jsonfiles.append(files)
# print(jsonfiles)
 
 
def parse_element(data, column_names, store_code, general_info, sublist, file):
    di = {}
    for i, col_name in enumerate(column_names):
        di[col_name] = data[i]
    di['ObjCode'] = store_code
    di['DiscountType'] = sublist["DiscountType"]
    di['DiscountValue'] = sublist["DiscountValue"]
    di['DateBegin'] = general_info['DateBegin']
    di['DateEnd'] = general_info['DateEnd']
    di['PWCcode'] = general_info['PWCcode']
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
    di['File'] = file
    return di
 
 
def parse_json():
    dfs = []
    for file in jsonfiles:
        try:
            with open(file) as f:
                d = json.load(f)
            for sublist in d['Information']['GoodsLists']:
                for prices in sublist['Prices']:
                    dfs.append(pd.DataFrame([parse_element(data, 
                                                        prices['ColumnsName'], 
                                                        prices["StoreCode"], 
                                                        d['GeneralInfo'], 
                                                        sublist,
                                                        file)
                                for data in prices['Data']]))
            # print("---------------------------------------------------------------------------")
        except Exception as e:
            print(file)
            print(e)
    df = pd.concat(dfs, ignore_index=True)
    # print(df.head(50))
    return df

res_df = parse_json()
# print(res_df.head())
# print(res_df.info())
res_df.to_excel("result.xlsx")