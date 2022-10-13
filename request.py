def get_openssl_version() -> int:
    try:
        import ssl
    except ImportError:
        print("Openssl Lib Error !!")
        # return -99
        # 建议直接更新Python的版本，有特殊情况请提交issues
        exit(-1)
    temp_list = ssl.OPENSSL_VERSION_INFO
    return int(f"{str(temp_list[0])}{str(temp_list[1])}{str(temp_list[2])}")
    
try:
    # 优先使用httpx，在httpx无法使用的环境下使用requests
    import httpx

    http = httpx.Client(timeout=20, transport=httpx.HTTPTransport(retries=10))
    # 当openssl版本小于1.0.2的时候直接进行一个空请求让httpx报错

    if get_openssl_version() <= 102:
        httpx.get()
except (TypeError, ModuleNotFoundError):
    import requests
    from requests.adapters import HTTPAdapter

    http = requests.Session()
    http.mount('http://', HTTPAdapter(max_retries=10))
    http.mount('https://', HTTPAdapter(max_retries=10))

