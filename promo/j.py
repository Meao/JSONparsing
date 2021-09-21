from flatten_json import flatten
import json
import os
import pandas as pd
for files in os.listdir('../promo'):
    print(files)
# from pandas.io.json import json_normalize
# json.loads is faster than pd.read_json
with open('export_20210913-1650_520_2670.json') as f:
    d = json.load(f)

# def json_extract(obj, key):
#     """Recursively fetch values from nested JSON."""
#     arr = []

#     def extract(obj, arr, key):
#         """Recursively search for values of key in JSON tree."""
#         if isinstance(obj, dict):
#             for k, v in obj.items():
#                 if isinstance(v, (dict, list)):
#                     extract(v, arr, key)
#                 elif k == key:
#                     arr.append(v)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract(item, arr, key)
#         return arr

#     values = extract(obj, arr, key)
#     return values

# # Find every instance of `Item ` in a Python dictionary.
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
                            # ['Information','GoodsLists','GoodsComposition','Value'], # NaN
                            # ['GeneralInfo','DateBegin'],
                            # ['GeneralInfo','DateEnd'],
                            # ['GeneralInfo','PWCcode'],
                            # ['Information','GoodsLists','PriceOptions','Value'],
                            # ['Information','GoodsLists','PriceOptions','FirstValue'],
                            # ['Information','GoodsLists','PriceOptions','Operator']
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
                            # ['Information','GoodsLists','Prices','StoreCode'],
                            ['Information','GoodsLists','DiscountType'],
                            ['Information','GoodsLists','DiscountValue'],
                            ['Information','GoodsLists','GoodsComposition'],
                            # ['Information','GoodsLists','GoodsComposition','Value'], # TypeError: list indices must be integers or slices, not str ?????????????????????
                            # # ['GeneralInfo','DateBegin'],
                            # # ['GeneralInfo','DateEnd'],
                            # # ['GeneralInfo','PWCcode'],
                            # ['Information','GoodsLists','PriceOptions','Value'],
                            # ['Information','GoodsLists','PriceOptions','FirstValue'],
                            # ['Information','GoodsLists','PriceOptions','Operator']
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
for sublist in d['Information']['GoodsLists']:
    # print('sublist', sublist)
    if 'GoodsComposition' in sublist:
        print('y')
#     new_list = [item for item in sublist['values']]
#     print('new_list', new_list)
# goods_data = d['Information']['GoodsLists'][1]['GoodsComposition']
# goods_data = pd.json_normalize(data=d['Information'],  # KeyError: 'GoodsComposition'
#                             record_path=['GoodsLists','GoodsComposition','GoodsCode'],
#                             errors='ignore'
#                             )
# goods_data = pd.json_normalize(data=d['Information']['GoodsLists'],   # KeyError: 'GoodsComposition'
#                             record_path=['GoodsComposition'],
#                             errors='ignore'
#                             )
# goods_data = pd.json_normalize(data=d['Information']['GoodsLists'][1],  # only shows value for the 1st list of prices
#                             record_path=['GoodsComposition','GoodsCode'],
#                             meta=[
#                             ['GoodsComposition','Value'],
#                             ],
#                             errors='ignore'
#                             )
# goods_data = pd.json_normalize(data=d['Information']['GoodsLists'][1], 
#                             record_path=['GoodsComposition'],
#                             errors='ignore'
#                             )
# goods_data = pd.json_normalize(data=d, 
#                             record_path=['Information','GoodsLists',1,'GoodsComposition'],  # KeyError: 1
#                             errors='ignore'
#                             )
goods_data = pd.json_normalize(data=d,record_path=['Information','GoodsLists','GoodsComposition'],errors='ignore')
# it seems like errors='ignore does not work :(
# goods_data = pd.json_normalize(data=d, 
#                             record_path=['Information','GoodsLists','GoodsComposition'],  # KeyError: 'GoodsComposition'
#                             errors='ignore'
#                             )
print(goods_data)
print("-------------------------------merge--------------------------------------------")
df = pd.merge(items_codes_data,options_data,on=['Information.GoodsLists.DiscountType','Information.GoodsLists.DiscountValue'])
print(df.head())
print("------------------------------column names---------------------------------------------")
# items_data.rename(columns={0: 'Item', 1: 'SalePriceBeforePromo', 2:'SalePriceTimePromo', 3:'DatePriceBeforePromo'},inplace=True)
# print(items_data.head())
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

# print(items_data.columns)
# prices_data = pd.json_normalize(data=information_data['Prices'], 
#                             record_path=['StoreCode'], 
#                             errors='ignore'
#                             )
# print(prices_data.head()) 

# df = pd.DataFrame(d)
# print(df.head(50))
# df['GoodsLists'] = df['GoodsLists'].apply(lambda x:eval(x)) # KeyError: 'GoodsLists'
# print(json_normalize(df).head(50)) # AttributeError: 'str' object has no attribute 'values'