from os import read
import json
with open('m.txt','rt+',encoding="utf-8") as f:
    f.write("""wertwte
    我我我欧文我
    问他问题为天文台谭维维额
    二维图特务""")
    print(f.read())
user ={
    "name":"张三",
    "age":18,
    "sex":"男",
    "hobby":["看电影","听音乐","看小说"]
}
with open('user.json','w',encoding="utf-8") as f:
    #存储json格式的数据
    json.dump(user,f,ensure_ascii=False,indent=2)
with open('user.json','r',encoding="utf-8") as f:
    #读取json格式的数据
    aa = json.load(f)
    print(aa)