from com_func.confread import config
from com_func.re_replace import params_get
from com_func.excel import ExcelOperate
from com_func.handle_sign import HandleSign
import requests

def com_request(cls, api, **kwargs):
    '''通用请求方式'''
    # -------------------请求接口----------------------------
    api_url = config.get("URL", "url") + params_get(config.get("URL", api + "_url"), cls, 1)  # 登录接口请求地址

    # -------------------请求参数----------------------------
    params = params_get(str(kwargs["params"]).replace("\n", ""), cls)  # 参数处理
    setattr(cls, "params", params)
    method = config.get("METHOD", api + "_method")



    # -------------------请求响应----------------------------
    respone = requests.request(method, api_url, json=params)  # 请求
    return respone


def com_assertEqual(self, respone, expect):
    '''判定'''
    # -------------------预期参数----------------------------
    expect = params_get(str(expect).replace("\n", ""), self)  # 参数处理

    print("实际状态:", dict(zip(["Status", "msg"], [respone.status_code, str(respone.json())])))
    print("预期状态:", expect)
    self.assertEqual(respone.status_code, expect["Status"])  # 判断code
    com_assertIn(str(respone.json()), expect["msg"])  # msg


def com_assertIn(respone, expect):
    if not expect in respone:
        raise AssertionError

def com_excel_read(sheetname):
    workbook_name = config.get("EXCEL", "workbook_name")  # 工作簿名
    excel = ExcelOperate(workbook_name)  # 打开excel
    data_list = excel.excel_read(sheetname)  # 获取数据
    return excel, data_list
