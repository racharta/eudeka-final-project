from required import Connection
import json, re, urllib.parse

# == TODO ==
headers = {"key": "49c734c84f172f6e80158331a0a32d1e",
           "Content-Type": "application/x-www-form-urlencoded"}
# ==========
conn = Connection("api.rajaongkir.com")


def get_url(url):
    conn.request("GET", url, headers=headers)
    res = conn.getresponse().read()
    data = res.decode("utf-8")

    data = json.loads(data)
    return data['rajaongkir']['results']

def get_province(name="", id=""):
    url = f"/starter/province?id={id}" if id else "/starter/province/"
    data =  get_url(url)
    if name:
        for i in data:
            if re.match(i['province'].lower(), name):
                return i
    else:
        return data

def get_city(name="", id_city="", id_province=""):
    url = "/starter/city"
    if id_city:
        url += f"?id={id_city}"
    if id_province:
        url += f"?province={id_province}"

    data = get_url(url)
    if name:
        for i in data:
            if re.match(i['city_name'].lower(), name):
                return i
    else:
        return data

def city_is_available(city_name):
    if get_city(name=city_name):
        return True
    else:
        return False

def province_is_available(province_name):
    if get_province(name=province_name):
        return True
    else:
        return False

def get_cost(from_, to, weight, courier='jne'):
    """function untuk mendapatkan harga ongkir"""
    payload = urllib.parse.urlencode({
               "origin": from_,
               "destination": to,
               "weight": weight,
               "courier": courier})
    conn.request("POST", "/starter/cost/", payload, headers=headers)
    data = conn.getresponse()
    data = data.read()
    result = data.decode("utf-8")
    result = json.loads(result)['rajaongkir']['results']
    return result  

