#!/usr/bin/env python
"""
 В json есть список метрик собираемых с устройства для обработки. Остальные метрики не нужны. Тестов SLA на устройстве может быть множество. Это последняя цифра в метрике в выводе snbmpwalk.  
		В JSON указано преобразование метрики устройства в метрику для обработки. Связано это с тем, что устройства могут быть разные, с разными метриками, а в мониторинге все будет единообразно. 
		Так же в json указан коэффициент преобразования для каждой метрики. Значение метрики нужно умножить на коэффициент, или не менять, если коэффициент =0 (например для текстовых метрик)
Результат работы – список метрик в формате IP_устройства.Метрика.№_теста=Значение
"""


import json
import openpyxl

input_json_file = "./input/eltexClass.json"
metrics_output = ""

input_xlsx_file = "./input/eltexSLA.xlsx"
#input_xlsx      = []
input_xlsx_lines = 2500+1

# from json file
devices = []

def parse_json():

    with open(input_json_file) as f:
        input_json = f.read()
       
    global metrics_output
    data = json.loads(input_json)
    metrics_output = data["metric"]

    global devices
    devices = data["devices"]

#  metrics from xsls    
def parse_xlsx():

    input_xlsx = []
    
    # читаем excel-файл
    wb = openpyxl.load_workbook(input_xlsx_file)
    # получаем активный лист
    sheet = wb.active

    #global input_xlsx
    for line in range(1, input_xlsx_lines):
        input_xlsx.append(sheet[f'A{line}'].value)
        #print(sheet[f'A{line}'].value)
    
    return input_xlsx
    
# Результат работы – список метрик в формате IP_устройства.Метрика.№_теста=Значение
if __name__ == '__main__':

    parse_json()
    
    metrics_from_xsls = parse_xlsx()
    #print(metrics_from_xsls)
    
    for device in devices:
        device_ip = device["ip"]
        
        for m in metrics_from_xsls:
            # 2500: eltEsrIpSlaStatTestOutOfSequenceReverse.100 0
            number_of_test = m.split()[0][0:-1]
            
            metric_xsls = m.split()[1].split(".")[0]
            
            #['rttOutSec.ds', 1]
            out_metric = metrics_output[metric_xsls][0]
            out_metric_koeficient = metrics_output[metric_xsls][1]
            
            value_from_json = m.split()[-1]
            value_of_metric = value_from_json*out_metric_koeficient if out_metric_koeficient else value_from_json
            
            #metric_from_json = metrics_output[""]
            print(f"{device_ip}.{out_metric}.{number_of_test}={value_of_metric}")
        
        