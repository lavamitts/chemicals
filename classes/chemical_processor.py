from glob import glob
import csv
from dotenv import load_dotenv
import os
import re
import json
from classes.html_file import HtmlFile
import classes.globals as g
from classes.commodity8 import Commodity8


class ChemicalProcessor(object):
    def __init__(self):
        self.get_config()
        self.cas_specifics = {}
        self.comm_codes_with_cas_numbers = {}

    def get_config(self):
        load_dotenv('.env')
        self.csv_path = os.getenv('CSV_PATH')

    def download(self):
        commodities = {}
        # Create a full list of 8 digit commodities that can be downloaded
        # This currently pulls from a CSV, as there is no simple way to pull
        # a list of all commodities and their 'end-line' / declarable status
        # from the database, although the nested set work will facilitate this
        with open(self.csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    commodity_code = row[1][0:8]
                    end_line = int(row[6])
                    if end_line == 1:
                        chapters = []
                        for i in range(0, 97):
                            if i != 77:
                                chapters.append(str(i).zfill(2))
                        if commodity_code[0:2] in chapters:
                            if commodity_code not in commodities:
                                # print("Downloading data for subheading", commodity_code)
                                c = Commodity8(commodity_code)
                                commodities[commodity_code] = c
                line_count += 1

        # Download commodities / subheadings
        for commodity in commodities:
            commodities[commodity].download()

    def get_specific_cas_references(self):
        with open(self.csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    commodity_code = row[1]
                    description = row[7]
                    c = Commodity8(commodity_code, description)
                    c.end_line = row[6]
                    c.productline_suffix = row[2]

                    c.sid = row[2]
                    c.start_date = row[3]
                    c.end_date = row[4]
                    c.indentation = row[5]
                    c.classification = row[8]
                    c.hierarchy = row[10].replace("_", "-")
                    key = c.gnid_pls()
                    if c.hierarchy != "":
                        hierarchy_list = c.hierarchy.split(",")
                        for item in hierarchy_list:
                            if item not in g.descendant_dict:
                                g.descendant_dict[item] = [key]
                            else:
                                if key not in g.descendant_dict[item]:
                                    g.descendant_dict[item].append(key)

                    g.commodity_codes[key] = c

                    if "CAS RN" in description:
                        description = description.replace("CAS RNs", "CAS RN")
                        match = re.search("\((CAS RN[^\)]+)\)", description)
                        if match:
                            groups = match.groups()
                            for group in groups:
                                group = group.replace(" or ", ", ")
                                group = group.replace(" and ", ", ")
                                group_items = group.split(",")
                                for group_item in group_items:
                                    cas_item = group_item.replace("CAS RN", "").strip()

                                    # Add to the list of impacted commodities
                                    if key not in self.comm_codes_with_cas_numbers:
                                        end_line = g._to_bool(g.commodity_codes[key].end_line)
                                        self.comm_codes_with_cas_numbers[key] = {"cas_codes": [cas_item], "end_line": end_line}
                                    else:
                                        if cas_item not in self.comm_codes_with_cas_numbers[key]["cas_codes"]:
                                            self.comm_codes_with_cas_numbers[key]["cas_codes"].append(cas_item)

                                    # Add to the list of impacted chemicals
                                    if cas_item not in self.cas_specifics:
                                        self.cas_specifics[cas_item] = [key]
                                    else:
                                        if key not in self.cas_specifics[cas_item]:
                                            self.cas_specifics[cas_item].append(key)
                line_count += 1

    def write_specific_cas_references(self):
        filename = os.path.join(os.getcwd(), "resources", "csv", "specific_chemicals.json")
        with open(filename, 'w') as f:
            f.write(json.dumps(self.cas_specifics, indent=4))

        filename = os.path.join(os.getcwd(), "resources", "csv", "specific_commodities.json")
        with open(filename, 'w') as f:
            f.write(json.dumps(self.comm_codes_with_cas_numbers, indent=4))

    def process_html_files(self):
        records = []
        my_path = os.path.join(os.getcwd(), "resources", "html", "*.html")
        files = []
        for file in glob(my_path):
            files.append(file)

        files.sort(reverse=False)
        count = 0
        for file in files:
            h = HtmlFile(file, self.cas_specifics)
            if len(h.cas_records) > 0:
                count += 1
            records += h.cas_records

        filepath = os.path.join(os.getcwd(), "resources", "csv", "chemicals.csv")
        fields = ['cus', 'cn_code', 'cas_rn',
                  'ec_number', 'un_number', 'nomen', 'name']

        for record in records:
            c = record[1]
            if len(c) < 13:
                print("Commodity code", c, "has fewer than 14 characters")

        with open(filepath, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(fields)
            csv_writer.writerows(records)
