import os
import uuid

import requests
import urllib.parse
from datetime import datetime
import time
from pytz import timezone
import PySimpleGUI as sg
from firebase import Firebase
import json

# Replace these values with your own:
street = "200 Bloomfield Ave"
town = "West Hartford"
state_initials = "CT"
zipcode = "06117"
dist_from_zip = 30  # Number of miles you're willing to drive (note: Walgreens requires 25 miles)
frequency = 1  # Check for vaccine availability every "frequency" minutes


# -----------------------------------------------------------------------------------------------------------------

pharmacy_errors_counts = dict()
pharmacy_errors_args = dict()
printed_errors = set()


def cvs_vaccines(zip, dist_from_zip):
    req = os.getenv(
        '_sn:4$_ss:0$_st:1617311359633$vapi_domain:cvs.com$_se:1$_pn:6%3Bexp-session$ses_id:1617308232262%3Bexp-session')

    cookies = {
        'adh_ps_pickup': 'on',
        'bbcart': 'on',
        'sab_newfse': 'on',
        'sab_displayads': 'on',
        'flipp2': 'on',
        'mc_rio_locator3': 'on',
        'mc_videovisit': 'on',
        'pivotal_forgot_password': 'off-p0',
        'pivotal_sso': 'off-p0',
        'ps': 'on',
        'rxhp': 'on',
        'rxhp-two-step': 'off-p0',
        'rxm': 'on',
        'rxm_phone_dob': 'on',
        'sab_deals': 'on',
        's2c_akamaidigitizecoupon': 'on',
        's2c_digitizecoupon': 'on',
        's2c_herotimer': 'off-p0',
        's2c_prodshelf': 'on',
        's2c_persistEcCookie': 'on',
        's2c_smsenrollment': 'on',
        'sftg': 'on',
        'show_exception_status': 'on',
        'mt.v': '2.1096946420.1612391892685',
        'gbi_visitorId': 'ckkq0i55m00013ba5rr6cf8i9',
        '_gcl_au': '1.1.1596802355.1612391896',
        '_4c_mc_': 'a3db4a28-c82f-4231-af1d-aceb7142f987',
        'QuantumMetricUserID': 'b20f7468324355f1c39b2e5596de9280',
        'BVBRANDID': 'dd34d813-044b-45f2-a5f6-dc47e2bfb332',
        'favorite_store': '5938/43.7003/-72.2898/Hanover/NH',
        'aat1': 'off-p1',
        'mc_home_new': 'off1',
        'refill_chkbox_remove': 'off-p0',
        's2c_beautyclub': 'off-p0',
        's2c_dmenrollment': 'off-p0',
        's2c_newcard': 'off-p0',
        's2c_papercoupon': 'on',
        '_group1': 'quantum',
        'mp_cvs_mixpanel': '%7B%22distinct_id%22%3A%20%2216fa26b8c78306-078a54de0d8704-c383f64-1704a0-16fa26b8c7924d%22%2C%22bc_persist_updated%22%3A%201612391908686%2C%22g_search_engine%22%3A%20%22google%22%7D',
        'CVPF': '3DCsiYyccHFa6FkXKYvoLU68JPLO4wETZogm-tafbU0xafJ16eGFOAA',
        'DG_IID': 'EDEE7A54-980B-3D86-8D08-C40DB0A10298',
        'DG_UID': 'A2555831-BD49-33A6-A501-9D930DDE4A59',
        'DG_ZID': '3820E408-65BB-308F-A272-E4DC91ED8564',
        'DG_ZUID': '6CAA9A50-3582-3C1C-9BF5-FC3CEF51952C',
        'DG_HID': '40373312-912B-311F-8927-87BDC472F335',
        'DG_SID': '69.112.101.1:n0zbo8RdCbhNbCrwbJrSNQ9whYOM4iBm/QCjYynqY4M',
        'pe': 'p1',
        'acctdel_v1': 'on',
        'adh_new_ps': 'on',
        'adh_ps_refill': 'on',
        'buynow': 'off',
        'dashboard_v1': 'off',
        'db-show-allrx': 'on',
        'disable-app-dynamics': 'on',
        'disable-sac': 'on',
        'dpp_cdc': 'off',
        'dpp_drug_dir': 'off',
        'dpp_sft': 'off',
        'getcust_elastic': 'on',
        'echomeln6': 'off-p2',
        'enable_imz': 'on',
        'enable_imz_cvd': 'on',
        'enable_imz_reschedule_instore': 'on',
        'enable_imz_reschedule_clinic': 'off',
        'gbi_cvs_coupons': 'true',
        'ice-phr-offer': 'off',
        'v3redirecton': 'false',
        'mc_cloud_service': 'on',
        'mc_hl7': 'on',
        'mc_ui_ssr': 'off-p0',
        'memberlite': 'on',
        'pauth_v1': 'on',
        'pbmplaceorder': 'off',
        'pbmrxhistory': 'on',
        'rxdanshownba': 'off',
        'rxdfixie': 'on',
        'rxd_bnr': 'on',
        'rxd_dot_bnr': 'on',
        'rxdpromo': 'on',
        'rxduan': 'on',
        'rxlite': 'on',
        'rxlitelob': 'off',
        'rxm_demo_hide_LN': 'off',
        'rxm_phdob_hide_LN': 'on',
        'rxm_rx_challenge': 'off',
        's2c_rewardstrackerbctile': 'on',
        's2c_rewardstrackerbctenpercent': 'on',
        's2c_rewardstrackerqebtile': 'on',
        's2cHero_lean6': 'on',
        'sft_mfr_new': 'on',
        'v2-dash-redirection': 'on',
        'bm_sz': '906745DC430A9D584BC72D8242C383C5~YAAQF6omFyUkoHl4AQAA+CIVjwvFtGQayC9oZnltvAxpTWRXS8nS5zuv8tevIl/yaFbABqwU+/ExBAPX//tj/8D6OaMFw2neW7ZirMDPgJ3xghl4EW2oCOWNHMIJl2uWfKXytPTfBwxilrEiWmjuQdOrOdhlZDPe33/INVAWZXscmmEVSbEaA9QMlBWc',
        'mt.sc': '%7B%22i%22%3A1617308232387%2C%22d%22%3A%5B%5D%7D',
        'AMCVS_06660D1556E030D17F000101%40AdobeOrg': '1',
        'AMCV_06660D1556E030D17F000101%40AdobeOrg': '-330454231%7CMCIDTS%7C18719%7CMCMID%7C09073556747944203903956111120418902550%7CMCAAMLH-1617913034%7C7%7CMCAAMB-1617913034%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1617315434s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2',
        's_cc': 'true',
        'gbi_sessionId': 'ckmzbkex100003b9bp4qld7uv',
        'QuantumMetricSessionID': 'a577244b236ed318f52e26764cf28c12',
        'mt.cem': '210307-Rx-Immunization-COVIDvax_1405672 - A-Old-winning-copy',
        'ak_bmsc': '437A8D5FFC13DB8EFC720ADBD40186051726AA17002C0000462A6660CE44E53F~plbQnwxX7at5Noc80F0AGVAnU5BqhOJKHxt8HNq9SwHwU04YkZ4qH3rT5ee26RmUwhdWQqPj9jcWj8pu+/AnEI7clyXjb65u2Tm8qATEW/ECt9LD9LybPog1EjKSjcLQIHUms05A1kuiiXc8V5Rl087GQyCDys0nkHQLOcjA7bE5zTTW8RdKMT4wo2cU5RLxh6z/1/OJVDEA2G4RVf5INuPVjP1Dkw0NG/vpIMZo/RZXAHmW9EnhPJlSNORP/GeuOi',
        'affinity': 'f907a143ac1049af',
        'akavpau_vp_www_cvs_com_vaccine': '1617309737~id=06612d000b7f27c2d4037515e208975d',
        'akavpau_vp_www_cvs_com_vaccine_covid19': '1617309737~id=06612d000b7f27c2d4037515e208975d',
        's_sq': '%5B%5BB%5D%5D',
        'gpv_p10': 'www.cvs.com%2Fvaccine%2Fintake%2Fstore%2Fcvd-store-select%2Ffirst-dose-select',
        'gpv_e5': 'cvs%7Cmweb%7Cvaccine%7Cintake%7Cstore%7Ccvd-store-select%7Crx%3A%20immunizations%3A%20first%20dose%20scheduler',
        'bm_sv': 'A6566D2E4144BE31B9C418FD7E9B61E0~Ucx5GGGu4n6xF1SRRL3Q1q10pNGxPbcs/wydlGxYHv97/Es/Dn2ispFvLIZP9aqMA00NqKu1EVCNYQx1zvkwCaBJJLImn0BhCfkQrk7m5cjrWj2sUiS+8HXqyIeZNrF0g6nhluc5dhAkDA9TZN/qUw==',
        'akavpau_www_cvs_com_general': '1617309715~id=8c6df807846574bedef6b16bf609d1df',
        '_abck': '26FCD431F7EA315D47FA0247A3893B7C~0~YAAQB5QZuPksQ3J4AQAAqmEljwXfUTEmruaffzySM8KkidHM3mfiL3YvnqdfCD8SBdjM2BwkFcbC2HZdVGmSE/twm1csZAi72FaM5VW/eRGlncUrPEZjqWPMfEEBJRPCAjiw3ECiHdKpU6+Tat7q6SojtLZrsx4wj0WiTSoUe3R4DAOCYRzfF9vPuUPSBx2nrlXazhGNOyQip5jnRCMmNQ+DP5/XpWsP6g/hC8N6rWvmAFcERS2UW0CEHYbhtIJ+rpOvyEAn3uq0WO/xOir1yOD/1ofcGWcdRbyUI06qprZPlKMsI0uczzO4hYPIhd0RanD7EXqkCnHtA2f8aUFOJuxvZEp5bMHphHmcR6W9zvF2nDfX2i2JYK38GcUtqA3vlcQtGlrW7gbwE96DDD5UCy3vXcTvdw==~-1~||-1||~-1',
        'RT': 'z=1&dm=cvs.com&si=7e6623ef-33bb-4e0c-90fb-2ec08cc93bbd&ss=kmzbk9ta&sl=l&tt=rn2&bcn=%2F%2F17d09914.akstat.io%2F',
        'qmexp': '1617311359131',
        'utag_main': f"v_id:01776a0bc89300020b8722673e5103073001406b00bd0{req}",
    }

    headers = {
        'authority': 'www.cvs.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not\\"A\\\\Brand";v="99"',
        'accept': 'application/json',
        'dnt': '1',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://www.cvs.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cvs.com/vaccine/intake/store/cvd-store-select/first-dose-select',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = '{"requestMetaData":{"appName":"CVS_WEB","lineOfBusiness":"RETAIL","channelName":"MOBILE","deviceType":"AND_MOBILE","deviceToken":"7777","apiKey":"a2ff75c6-2da7-4299-929d-d670d827ab4a","source":"ICE_WEB","securityType":"apiKey","responseFormat":"JSON","type":"cn-dep"},"requestPayloadData":{"selectedImmunization":["CVD"],"distanceInMiles":' + str(
        dist_from_zip) + ',"imzData":[{"imzType":"CVD","ndc":["59267100002","59267100003","59676058015","80777027399"],"allocationType":"1"}],"searchCriteria":{"addressLine":"' + str(
        zip) + '"}}}'

    response = requests.post('https://www.cvs.com/Services/ICEAGPV1/immunization/1.0.0/getIMZStores', headers=headers,
                             cookies=cookies, data=data)
    if response is not None and len(response.text) > 0:
        result = json.loads(response.text)
        if result["responseMetaData"]["statusDesc"] != "No stores with immunizations found":
            popup_and_store_info("CVS")


