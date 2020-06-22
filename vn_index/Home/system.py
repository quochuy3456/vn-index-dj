import os

def check_newwork():
    """
    check network connection
    :return:
    """
    hostname = "google.com"
    try:
        hostname = "google.com"
        response = os.system("ping -c 1 " + hostname)
        return True
    except:
        return False