from com_func.confread import config, config_write
from com_func.test_log import log
from com_func.com_request_func import com_request
from com_func.re_replace import username_get, email_get, params_get



def env_params_init():
    '''预置账号写入'''
    # 预置账号信息写入conf.ini文件
    try:
        env_params_regist()
        env_projects_create()
        env_testcases_create()
    except Exception as e:
        log.error("测试环境数据初始化失败", exc_info=True)
        raise ValueError("测试环境数据初始化失败")


def env_params_regist():
    '''生成一组非管理员/管理员账号,将账号信息写入conf.ini文件'''
    try:
        user_list = ["unadmin_params", "admin_params"]
        for user in user_list:
            params = {"username": username_get("username new 6".split(" ")),"email": email_get("email new".split(" ")),"password": "334498sun","password_confirm": "334498sun"}
            respone = com_request(env_params_regist, "register", params=params)
            if respone.status_code == 201:
                config_write("PRESET", user, str(params))
            else:
                raise ValueError
    except Exception as e:
        raise ValueError

def env_projects_create():
    '''生成一项目,将项目信息写入conf.ini文件'''
    try:
        # -------------------登录普通账户获取token----------------------------------------------
        params = config.get("PRESET", "unadmin_params")
        respone = com_request(env_projects_create, "login", params=params)
        token = "JWT" + " " + respone.json()["token"]
        # -------------------创建项目----------------------------------------------
        params = {"name": "*name new 5 en*","leader": "孙忘","tester": "孙忘","programmer": "孙忘","publish_app": "自动化分析工具","desc": "时序自动化"}
        respone = com_request(env_projects_create, "projects", params=params, token=token)
        if respone.status_code == 201:
            config_write("PRESET", "projects", str(respone.json()))
        else:
            raise ValueError
    except Exception as e:
        raise ValueError

def env_testcases_create():
    '''生成一接口,将接口信息写入conf.ini文件'''
    try:
        # -------------------登录普通账户获取token----------------------------------------------
        params = config.get("PRESET", "unadmin_params")
        respone = com_request(env_projects_create, "login", params=params)
        token = "JWT" + " " + respone.json()["token"]
        # -------------------创建接口----------------------------------------------
        params = {"name": "*tcname new 200 ec*","tester": "孙忘","project_id": "*projects id exist*","desc": "时序自动化"}
        respone = com_request(env_testcases_create, "interfaces", params=params, token=token)
        if respone.status_code == 201:
            config_write("PRESET", "interfaces", str(respone.json()))
        else:
            raise ValueError
    except Exception as e:
        raise ValueError