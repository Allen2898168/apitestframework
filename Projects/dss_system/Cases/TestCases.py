import xlrd
import unittest
from ddt import ddt, data, unpack
import json
import os
import xlrd

from Common.Case import Case
from Projects.dss_system.Base.Base import Base

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_excel(excel_path=BASE_PATH + "./Conf/case.xlsx"):
    '''
    读取excel文件内容
    :param excel_path: xlsx文件的路径
    :return: k-v的列表,k为sheet名，v为表格数据
    '''
    # 打开文件
    workbook = xlrd.open_workbook(excel_path)
    # 获取所有sheet
    sheet_list = workbook.sheet_names()  # [u'sheet1', u'sheet2']
    sheets_data = []

    for sheet in sheet_list:

        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_name(sheet)  # sheet索引从0开始

        # 获取第一行作为key
        first_row = sheet.row_values(0)  # 获取第一行内容

        # 获取表的行数
        rows_length = sheet.nrows

        # 定义两个空列表，存放每行的数据
        all_rows = []
        rows_dict = []
        for i in range(rows_length):  # 循环逐行打印
            if i == 0:  # 跳过第一行
                continue
            all_rows.append(sheet.row_values(i))
        for row in all_rows:
            lis = dict(zip(first_row, row))
            rows_dict.append(lis)

        sheet_data = {"sheet": sheet.name, "data": rows_dict}
        sheets_data.append(sheet_data)
    return sheets_data


excel_data = read_excel()


@ddt
class TestCases(Base):
    """ 数据驱动测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestCases, self).__init__(*args, **kwargs)

    for sheet_data in excel_data:
        sheet = sheet_data.get("sheet")
        cases = sheet_data.get("data")

        exec(F"""
@data(*{cases})
@unpack
def test_{sheet}(self,case_id,title,server,path,is_skip,headers,is_token,method,request_data,expect_result,actual_result
                 ,public_value,setup_sql,teardown_sql):

    with self.setUp():    
        path = self.build_param(path)
        body = self.build_param(request_data)
        expect_result = self.build_param(expect_result)    
        # setup_sql = self.execute_setup_sql(setup_sql)
        # teardown_sql = self.execute_teardown_sql(teardown_sql)
        

    with self.steps():
        if is_skip == 0:
            self.logger.warning("跳过用例编号：%s,标题：%s" %(case_id,title)) 
        elif is_skip == 1:
            self.logger.warning("执行用例编号：%s,标题：%s" %(case_id,title)) 
            resp = self.client_request(server,path,headers,is_token,method,body) 
            resp_json = json.loads(resp.text)
            # self.logger.warning("响应结果：%s" %(resp_json)) 
        else:
            self.logger.warning("未知is_skip") 

    with self.verify():
        self.assert_verify(expect_result,resp) 

    with self.save():
        if public_value:
            for save in public_value.split(";"):
                key = save.split("=")[0]
                jsp = save.split("=")[1]
                self.save_date(resp, key, jsp)
        """
             )


if __name__ == '__main__':
    unittest.main()
