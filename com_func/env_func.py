from com_func.confread import config_write
from com_func.test_log import log
from com_func.com_request_func import com_request
from com_func.re_replace import username_get,email_get



def env_params_init():
    '''预置账号写入'''
    # 预置账号信息写入conf.ini文件
    try:
        env_params_regist()
    except Exception as e:
        print(e)
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
        log.error("测试环境数据初始化失败", exc_info=True)
        raise ValueError("测试环境数据初始化失败")