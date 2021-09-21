import json
import os
import pandas as pd
jsonfiles = []
for files in os.listdir('../promo'):
    # print(files)
    if '.json' in files:
        jsonfiles.append(files)
print(jsonfiles)
for file in jsonfiles:
    try:
        with open(file) as f:
            d = json.load(f)

        items_data = pd.json_normalize(data=d, 
                                    record_path=['Information','GoodsLists','Prices','Data'], 
                                    meta=[['Information','GoodsLists','Prices','StoreCode'],
                                    ['Information','GoodsLists','DiscountType'],
                                    ['Information','GoodsLists','DiscountValue'],
                                    # ['GeneralInfo','DateBegin'],
                                    # ['GeneralInfo','DateEnd'],
                                    # ['GeneralInfo','PWCcode'],
                                    ['Information','GoodsLists','PriceOptions','Value'],
                                    ['Information','GoodsLists','PriceOptions','FirstValue'],
                                    ['Information','GoodsLists','PriceOptions','Operator']
                                    ],
                                    errors='ignore'
                                    )
        # print(items_data.head())
        print("---------------------------------------------------------------------------")
        items_data.columns = ['Item',
        'SalePriceBeforePromo',
        'SalePriceTimePromo',
        'DatePriceBeforePromo',
        'ObjCode',
        'DiscountType',
        'DiscountValue',
        # 'DateBegin',
        # 'DateEnd',
        # 'PWCcode',
        'Value',
        'FirstValue',
        'LessOrEqual']
        items_data['File'] = file
        items_data['DateBegin'] = d['GeneralInfo']['DateBegin']
        items_data['DateEnd'] = d['GeneralInfo']['DateEnd']
        items_data['PWCcode'] = d['GeneralInfo']['PWCcode']
        print(items_data.head())
        print("---------------------------------------------------------------------------")
    except:
        print(file)

# df.to_excel("result.xlsx")  