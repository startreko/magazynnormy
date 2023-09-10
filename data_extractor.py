
import os
import json
import xml.etree.ElementTree as ET
import math
from datetime import datetime

class DataExtractor:
    def __init__(self, xml_directory, json_directory):
        self.xml_directory = xml_directory
        self.json_directory = json_directory
        self.namespace = {"ns": "http://www.example.com/Schema"}

    def _read_xml(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        marker_material = root.find(".//ns:MarkerMaterial", self.namespace)
        marker_attributes = root.find(".//ns:MarkerAttributes", self.namespace)
        file_creation_time = os.path.getctime(file)
        file_creation_date = datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d %H:%M:%S')

        if marker_material is not None and marker_material.get("description") not in ["FIB", "FIB_MAT", "FIB_STO"]:
            description = marker_material.get("description").replace(' ', '_')
            width = marker_material.get("width")
            achieved_length = marker_attributes.get("achievedLength")
            width_m = str(round(float(width) / 100, 2)) + "m"

            if achieved_length is not None:
                achieved_length_m = math.ceil(float(achieved_length) * 10 / 100) / 10
            else:
                achieved_length_m = "data error"

            return file_creation_date, description, width_m, achieved_length_m
        else:
            return None

    def _convert_shading_item(self, item):
        patterns = [
            (lambda s: "ARM" in s, "ARM"),
            (lambda s: "PODL" in s, "ARM"),
            (lambda s: "_AS_" in s, "AS"),
            (lambda s: "_WS_" in s, "WS")
        ]

        for pattern, value in patterns:
            if pattern(item):
                return value
        return "OTHER"

    def _read_json(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        shading_item = self._convert_shading_item(data.get("shadingItem", ""))
        qty = data.get("qty", 0)
        return shading_item, qty

    def harmonize_creation_dates(self, data):
        latest_dates = {}
        for entry in data:
            order_id = entry[11]
            fabric_id = entry[4]
            creation_date = entry[3]
            key = (order_id, fabric_id)
            if key not in latest_dates or (creation_date > latest_dates[key]):
                latest_dates[key] = creation_date

        new_data = [entry for entry in data if latest_dates[(entry[11], entry[4])] == entry[3]]
        new_data.sort(key=lambda x: (x[4], x[2], x[11]))
        return new_data

    def extract_data(self, order_no):
        data = []
        for file in os.listdir(self.xml_directory):
            if file.startswith(order_no):
                xml_file = os.path.join(self.xml_directory, file)
                parts = file.split('-')
                if len(parts) >= 3:
                    work_order = parts[1]
                    cutting_order = parts[2].split('.')[0]

                xml_data = self._read_xml(xml_file)
                if xml_data is not None:
                    json_filename = '0000000' + file[:-4][-7:] + '.json'
                    json_file = os.path.join(self.json_directory, json_filename)
                    if os.path.isfile(json_file):
                        json_data = self._read_json(json_file)
                        data.append((order_no, work_order, cutting_order) + xml_data + json_data)

        return self.harmonize_creation_dates(data)

