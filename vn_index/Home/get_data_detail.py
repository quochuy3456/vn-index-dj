import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    filename='get_data_detail.log',
                    filemode='w',
                    format=(
                            '%(levelname)s:\t'
                            '%(filename)s:'
                            '%(funcName)s():'
                            '%(lineno)d\t'
                            '%(message)s'
                            )
                    )

logger = logging.getLogger()
FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(FORMAT)


class GetDataDetail:
    def __init__(self):
        self.data = {
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Length': '655',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                        'X-MicrosoftAjax': 'Delta=true',
                    }
        self.headers = {
                        'Accept': "*/*",
                        'Accept-Encoding': "gzip, deflate, br",
                        'Accept-Language': "en-US,en;q=0.9,vi;q=0.8",
                        'Cache-Control': "no-cache",
                        'Connection': "keep-alive",
                        'Content-Length': "655",
                        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                        "Host": "s.cafef.vn",
                        "Origin": "https://s.cafef.vn",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) snap Chromium/83.0.4103.97 Chrome/83.0.4103.97 Safari/537.36",
                        "X-MicrosoftAjax": "Delta=true"
                    }
        self.data_detail = []

        self.lbl_11 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Thay đổi (+/-%)',
                       'GD KL - KL', 'GD KL - GT', 'GD TT - KL', 'GD TT - GT',
                       'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
        self.lbl_12 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Thay đổi (+/-%)',
                       'GD KL - KL', 'GD KL - GT', 'GD TT - KL', 'GD TT - GT',
                       'Giá tham chiếu', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
        self.lbl_13 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Giá bình quân',
                       'Thay đổi (+/-%)', 'GD KL - KL', 'GD KL - GT', 'GD TT - KL',
                       'GD TT - GT', 'Giá tham chiếu', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']

    @staticmethod
    def convert_to_int(data):
        print(data)
        if "%" in data:
            data = data[0:5]

        if "," in data:
            data = data.replace(",", "")

        try:
            data_to_int = float(data)
            if data_to_int:
                return data_to_int
            else:
                return data
        except:
            return data

    def crawl_all_data(self, cpn_code):
        dt = self.data
        hd = self.headers
        dt['ctl00$ContentPlaceHolder1$ctl03$txtKeyword'] = cpn_code
        hd["Referer"] = f"https://s.cafef.vn/Lich-su-giao-dich-{cpn_code.upper()}-1.chn"
        for i in range(1, 15):
            dt['__EVENTARGUMENT'] = i
            d = BeautifulSoup(
                    requests.post(
                        f"https://s.cafef.vn/Lich-su-giao-dich-{cpn_code.upper()}-1.chn",
                        data=dt, headers=hd).text, "html.parser")
            try:
                rows = d.find_all('table')[1].find_all('tr')[2:]
            except:
                return None

            if len(rows[0].find_all('td')[0:-3]) <= 11:
                for t in rows:
                    d = list(map(lambda x: self.convert_to_int(x.get_text(strip=True)), t.find_all('td')))
                    self.data_detail.append(list(filter(lambda x: True if x else False, d)))
            else:
                for t in rows:
                    d = list(map(lambda x: self.convert_to_int(x.get_text(strip=True)), t.find_all('td')[0:-3]))
                    self.data_detail.append(list(filter(lambda x: True if x else False, d)))

        try:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_11)
            return df
        except:
            logging.debug('Combine title with data length 11')

        try:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_12)
            return df
        except:
            logging.debug('Combine title with data length 12')

        try:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_13)
            return df
        except:
            df = None
            logging.debug('Combine title with data length 13')
            logging.error("Length not match data <-> label")
            return df
