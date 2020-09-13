from com_func.test_log import log
from com_func.confread import config
from jsonpath import jsonpath
from com_func.sql_request import mysql
from com_func.com_request_func import com_request, com_assertEqual, com_excel_read
import unittest
import ddt
import openpyxl


@ddt.ddt
class TestProjects(unittest.TestCase):
    '''新增项目'''
    Worksheet_name = "projects"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "unadmin_params")
        respone = com_request(TestProjects, "login", params=params)
        cls.token = "JWT" + " " + respone.json()["token"]


    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestProjects, self.Worksheet_name, **kwargs, token=self.token)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取新增项目名称
                res = mysql.sql_read(kwargs["sql_cheack"], jsonpath(respone.json(), "$..name"))
                print("实际项目名称:", res["name"])
                print("预期项目名称:", self.params["name"])
                self.assertEqual(res["name"], self.params["name"])  # 校验更新后的昵称与预期
        except AssertionError as e:
            log.error(f"用例--{info}--执行失败", exc_info=True)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "失败")
            raise e
        else:
            log.info(f"用例--{info}--执行成功", exc_info=False)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "成功")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.excel.wb.save(cls.excel.path)
        cls.excel.wb.close()



@ddt.ddt
class TestInterfaces(unittest.TestCase):
    '''新增项目'''
    Worksheet_name = "interfaces"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        '''登录获取token,用户id'''
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path)   # 重新载入workbook
        params = config.get("PRESET", "unadmin_params")
        respone = com_request(TestInterfaces, "login", params=params)
        cls.token = "JWT" + " " + respone.json()["token"]


    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestInterfaces, self.Worksheet_name, **kwargs, token=self.token)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取新增项目名称
                res = mysql.sql_read(kwargs["sql_cheack"], jsonpath(respone.json(), "$..name"))
                print("实际用例名称:", res["name"])
                print("预期用例名称:", self.params["name"])
                self.assertEqual(res["name"], self.params["name"])  # 校验更新后的昵称与预期
        except AssertionError as e:
            log.error(f"用例--{info}--执行失败", exc_info=True)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "失败")
            raise e
        else:
            log.info(f"用例--{info}--执行成功", exc_info=False)
            self.excel.excel_write(self.Worksheet_name, kwargs["id"], "成功")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.excel.wb.save(cls.excel.path)
        cls.excel.wb.close()



