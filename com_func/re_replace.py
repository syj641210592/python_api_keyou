from com_func.sql_request import mysql
from com_func.confread import config
from com_func.test_log import log
from com_func.com_faker import faker_cn, data_create
import random
import re



def params_get(params, cls, type_mode=0):
    '''处理带*参数'''
    try:
        if "*" in params:
            while re.search(r"\*(.+?\s.+?.*?)\*", str(params)):
                res_value = re.search(r"\*(.+?\s.+?.*?)\*", str(params))  # 获取带*参数
                res_str = res_value.group()
                res_list = res_value.group(1).split(" ")  # 切割带*参数
                if res_list[0] == "username":
                    res = username_get(res_list, cls)
                elif "name" in res_list[0]:
                    res = name_get(res_list, cls)                   
                elif res_list[0] == "email":
                    res = email_get(res_list, cls)
                elif res_list[0] == "projects" or res_list[0] == "interfaces":
                    res = projects_interfaces_get(res_list, cls)
                elif res_list[0] == "params":
                    res = expect_params_get(res_list, cls)
                params = params.replace(res_str, str(res))
            mysql.con.commit()                       
    except Exception:  # 获取失败报判定错误
        log.error("带*参数解析失败", exc_info=True)
        raise AssertionError
    else:
        if type_mode == 0:
            return eval(params)
        else:
            return params

def expect_params_get(params_list, cls):
    expect_params = getattr(cls, "params")[params_list[1]]
    return expect_params

def name_get(params_list, cls=None):
    if params_list[0] =="name":
        database_name = "tb_projects"
    elif params_list[0] =="tiname":
        database_name = "tb_interfaces"
    elif params_list[0] =="tcname":
        database_name = "tb_testcases"

    if "new" in params_list:
        while True:
            name = data_create("str", params_list[2], str_type=params_list[3])
            sql = f"SELECT count(name) FROM test.{database_name} WHERE name = %s;"
            res = mysql.sql_read(sql, name)
            if res["count(name)"] == 0:
                break
    elif "exist" in params_list:
        sql = f"SELECT name FROM test.{database_name} WHERE 1 ORDER BY rand() LIMIT 1;"
        res = mysql.sql_read(sql)
        name = res["name"]
    elif "str" in params_list:
        name = data_create("str", params_list[2], str_type=params_list[3])
    return name

def username_get(params_list, cls=None):
    if "new" in params_list:
        while True:
            username = data_create("str", params_list[2])
            sql = "SELECT count(username) FROM test.auth_user WHERE username=%s;"
            res = mysql.sql_read(sql, username)
            if res["count(username)"] == 0:
                break
    elif "unadmin" in params_list:
        username = eval(config.get("PRESET", "unadmin_params"))["username"]
    elif "exist" in params_list:
        sql = "SELECT username FROM test.auth_user WHERE 1 ORBDER BY rand() LIMIT 1;"
        res = mysql.sql_read(sql)
        username = res["username"]
    return username


def email_get(params_list, cls=None):
    if "new" in params_list:
        while True:
            email = f"{random.randint(0,999999999)}@qq.com"
            sql = "SELECT count(email) FROM test.auth_user WHERE email=%s;"
            res = mysql.sql_read(sql, email)
            if res["count(email)"] == 0:
                break
    elif "exist" in params_list:
        sql = "SELECT email FROM test.auth_user where 1 ORDER BY rand() LIMIT 1;"
        res = mysql.sql_read(sql)
        email = res["email"]       
    return email

def projects_interfaces_get(params_list, cls=None):
    if params_list[0] =="projects":
        database_name = "tb_projects"
    elif params_list[0] =="interfaces":
        database_name = "tb_interfaces"


    if "id" in params_list:
        if "exist" in params_list:
            id = eval(config.get("PRESET", params_list[0]))["id"]
        elif "new" in params_list:
            sql = f"SELECT max(id) FROM test.{database_name};"
            res = mysql.sql_read(sql)
            id = int(res["max(id)"]) + 100
    return id