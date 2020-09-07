from com_func.sql_request import mysql
from com_func.confread import config
import random, string
import re
from com_func.test_log import log


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
                elif res_list[0] == "email":
                    res = email_get(res_list, cls)
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


def username_get(params_list, cls):
    if "new" in params_list:
        while True:
            username = ''.join(random.sample(string.ascii_letters + string.digits, int(params_list[2])))
            sql = "SELECT count(username) FROM test.auth_user WHERE username=%s;"
            res = mysql.sql_read(sql, username)
            if res["count(username)"] == 0:
                break
    elif "exist" in params_list:
        sql = "SELECT username FROM test.auth_user where 1 ORDER BY rand() LIMIT 1;"
        res = mysql.sql_read(sql)
        username = res["username"]
    return username


def email_get(params_list, cls):
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