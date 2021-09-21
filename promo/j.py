from flatten_json import flatten
import json
import os
import pandas as pd

for files in os.listdir('../promo'):
    print(files)
# from pandas.io.json import json_normalize
# json.loads is faster than pd.read_json
with open('export_20210913-1649_435_7429.json') as f:
    d = json.load(f)


# # Find every instance of Item in a Python dictionary.
# names = json_extract(d, 'Item')
# print(names)
# print("---------------------------------------")
#     df = pd.DataFrame(d)
# print(df.head(50))
# d_flattened = flatten(d)
# df = pd.DataFrame(d_flattened)
# print(df.head()) # returns Empty DataFrame
# print("---------------------------------------")
print("----------------------------------all_data-----------------------------------------")
all_data = pd.json_normalize(data=d, 
                            errors='ignore' # The errors argument defaults to 'raise’ and will raise KeyError if keys listed in meta are not always present. 
                            )
print(all_data.head())
print("--------------------------------GeneralInfo-------------------------------------------")
generalInfo = pd.json_normalize(d['GeneralInfo'])
information = pd.json_normalize(d['Information'])
print(generalInfo.head())
print("---------------------------------Information------------------------------------------")
print(information.head())
print("---------------------------------GoodsLists------------------------------------------")
information_data = pd.json_normalize(data=d['Information'], # passing the json object data path d[Information]
                            record_path=['GoodsLists'], # passing the record path within the object we wanted to parse GoodsLists
                            errors='ignore' 
                            )
print(information_data.head()) 
print("---------------------------------Prices------------------------------------------")
prices_data = pd.json_normalize(data=d['Information'], 
                            record_path=['GoodsLists','Prices'], # passing the record path within the object we wanted to parse Prices
                            errors='ignore'
                            )
print(prices_data.head())
print("---------------------------------Data------------------------------------------")
items_data = pd.json_normalize(data=d['Information'], 
                            record_path=['GoodsLists','Prices','Data'], # passing the record path within the object we wanted to parse Data
                            errors='ignore'
                            )
print(items_data.head())
print("------------------------'Data'-+-GeneralInfo-------------------------------------------------")
items_gen_data = pd.json_normalize(data=d, 
                            record_path=['Information','GoodsLists','Prices','Data'], 
                            meta=[['GeneralInfo']], # adding columns from initial json
                            errors='ignore'
                            )
print(items_gen_data.head())
print("------------------------Data-+-items_codes_data---------------------------------------------------")
items_codes_data = pd.json_normalize(data=d, 
                            record_path=['Information','GoodsLists','Prices','Data'], 
                            meta=[['Information','GoodsLists','Prices','StoreCode'],
                            ['Information','GoodsLists','DiscountType'],
                            ['Information','GoodsLists','DiscountValue'],
                            # ['Information','GoodsLists','GoodsComposition','Value'], # NaN cause it's over 1 lvl to the path item function works with
                            ],
                            errors='ignore'
                            )
items_codes_data['DateBegin'] = d['GeneralInfo']['DateBegin']
items_codes_data['DateEnd'] = d['GeneralInfo']['DateEnd']
items_codes_data['PWCcode'] = d['GeneralInfo']['PWCcode']
print(items_codes_data.head())
print("----------------------------PriceOptions+-----------------------------------------------")
priceoptions_data = pd.json_normalize(data=d, 
                            record_path=['Information','GoodsLists','PriceOptions'], 
                            meta=[
                            ['Information','GoodsLists','DiscountType'],
                            ['Information','GoodsLists','DiscountValue'],
                            ['Information','GoodsLists','GoodsComposition'],
                            # ['Information','GoodsLists','GoodsComposition','Value'], # TypeError: list indices must be integers or slices, not str 
                            ],
                            errors='ignore'
                            )
print(priceoptions_data.head())
print("------------------------------options_data--reindex-------------------------------------------")
# p_data = pd.json_normalize(data=priceoptions_data['Information.GoodsLists.GoodsComposition'], # AttributeError: 'float' object has no attribute 'values'
#                             errors='ignore'
#                             )
# print(p_data.head())
# print("---------------------------------------------------------------------------")
# if Value in df.columns
options_data = priceoptions_data.reindex(columns = ['Value','FirstValue','Operator','Information.GoodsLists.DiscountType','Information.GoodsLists.DiscountValue'])
# options_data = priceoptions_data['Value','FirstValue','Operator'] # not all columns exist !
print(options_data.head())
# else 
print("------------------------------sublist---------------------------------------------")

goods_data = pd.json_normalize(data=d,record_path=['Information','GoodsLists','GoodsComposition'],errors='ignore')
#  errors='ignore works for missing dict keys, but file 1 is missing a list, so could use hacks like https://stackoverflow.com/questions/32291437/pandas-json-normalize-produces-confusing-keyerror-message 
# but anyway pandas concat tells list comprehentions is fastest and it's the way to go
# goods_data = pd.json_normalize(data=d, 
#                             record_path=['Information','GoodsLists','GoodsComposition'],  # KeyError: 'GoodsComposition'
#                             errors='ignore'
#                             )
print(goods_data)
print("-------------------------------merge--------------------------------------------")
df = pd.merge(items_codes_data,options_data,on=['Information.GoodsLists.DiscountType','Information.GoodsLists.DiscountValue'])
print(df.head())
print("------------------------------column names---------------------------------------------")
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
'LessOrEqual'
]
print(df.head())
print("---------------------------------------------------------------------------")
# items_data.to_excel("output.xlsx")  

# df = pd.DataFrame(d)
# print(df.head(50))
# df['GoodsLists'] = df['GoodsLists'].apply(lambda x:eval(x)) # KeyError: 'GoodsLists'
# print(json_normalize(df).head(50)) # AttributeError: 'str' object has no attribute 'values'