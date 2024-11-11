table = ['table1', 'table2']
print(str(table))
info = {"hiveTable": table}

# """
# {'hiveTable':table}
# """
import json

with open('output.json', 'w') as f:
    # 使用json.dump()将字典对象写入文件
    json.dump(info, f)