import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    filename='get_data.log',
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

# path_1 = "https://s.cafef.vn/hastc/PVC-tong-cong-ty-hoa-chat-va-dich-vu-dau-khi-ctcp.chn"
# path_2 = "https://s.cafef.vn/hastc/CSC-cong-ty-co-phan-tap-doan-cotana.chn"
#
# path_3 = "https://s.cafef.vn/hose/VCB-ngan-hang-thuong-mai-co-phan-ngoai-thuong-viet-nam.chn"
# path_4 = "https://s.cafef.vn/hose/VNM-cong-ty-co-phan-sua-viet-nam.chn"
#
# path_5 = "https://s.cafef.vn/upcom/HHA-cong-ty-co-phan-van-phong-pham-hong-ha.chn"
# path_6 = "https://s.cafef.vn/upcom/KSA-cong-ty-co-phan-cong-nghiep-khoang-san-binh-thuan.chn"

lst_items = ["EPS cơ bản", "EPS pha loãng", "P/E", "Giá trị sổ sách",
            "Hệ số beta", "KLGD khớp lệnh trung bình 10 phiên",
            "KLCP đang niêm yết", "KLCP đang lưu hành", "thị trường"]

class GetIndex:
    def __init__(self, path, lst_items=lst_items):
        self.path = path
        self.all_data = None
        self.clawer_all_data()
        self.lst_items = lst_items

    def clawer_all_data(self):
        self.all_data = BeautifulSoup(requests.get(self.path).text, "html.parser")

    def get_eps(self, text):
        d = self.all_data.find(text=text).find_parents('li')[0]
        if d.find_all('div'):
            return list(map(lambda x: x.get_text(strip=True), d.find_all('div')))
        elif d.find_all('span'):
            return list(map(lambda x: x.get_text(strip=True), d.find_all('span')))
        else:
            logger.info("Try get data with get_eps(): FAIL")
            return None

    def get_pe(self, text):
        d = self.all_data.find_all('li')
        for s in d:
            if text in s.get_text(strip=True):
                if s.find_all('div'):
                    return list(map(lambda x: x.get_text(strip=True), s.find_all('div')))
                elif s.find_all('span'):
                    return list(map(lambda x: x.get_text(strip=True), s.find_all('span')))
                else:
                    logger.info("Try get data with get_pe(): FAIL")
                    return "Error"

    def detect_method(self, vle):
        logging.info(f"Try get data {vle}")
        try:
            _dt = self.get_eps(vle)
        except:
            _dt = self.get_pe(vle)
        return _dt

    def get_list(self):
        dt = list(map(self.detect_method, self.lst_items))
        dt_dict = pd.DataFrame(dt).T
        return dt_dict

# lst_path = [path_1, path_2, path_3, path_4, path_5, path_6]


# kt = GetIndex(path_3)
# print(kt.get_list()[1][1])


# for p in lst_path:
#     kt = GetIndex(p)
#     for i in lst_item:
#         try:
#             logger.info("Try get data with get_eps()")
#             d = kt.get_eps(text=i)
#         except:
#             logger.warning("Try get data with get_eps(): FAIL")
#             logger.info("Try get data with get_ep()")
#             d = kt.get_pe(text=i)
#         print(d)
#     print("---------------")