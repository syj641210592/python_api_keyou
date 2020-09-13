from com_func.test_log import log
from com_func.confread import config
from com_func.sql_request import mysql
from com_func.com_request_func import com_request, com_assertEqual, com_excel_read
from jsonpath import jsonpath
import unittest
import ddt
import openpyxl


@ddt.ddt
class TestRegister(unittest.TestCase):
    '''注册接口测试'''
    Worksheet_name = "register"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path) 

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestRegister, self.Worksheet_name, **kwargs)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
            if kwargs["sql_cheack"]:  # 存在sql校验,获取新增注册名称
                res = mysql.sql_read(kwargs["sql_cheack"], jsonpath(respone.json(), "$..username")[0])
                print("实际项目名称:", res["username"])
                print("预期项目名称:", self.params["username"])
                self.assertEqual(res["username"], self.params["username"])  # 校验更新后的昵称与预期
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
class TestLogin(unittest.TestCase):
    '''登录接口测试'''
    Worksheet_name = "login"
    excel, data_list = com_excel_read(Worksheet_name)

    @classmethod
    def setUpClass(cls):
        cls.excel.wb = openpyxl.load_workbook(cls.excel.path) 

    def setUp(self):
        pass
    
    @ddt.data(*data_list)
    @ddt.unpack
    def test_case(self, info, **kwargs):
        '''{info}'''
        try:
            respone = com_request(TestLogin, self.Worksheet_name, **kwargs)
            com_assertEqual(self, respone, eval(kwargs["expect"]))
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


