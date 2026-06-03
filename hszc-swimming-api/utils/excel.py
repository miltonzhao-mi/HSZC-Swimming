"""Excel 工具类"""
import openpyxl
from io import BytesIO


class ExcelHelper:
    """Excel 处理辅助类"""

    def __init__(self, file):
        """初始化"""
        self.file = file
        self.workbook = None
        self.sheet = None
        self._load()

    def _load(self):
        """加载文件"""
        if hasattr(self.file, 'read'):
            self.workbook = openpyxl.load_workbook(BytesIO(self.file.read()))
        else:
            self.workbook = openpyxl.load_workbook(self.file)
        self.sheet = self.workbook.active

    def read_data(self, header_row=1):
        """读取数据为字典列表"""
        headers = []
        data = []

        for row_idx, row in enumerate(self.sheet.iter_rows(values_only=True), 1):
            if row_idx == header_row:
                headers = [str(cell).strip() if cell else '' for cell in row]
            else:
                if any(row):
                    row_data = {}
                    for idx, cell in enumerate(row):
                        if idx < len(headers) and headers[idx]:
                            row_data[headers[idx]] = cell
                    data.append(row_data)

        return data

    def read_one(self, header_row=1):
        """读取第一行数据"""
        data = self.read_data(header_row)
        return data[0] if data else None

    @staticmethod
    def export_to_bytes(headers, data_list):
        """导出数据到 BytesIO"""
        wb = openpyxl.Workbook()
        ws = wb.active

        # 写入表头
        ws.append(headers)

        # 写入数据
        for item in data_list:
            if isinstance(item, dict):
                ws.append([item.get(h, '') for h in headers])
            else:
                ws.append(item)

        # 保存到 BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return output

    @staticmethod
    def export_to_response(headers, data_list, filename='export.xlsx'):
        """导出为 Django HttpResponse """
        from django.http import HttpResponse
        output = ExcelHelper.export_to_bytes(headers, data_list)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
