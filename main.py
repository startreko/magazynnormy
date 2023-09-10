
from data_extractor import DataExtractor

class ReportProcessor:
    def __init__(self):
        self.xml_path = "YOUR_XML_DIRECTORY_PATH"
        self.json_path = "YOUR_JSON_DIRECTORY_PATH"
        self.file_extractor = DataExtractor(self.xml_path, self.json_path)

    def validate_input(self, order_number):
        if len(order_number) < 7:
            return 'Invalid order number length'
        data = self.file_extractor.extract_data(order_number)
        if not data:
            return 'The provided order number does not exist'
        return ''

if __name__ == "__main__":
    from gui import WarehouseGUI

    app = WarehouseGUI(ReportProcessor())
    app.run()
