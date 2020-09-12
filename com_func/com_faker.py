from faker import Faker
import random, string


faker_cn = Faker(locale="zh_CN")
faker_en = Faker()

def data_create(type_name, length, *args, **kwargs):
    try:
        if type_name == "str":
            str_type = kwargs.get("str_type")
            if str_type == "en" or str_type == None:
                data = faker_en.pystr(min_chars=None, max_chars=int(length))
            elif str_type == "cn":
                data = faker_cn.text(max_nb_chars=int(length)).replace(".", "").replace("\n", "")
                data = data + data[0:int(length)-len(data)]
            elif str_type == "ec":
                data_en = faker_en.pystr(min_chars=None, max_chars=int(random.randint(1, int(length))))
                data_cn = faker_cn.text(max_nb_chars=int(length)).replace(".", "").replace("\n", "")[0:int(length)-len(data_en)]
                data = data_en + data_cn
            else:
                data = ""
            while True:
                if len(data) < int(length):
                    data = data + data[0:int(length)-len(data)]
                else:
                    break
        return data
    except Exception as e:
        raise ValueError("生成数据错误")