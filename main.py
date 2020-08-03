import json
import xmltodict
import csv
import sys


def xml_to_json(xml_path):
    xml_file = open(xml_path,'r',encoding='utf-8').read()
    xmls = xmltodict.parse(xml_file)
    data = json.loads(json.dumps(xmls, indent=4))
    # with open('1.json', 'r', encoding='utf-8')as f1:
    #     data = json.loads(f1.read())
    ip_jiedian = data['aurora']['data']['report']['targets']['target']
    print(ip_jiedian)
    return ip_jiedian

def chuli(pip,i):
    try:
        _res = i['result']['value']
        if len(_res) == 4:
            res_port = int(_res[0])  # 端口
            res_xieyi = _res[2]  # 端口
        else:
            res_port = int(_res[0]) # 端口
            res_xieyi = _res[1]  # 端口
        if res_xieyi == 'https':
            full_path = f'https://{pip}:{res_port}||{res_xieyi}'
        else:
            full_path = f'http://{pip}:{res_port}||{res_xieyi}'
        return full_path
    except Exception as e:
        pass

def handle_json(ip_jiedian: list):
    all_data = []
    for _ip in ip_jiedian:
        try:
            items = {}
            pip = _ip['ip']
            port = _ip['appendix_info']['info']
            set_tuple = []
            if isinstance(port, list) and len(port) >= 1:
                for _port in port:
                    pport = _port['record_results']
                    for i in pport:
                        if i:
                            full_path = chuli(pip, i)
                            set_tuple.append(full_path)
            else:
                pport = port['record_results']
                for i in pport:
                    if i:
                        full_path = chuli(pip,i)
                        set_tuple.append(full_path)
        except Exception as e:
            continue
        items['data'] = list(set(set_tuple))
        all_data.append(items)
    return all_data


def handle_data(ip):
    if ip:
        ip_list = ip.split('://')
        ip_items = {}
        ip_ip = ip_list[1].split(':')[0]
        ip_port = ip_list[1].split(':')[1].split('||')[0]
        xieyi = ip.split('||')[1]
        ip_items['协议'] = xieyi
        ip_items['ip'] = ip_ip
        ip_items['开放端口'] = ip_port
        return ip_items


def json_to_csv(json_list, csv_path):
    # 2. csv的写入文件对象
    csv_file = open(csv_path, 'w', encoding='utf-8-sig')
    # 3. 取出数据 : 1.表头 2. 内容
    # 3.1获取表头所需要的数据
    sheet_title = json_list[0].keys()
    # 3.2 取所有内容
    json_values = []
    for dict in json_list:
        json_values.append(dict.values())

    # 4.写入csv文件
    # 4.1根据文件对象  生成读写器
    csv_writer = csv.writer(csv_file)

    # 4.2 写入表头
    csv_writer.writerow(sheet_title)
    # 4.3 写入内容
    csv_writer.writerows(json_values)

    # 5.关闭文件
    csv_file.close()

    print("完成")


def wirte_to_csv(data: list, csv_path='data.csv'):
    print(data)
    json_list = []
    for _data in data:
        for k in _data['data']:
            # 每一个单独的节点
            if k:
                k_items = handle_data(k)
                k_items.update({'url': k.split("||")[0]})
                print(k_items)
                json_list.append(k_items)
    json_to_csv(json_list, csv_path)


if __name__ == '__main__':
    import sys
    file_path = sys.argv[1]
    csv_path = sys.argv[2]
    print(file_path)
    data = handle_json(xml_to_json(file_path))
    wirte_to_csv(data,csv_path)
