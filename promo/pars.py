import json
import os
import pandas as pd
jsonfiles = []
for files in os.listdir('../promo'):
    # print(files)
    if '.json' in files:
        jsonfiles.append(files)
print(jsonfiles)
def parse_json(file):
    with open(file) as f:
        d = json.load(f)

    items_data = pd.json_normalize(data=d, 
                                record_path=['Information','GoodsLists','Prices','Data'], 
                                meta=[['Information','GoodsLists','Prices','StoreCode'],
                                ['Information','GoodsLists','DiscountType'],
                                ['Information','GoodsLists','DiscountValue']
                                ],
                                errors='ignore'
                                )
    items_data['DateBegin'] = d['GeneralInfo']['DateBegin']
    items_data['DateEnd'] = d['GeneralInfo']['DateEnd']
    items_data['PWCcode'] = d['GeneralInfo']['PWCcode']
    priceoptions_data = pd.json_normalize(data=d, 
                                record_path=['Information','GoodsLists','PriceOptions'], 
                                meta=[
                                ['Information','GoodsLists','DiscountType'],
                                ['Information','GoodsLists','DiscountValue']
                                ],
                                errors='ignore'
                                )
    # print(priceoptions_data.head())
    options_data = priceoptions_data.reindex(columns = ['Value','FirstValue','Operator','Information.GoodsLists.DiscountType','Information.GoodsLists.DiscountValue'])
    df = pd.merge(items_data,options_data,on=['Information.GoodsLists.DiscountType','Information.GoodsLists.DiscountValue'])
    # print(df.head())
    print("---------------------------------------------------------------------------")
    df.columns = ['Item',
    'SalePriceBeforePromo',
    'SalePriceTimePromo',
    'DatePriceBeforePromo',
    'ObjCode',
    'DiscountType',
    'DiscountValue',
    'DateBegin',
    'DateEnd',
    'PWCcode',
    'Value',
    'FirstValue',
    'LessOrEqual']
    df['File'] = file
    print(df.head())
    print("---------------------------------------------------------------------------")
    # convert NaN to None
    # convert types of data in some price columns?

for file in jsonfiles:
    try:
        parse_json(file)
    except:
        print(file)

# df.to_excel("result.xlsx")  