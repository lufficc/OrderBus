import json
import time
import webbrowser
import yaml
import requests
import io


def order():
    config = yaml.load(io.open('config.yaml', encoding='utf-8'))
    phone_number = config['phone_number']
    route_code = config['route_code']
    date = config['date']
    cookie = config['cookie']
    headers = {
        'Cookie': cookie,
        'Host': 'sep.ucas.ac.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    route_codes = {
        '0001': '雁栖湖—玉泉路7:00',
        '0003': '雁栖湖—玉泉路13:00',
        '0004': '雁栖湖—玉泉路15:40',
        '0005': '玉泉路—雁栖湖6:30',
        '0006': '玉泉路—雁栖湖10:00',
        '0007': '玉泉路—雁栖湖15:00',
        '0009': '雁栖湖—玉泉路7:00（周末）',
        '0011': '雁栖湖—玉泉路13:00（周末）',
        '0012': '雁栖湖—玉泉路15:40（周末）',
        '0013': '玉泉路—雁栖湖6:30（周末）',
        '0014': '玉泉路—雁栖湖10:00（周末）',
        '0015': '玉泉路—雁栖湖18:00（周末）',
        '0017': '雁栖湖—玉泉路7:00(节假日)',
        '0019': '雁栖湖—玉泉路13:00(节假日)',
        '0020': '雁栖湖—玉泉路15:40(节假日)',
        '0021': '玉泉路—雁栖湖6:30(节假日)',
        '0022': '玉泉路—雁栖湖10:00(节假日)',
        '0023': '玉泉路—雁栖湖18:00(节假日)',
    }

    print("即将开始预约, 预约信息:")
    print('手机号: {}'.format(phone_number))
    print('路线: {}'.format(route_codes[route_code]))
    print('日期: {}'.format(date))
    print('-' * 32)
    data = {
        'payProjectId': 4,
        'factorycode': 'R001',
        'routecode': route_code,
        'bookingdate': date,
        'payAmt': 6,
        'tel': phone_number
    }
    sess = requests.Session()
    count = 1
    while True:
        try:
            response = sess.post('http://payment.ucas.ac.cn/NetWorkUI/reservedBusCreateOrder', data=data, headers=headers)
            info = response.json()
            if info['returncode'] == 'SUCCESS':
                pay_url = "http://payment.ucas.ac.cn/NetWorkUI/showUserSelectPayType25" + str(info['payOrderTrade']['id'])
                print('预定成功,请在打开的网页中进行支付。如果没有自动打开网页, 请复制连接到浏览器进行支付: ')
                print(pay_url)
                try:
                    webbrowser.open(pay_url)
                except Exception:
                    pass
                quit()
            else:
                print('{:0>5d}: {}'.format(count, info['returnmsg']))
                count += 1
        except json.decoder.JSONDecodeError:
            print('您未登录，请在浏览器登陆后复制 Cookie 到 config.yaml.')
            quit()
        except Exception as e:
            print(e)
        time.sleep(0.5)


if __name__ == '__main__':
    order()
