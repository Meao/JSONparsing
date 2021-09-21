from pandas import json_normalize
# code from a stackoverflow answer to a question on normalization
data ={"data":[{"date":"2018-08-20T00:00:00","values":[
    {"account":"account_1","device":"device_1","deviceModel":"testdev","id":"id_1","Events":[
        {"EventCategory":"Scan","EventCategoryData":[
            {"name":"scanname","info":[{"type":"any","count":8.0}]},
            {"name":"scanname","info":[{"type":"any","count":1.0}]}],"scancount":2.0},
        {"EventCategory":"Web","EventCategoryData":[
            {"name":"web_Scan","info":[{"type":"Web","count":2.0}]},
            {"name":"web scan 2","info":[{"type":"Web 2","count":0.0}]},
            {"name":"web 3 ","info":[{"type":"Web 3","count":2.0}]}]},
        {"EventCategory":"WWW","EventCategoryData":[{"name":"any","info":[{"type":"wifi","count":2.0}]}],"scancount":4.0},
        {"EventCategory":"Others","EventCategoryData":[{"name":"anything","info":[{"previousversion":"default","updatedversion":"default"}]}]}]}]},
{"date":"2018-08-22T00:00:00","values":[{"account":"account_1","device":"device_1","deviceModel":"testdev","id":"id_2","Events":[{"EventCategory":"Scan2","EventCategoryData":[{"name":"scan name","info":[{"type":"scan 2","count":2}]},{"name":"update","info":[{"type":"scan","count":1},{"type":"WWW","count":1}]}],"scancount":1},{"EventCategory":"Web","EventCategoryData":[{"name":"web1","info":[{"type":"WWW","count":1}]},{"name":"Wifi","info":[{"type":"Web Sites","count":1}]},{"name":"web2","info":[{"type":"scan","count":1}]}]}]}]}],"status":"success"}
# #merge all data['data] multiple list of data['value'] into single list
# flat_list = [item for sublist in data['data'] for item in sublist['values']]
# print(flat_list)
# print("---------------------------------------------------------------------------")
# result = json_normalize(flat_list, record_path=['Events','EventCategoryData','info'],\
#                         meta=['account','device','deviceModel','id',['Events','EventCategory'],\
#                               ['Events','EventCategory','name']])
# print(result)
# print("---------------------------------------------------------------------------")
#merge all data['data] multiple list into single list and merge date items into values sublist of dict.
flat_list = []
for sublist in data['data']:
    new_list = [item for item in sublist['values']]
    print('new_list', new_list)
    new_list[0]['date'] = sublist['date']
    print('new_list_date', new_list)
    flat_list.extend(new_list)
print("---------------------------------------------------------------------------")
print('flat_list', flat_list)
print("---------------------------------------------------------------------------")
result = json_normalize(flat_list, record_path=['Events','EventCategoryData','info'],\
                        meta=['account','device','deviceModel','id','date',['Events','EventCategory'],\
                              ['Events','EventCategory','name']])

print(result)