def rite_aid_vaccines(zip, dist_from_zip):
    headers = {
        'authority': 'www.riteaid.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not\\"A\\\\Brand";v="99"',
        'accept': '*/*',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.riteaid.com/pharmacy/apt-scheduler',
        'accept-language': 'en-US,en;q=0.9',
        '$cookie': '_gcl_au=1.1.1188221961.1616695124; _ga=GA1.2.830114817.1616695124; _mibhv=anon-1594168248362-9610399811_7189; __ruid=149436981-lf-oy-45-1p-wyv0rj9536aa434t7mff-1594168247979; _scid=44508585-5c2b-49c1-b146-71c077437c67; _pin_unauth=dWlkPVl6RXdabUpqTW1ZdFpXVTRZaTAwWTJRMUxUazROR010WkRZMFlXVmhaR1EyWXpJMQ; __rcmp=0\\u0021bj1fZ2MsZj1nYyxzPTAsYz0xNDgsdHI9MCxybj02MDgsdHM9MjAyMTAzMjUuMTc1OCxkPXBj; check=true; _gid=GA1.2.1652233128.1617308074; AMCVS_3B2A35975CF1D9620A495FA9%40AdobeOrg=1; AMCV_3B2A35975CF1D9620A495FA9%40AdobeOrg=77933605%7CMCIDTS%7C18719%7CMCMID%7C03294140053084263894531515667709850149%7CMCAAMLH-1617912874%7C7%7CMCAAMB-1617912874%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1617315274s%7CNONE%7CvVersion%7C4.5.1; s_cc=true; _sctr=1|1617249600000; __rutmb=149436981; __rutma=149436981-lf-oy-45-1p-wyv0rj9536aa434t7mff-1594168247979.1617308074769.1617311556158.11.32.4; __rpckx=0\\u0021eyJ0NyI6eyIzMiI6MTYxNzMxMTc0MDc5NX0sInQ3diI6eyIzMiI6MTYxNzMxMTc0MDc5NX0sIml0aW1lIjoiMjAyMTA0MDEuMjExMiIsImVjIjoxfQ~~; mbox=PC#c21e61e7bcf24f05b223b4c75f918675.34_0#1679945110|session#258e41acf30a43a5980396f58158a94f#1617313602; adcloud={%22_les_v%22:%22y%2Criteaid.com%2C1617313541%22}; __rpck=0\\u0021eyJwcm8iOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsImJ0Ijp7IjAiOmZhbHNlLCIxIjpudWxsLCIyIjoxMDA1MiwiMyI6MC42M30sIkMiOnt9LCJOIjp7fX0~; gpv_Page=web%3Apharmacy%3Aapt-scheduler; s_sq=%5B%5BB%5D%5D; _derived_epik=dj0yJnU9LXNtN3FNM3hlM2tPN1B5N1RVWW14RnJrN2xLNU43c2kmbj1KM2NCTndXU3JCTm85dkNTc29Ya2ZnJm09NyZ0PUFBQUFBR0JtTl80JnJtPWQmcnQ9QUFBQUFGOUJ5UUE; s_plt=5.45; s_pltp=web%3Apharmacy%3Aapt-scheduler; _gat_UA-1427291-1=1',
    }

    params = (
        ('address', zip),
        ('attrFilter', 'PREF-112'),
        ('fetchMechanismVersion', '2'),
        ('radius', dist_from_zip),
    )

    response = requests.get('https://www.riteaid.com/services/ext/v2/stores/getStores', headers=headers, params=params)

    if response is not None and len(response.text) > 0:
        result = json.loads(response.text)
        if len(result["Data"]["stores"]) != 0:
            popup_and_store_info("Rite Aid")


def walgreens_vaccines(lat, long, state, start_date):
    env1 = os.getenv('A99432B1AF00F9E75B5EB7A77022E7A1|0eed2717dafcc06d|1')
    env2 = os.getenv('320459500_16h1vOQIEUOJMNHWCABSNNASSCKJUCUHCGKKG-0e7')

    cookies = {
        'XSRF-TOKEN': 'xgNRZBevh7/Vpg==.Bamtws483hxZpQ+ymiqC+y0Ng/NSfZV+Ke60+6SAMJg=',
        'session_id': 'eb3b9644-20a3-419b-840e-c0abf8359d88',
        'dtCookie': f"5{env1}",
        'bm_sz': '3F020FB9F1A2D557B8D9735949FF08DC~YAAQTPo7F11wdHN4AQAA0ZnPjwspOAZn74hGYY3yUlX7gZU79w92N0bnzNyZJsMQmYr7WkVJvcJ1X2oO60VAIa48hsnyc6Dx3NLrEiQOgoG2Tc24osBsRP5e8LSr1ylGX4zF4OGbnYJzHOh0g/XyhYPqrBrltOA/qHMJbzNUhd2wwIKR2CULXxIOC22NiTBcOAQ=',
        'mt.sc': '%7B%22i%22%3A1617320451530%2C%22d%22%3A%5B%5D%7D',
        'mt.v': '2.1358662350.1617320451535',
        'at_check': 'true',
        's_ecid': 'MCMID%7C76463626635333007142587811141589522543',
        'AMCVS_5E16123F5245B2970A490D45%40AdobeOrg': '1',
        'mbox': 'session#dc2efc88a90a4008920120e90a323057#1617322312|PC#dc2efc88a90a4008920120e90a323057.34_0#1680565254',
        '_gcl_au': '1.1.1791247494.1617320453',
        's_cc': 'true',
        'AMCV_5E16123F5245B2970A490D45%40AdobeOrg': '-1124106680%7CMCIDTS%7C18719%7CMCMID%7C76463626635333007142587811141589522543%7CMCAID%7CNONE%7CMCOPTOUT-1617327653s%7CNONE%7CMCAAMLH-1617925253%7C7%7CMCAAMB-1617925253%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-18726%7CvVersion%7C5.2.0',
        'mt.mbsh': '%7B%22fs%22%3A1617320454207%7D',
        'rxVisitor': '1617320454406VPRPAGBPV367H8ORPODAEV0T3OV863N2',
        'bm_mi': '4DEC580FAA4B77739B6DC0861B5638FF~T8EbLeWiJn1kvx0pFZl+RDfnrs4hgQhpCG88kA2AGzDdeKN6Nhtx9yrXn0a7eo9t6xq5qDUZNwRg6IUdQXayQ/zNJwvsaiyj0FsN34dlyTirdtNUTotcbV7xRLLiuGmzgvdCsiwRHuDXznouTAHPzSXv3OIAPcdz/DYyJVTQqISa3nszu9dPMvMk0I+6uOCerLOQhqAAVTE801Ti+/i01bjrzwWbFJDqFjA0mZ2Ysa/WSrSFaQxLh2wlAMoUA4+dYjJceulkILsPS/NfMAcZwFdy367BvjyCSjn8JxFAL48xsTAG/iurhr260NOgyXU/',
        'wag_sid': 'u8lfocq6vzjq7gqrla9unzs7',
        'uts': '1617320463287',
        'ak_bmsc': 'F61F560B7D191563C45FB7E4A8BA702A173BFA4C2C2E0000025A666083B6AB3E~pl6zx3iJ8i4O9KPGF4NOiyauHTFpjmxg5JF2O064eRRwQ92A0VFrOnqGsMRIZ5lX+V+3cC9lQITzM4Q/qsOaCCDBIVw61RummqiuBDezGAoUvx3QUbmeAcKvmMWukJoV2mB3L/lCasiUKqbTvQSWhUQ0xHTY/v80aStl+Y6Bof0Q09m5i1HqJJR1rvqliFhqqX4vP+zGhEiGJ9nWJaE2qY5ay5jl9ZK/EMID2dgCNQgdk9xqYonbgcNzBvHq70OTiC',
        'fc_vnum': '1',
        'fc_vexp': 'true',
        'dtSa': '-',
        'USER_LOC': '5K48AZ9EjJsd1%2BhKAwBaTAuAIjJ7tdA3%2FnUIxy5wSvjTo6c5I8JPZfhLqcIjQ1HX',
        'gpv_Page': 'https%3A%2F%2Fwww.walgreens.com%2Ffindcare%2Fvaccination%2Fcovid-19%2Flocation-screening',
        'gRxAlDis': 'N',
        'rxvt': '1617322285467|1617320454412',
        'dtPC': f"5{env2}",
        '_abck': '4891F67D6739D24AEB164F19E9A9B464~0~YAAQTPo7F2twdHN4AQAALCXQjwVAtZ+nt2cbaKoAbSBeDeBoKKcHEramVXQJUNm7FWSd3acGnBveuVgIsJER2SLfjyFVJ9gt3CvMQ6p+0QoiB2uv8T+hIZM3rj0mLcwSDZnUXbhSl7D3TK3sneb9jebcqmmcNK7qszOA87zvpyCkG0xYiOtK9T7qGioS2lv8C/Q9LYeylkgT6CXYr6OFa7ZqN2Fd17SA7fh8bg3o7Bn+BwlfMHTuWIGn9Lkl1BlGSaiAxY6PhIZISQuxyjkDNdJigDRCfV2dZQHeQEUtW7zXgTFBpojKYMwZ0qmZY/fjkVaGsQwtZZOUsph0e0uLLRvdbMBicQCZIkM2or586ni0x5VAOdka4uC/2hcGRp2IsEzmXo0rFgP0glQv+88BZ7LR/FH4WonfLno7~-1~||-1||~-1',
        'dtLatC': '1',
        'akavpau_walgreens': '1617320789~id=990118b6a67c65a5cecb1d89438b7c2d',
        'bm_sv': '286440021695AE01FD01CDC4E54CF743~63x+T0EjbASjOvFoGUUBOobsa8/iIyOpN9V0nHlzLgXGzkGivVw1jYejbGdrFgn4nRXCpfQkWdG/PJUa8cNBoe7le6vbAWaRF+i8199KltadoLeUfiI7h0pYJqIeN0jh+KSEMSHL2hld/zPMhRbg1EjqQqBlBciHgwSIUS0o1e8=',
        's_sq': 'walgrns%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwg%25253Afindcare%25253Acovid19%252520vaccination%25253Alocation%25253Ascreening%2526link%253DSearch%2526region%253Dwag-body-main-container%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwg%25253Afindcare%25253Acovid19%252520vaccination%25253Alocation%25253Ascreening%2526pidt%253D1%2526oid%253DSearch%2526oidt%253D3%2526ot%253DSUBMIT',
    }

    headers = {
        'authority': 'www.walgreens.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not\\"A\\\\Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'dnt': '1',
        'x-xsrf-token': 'ofCzLBxw/HBMZQ==.8dBDpIgVTt1bCFWpkwauCT2nMAyphdguAnQIyuv7IRE=',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.walgreens.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = '{"position":{"latitude":' + lat + ',"longitude":' + long + '},"state":"' + state + '","vaccine":{"productId":""},"appointmentAvailability":{"startDateTime":"' + start_date + '"},"radius":25,"size":25,"serviceId":"99"}'

    response = requests.post('https://www.walgreens.com/hcschedulersvc/svc/v1/immunizationLocations/availability',
                             headers=headers, cookies=cookies, data=data)

    if response is not None and len(response.text) > 0:
        result = json.loads(response.text)
        if str(result["appointmentsAvailable"]) == "true":
            popup_and_store_info("Walgreens")


def get_lat_long(street, town, state_initials, zip):
    address = street + ", " + town + ", " + state_initials + " " + zip

    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return response[0]["lat"], response[0]["lon"]


def get_start_date():
    curr_date = datetime.today().strftime('%Y-%m-%d')
    start_day = str(int(curr_date[9:10]) + 1)
    if len(start_day) < 2:
        start_day = "0" + start_day
    return curr_date[0:8] + start_day


def popup_and_store_info(pharmacy):
    tz = timezone("EST")
    sg.popup_ok_cancel(pharmacy + ': COVID VACCINE AVAILABLE - check file', keep_on_top=True)

    out_file = open("Available Vaccine Locations", "a")
    out_file.write("\nAs of " + str(datetime.now(tz)) + ": \n")
    out_file.write("COVID-19 vaccine available at " + pharmacy + " in your area")
    out_file.close()


def check_all_pharmacies(street, town, state_initials, zip, dist_from_zip, freq):
    global pharmacy_errors_counts
    # in case improperly entered
    freq = int(freq)
    dist_from_zip = str(dist_from_zip)

    lat, long = get_lat_long(street, town, state_initials, zip)
    start_date = get_start_date()

    start_time = datetime.now()
    start_day = start_time.day

    pharmacy_errors_counts["CVS"] = 0
    pharmacy_errors_counts["RiteAid"] = 0
    pharmacy_errors_counts["Walgreens"] = 0
    pharmacy_errors_args["CVS"] = "null"
    pharmacy_errors_args["RiteAid"] = "null"
    pharmacy_errors_args["Walgreens"] = "null"

    config = {
        "apiKey": "AIzaSyCO153mNizXLbhHPYncEL5IniYRMDmEvFA",
        "authDomain": "vaccinefinder-309421.firebaseapp.com",
        "databaseURL": "https://vaccinefinder-309421-default-rtdb.firebaseio.com/",
        "storageBucket": "vaccinefinder-309421.appspot.com",
        "serviceAccount": ""
    }

    firebase = Firebase(config)
    fbase_ref = firebase.database()
    uid = fbase_report(fbase_ref, "uadd", state_initials)
    fbase_ref = fbase_ref.child(uid)

    print("Starting to search - You will see a popup if an available vaccine is found.")
    print("Vaccine locations will also be written to the file \"Available Vaccine Locations\" when found.")

    helper_all_pharmacies(zip, dist_from_zip, lat, long, state_initials, start_date, fbase_ref)

    while True:
        curr_time = datetime.now()
        if curr_time.minute % freq == 0:
            if start_day != curr_time.day:
                start_date = get_start_date()
                start_day = curr_time.day
            helper_all_pharmacies(zip, dist_from_zip, lat, long, state_initials, start_date, fbase_ref)

            time.sleep((freq) * 60)


def helper_all_pharmacies(zip, dist_from_zip, lat, long, state_initials, start_date, fbase_ref):
    global pharmacy_errors_args

    try:
        cvs_vaccines(zip, dist_from_zip)
        pharmacy_errors_counts["CVS"] = 0
    except Exception as e:
        pharmacy_errors_counts["CVS"] += 1
        pharmacy_errors_args["CVS"] = e.args
    try:
        rite_aid_vaccines(zip, dist_from_zip)
        pharmacy_errors_counts["RiteAid"] = 0
    except Exception as e:
        pharmacy_errors_counts["RiteAid"] += 1
        pharmacy_errors_args["RiteAid"] = e.args
    try:
        walgreens_vaccines(lat, long, state_initials, start_date)  # Walgreens requires 25 mile distance from zipcode
        pharmacy_errors_counts["Walgreens"] = 0
    except Exception as e:
        pharmacy_errors_counts["Walgreens"] += 1
        pharmacy_errors_args["Walgreens"] = e.args

    check_for_errors(fbase_ref)


def fbase_report(fbase_ref, key, value):
    try:
        if key == "uadd":
            return fbase_ref.push({key: value})["name"]
        fbase_ref.child(key).set(value)
    except Exception as e:
        return "failure"


def check_for_errors(fbase_ref):
    global printed_errors
    slen = len(printed_errors)

    for pharmacy in pharmacy_errors_counts.keys():
        if pharmacy_errors_counts[pharmacy] > 2 and pharmacy not in printed_errors:
            print("Error searching " + pharmacy + " database - problem reported to developer.")
            printed_errors.add(pharmacy)
            fbase_report(fbase_ref, pharmacy, pharmacy_errors_args[pharmacy])

    if len(printed_errors) != slen:
        print("All other pharmacies will continue working as expected.")


check_all_pharmacies(street, town, state_initials, zipcode, dist_from_zip, frequency)
