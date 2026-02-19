import random

DATASET = [
    {"uin": "ACON4NA202200082103", "iccid": "89916490634626390482", "imei": "868274067382103", "vin": "ACCDEV20222576271"},
    {"uin": "ACON4NA032300002587", "iccid": "89916420534723887726", "imei": "868274066878952", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA032300006206", "iccid": "89916420534724238267", "imei": "868274067373607", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA032300007045", "iccid": "89916420534723861705", "imei": "868274066913445", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA042300017276", "iccid": "89916420534724320743", "imei": "867018064975000", "vin": "PROA4G04072278723"},
    {"uin": "ACON4NA042300019957", "iccid": "89916420534724525416", "imei": "867018065647848", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA042300021793", "iccid": "89916420534724481495", "imei": "867018065546362", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA052300028666", "iccid": "89916420534724333977", "imei": "867018065645867", "vin": "MAT561004P0F12345"},
    {"uin": "ACON4NA032300002187", "iccid": "89916420534723923927", "imei": "868274066882426", "vin": "MAT12345678912345"},
    {"uin": "ACON4NA032300004343", "iccid": "89916420534724271664", "imei": "868274067389579", "vin": "MAT447153P2E11998"},
    {"uin": "ACON4NA032300004910", "iccid": "89916420534724232237", "imei": "868274067350290", "vin": "ILTA4G2905ORI9276"},
    {"uin": "ACON4NA042300009488", "iccid": "89916420534724267944", "imei": "868274066874761", "vin": "MAT835201P2F15286"},
    {"uin": "ACON4NA042300010295", "iccid": "89916420534724241790", "imei": "868274066904907", "vin": "MAT828045R2C05170"},
    {"uin": "ACON4NA042300010882", "iccid": "89916420534724196408", "imei": "868274066937774", "vin": "ILTA4G0602ORI6677"},
    {"uin": "ACON4NA042300011120", "iccid": "89916420534724343539", "imei": "868274067359275", "vin": "MAT805025RFD06587"},
    {"uin": "ACON4NA042300012602", "iccid": "89916420534724222915", "imei": "868274067351959", "vin": "ACCDEV20220476222"},
    {"uin": "ACON4NA042300020424", "iccid": "89916420534724375309", "imei": "868274066915523", "vin": "ACCDEV07242463882"},
    {"uin": "ACON4TA022300000042", "iccid": "89916420534723784550", "imei": "862614067298112", "vin": "ACCDEV07242463882"},
    {"uin": "ACON4NA052300031681", "iccid": "89916420534724306999", "imei": "867018065661930", "vin": "MAT513061PFE05898"},
    {"uin": "ACON4NA052300037362", "iccid": "89916420534724792271", "imei": "866824060213218", "vin": "PROA4G03092449859"},
    {"uin": "ACON4NA032300004899", "iccid": "89916420534723867454", "imei": "868274066943863", "vin": "MAT0050209038000R"},
    {"uin": "ACON4NA032300005159", "iccid": "89916420534724270484", "imei": "868274067385627", "vin": "ACCDEV07242463882"},
    {"uin": "ACON4NA032300002107", "iccid": "89916420534723924768", "imei": "868274066870793", "vin": "MAT883003S3C10288"},
    {"uin": "ACON4NA042300011731", "iccid": "89916420534724190625", "imei": "868274067388597", "vin": "ACCDEV14012076255"},
    {"uin": "ACON4NA032300005451", "iccid": "89916420534723870201", "imei": "868274066893902", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA052300032522", "iccid": "89916420534724563862", "imei": "867018065541264", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA042300007414", "iccid": "89916420534724237459", "imei": "868274067375040", "vin": "ACCDEV03236912090"},
    {"uin": "ACON4NA042300014890", "iccid": "89916420534724367967", "imei": "867018065090528", "vin": "ILTA4G2804EVT9604"},
    {"uin": "ACON4NA042300010877", "iccid": "89916420534724242137", "imei": "868274066945991", "vin": "MAT566021P3K31375"},
    {"uin": "ACON4NA042300014726", "iccid": "89916420534724360665", "imei": "867018065110102", "vin": "INTA4G0404V302738"},
    {"uin": "ACON4NA042300018239", "iccid": "89916420534724378626", "imei": "867018064971686", "vin": "MAT566007R1B03595"},
    {"uin": "ACON4NA012300000409", "iccid": "89916420534723112364", "imei": "867018061364158", "vin": "MAT563066P7D09001"},
    {"uin": "ACON4NA032300001707", "iccid": "89916420534723927811", "imei": "867018061476192", "vin": "ILTA4G2905ORI9318"},
    {"uin": "ACON4NA032300002349", "iccid": "89916420534723820800", "imei": "868274066899230", "vin": "ACCDEV07242470952"},
    {"uin": "ACON4NA032300002995", "iccid": "89916420534723886413", "imei": "868274066908783", "vin": "ILTA4G1006ORI9773"},
    {"uin": "ACON4NA032300003391", "iccid": "89916420534723822053", "imei": "868274066906332", "vin": "ACCDEV20323290395"},
    {"uin": "ACON4NA032300003388", "iccid": "89916420534723879608", "imei": "867018061574467", "vin": "MAT834002P2E12566"},
    {"uin": "ACON4NA042300007605", "iccid": "89916420534724258448", "imei": "868274067347312", "vin": "MAT566013P1C10489"},
    {"uin": "ACON4NA042300012293", "iccid": "89916420534724345120", "imei": "868274067393670", "vin": "MAT514019R5D08653"},
    {"uin": "ACON4NA042300021139", "iccid": "89916420534724522470", "imei": "867018065614400", "vin": "MATX1188042RP0540"},
    {"uin": "ACON4NA052300031020", "iccid": "89916420534724554861", "imei": "867018065640868", "vin": "SPUA4G2808CEV1341"},
    {"uin": "ACON4NA052300031110", "iccid": "89916420534724551768", "imei": "867018065611869", "vin": "INTA4G0404V306710"},
    {"uin": "ACON4NA042300019275", "iccid": "89916420534724496741", "imei": "867018065655577", "vin": "MAT883003S3C09146"},
    {"uin": "ACON4NA032500460328", "iccid": "89916450244842079535", "imei": "865827070500178", "vin": "ACCDEV03238799748"},
    {"uin": "ACON4NA032300001917", "iccid": "89916420534723926987", "imei": "868274066871700", "vin": "SPUA4G0412CEV0890"},
    {"uin": "ACON4NA042300010131", "iccid": "89916420534724347605", "imei": "868274067364101", "vin": "MAT883003S3B06178"},
    {"uin": "ACON4NA042300022564", "iccid": "89916420534724327300", "imei": "867018065562120", "vin": "MAT883003S3C10287"},
    {"uin": "ACON4NA042300022706", "iccid": "89916420534724513123", "imei": "867018064982972", "vin": "ACCDEV20222579317"},
    {"uin": "ACON4NA032300002679", "iccid": "89916420534723820628", "imei": "868274066899487", "vin": "ACCDEV07242552247"},
    {"uin": "ACON4NA042300009396", "iccid": "89916420534724265336", "imei": "868274067362899", "vin": "ACCDEV20222576270"},
    {"uin": "ACON4NA042300010838", "iccid": "89916420534724196770", "imei": "868274066923337", "vin": "MAT828061P2K26935"},
    {"uin": "ACON4NA042300020067", "iccid": "89916420534724525945", "imei": "867018065564589", "vin": "ACCDEV2022DEV2022"}
]


RTO_CODES = {
    "Andaman & Nicobar Islands": ["AN01", "AN02", "AN03"],
    "Andhra Pradesh": ["AP01", "AP02", "AP03", "AP04", "AP05", "AP07", "AP09", "AP10", "AP11", "AP12"],
    "Arunachal Pradesh": ["AR01", "AR02", "AR03", "AR04", "AR05", "AR06"],
    "Assam": ["AS01", "AS02", "AS03", "AS04", "AS05", "AS06", "AS07", "AS08", "AS09", "AS10"],
    "Bihar": ["BR01", "BR02", "BR03", "BR04", "BR05", "BR06", "BR07", "BR08", "BR09", "BR10"],
    "Chhattisgarh": ["CG01", "CG02", "CG03", "CG04", "CG05", "CG06", "CG07", "CG08"],
    "Goa": ["GA01", "GA02", "GA03", "GA04"],
    "Gujarat": ["GJ01", "GJ02", "GJ03", "GJ04", "GJ05", "GJ06", "GJ07", "GJ08", "GJ09", "GJ10"],
    "Haryana": ["HR01", "HR02", "HR03", "HR04", "HR05", "HR06", "HR07", "HR08", "HR09", "HR10"],
    "Himachal Pradesh": ["HP01", "HP02", "HP03", "HP04", "HP05", "HP06", "HP07", "HP08"],
    "Jammu & Kashmir": ["JK01", "JK02", "JK03", "JK04", "JK05", "JK06"],
    "Jharkhand": ["JH01", "JH02", "JH03", "JH04", "JH05", "JH06", "JH07", "JH08"],
    "Karnataka": ["KA01", "KA02", "KA03", "KA04", "KA05", "KA06", "KA07", "KA08", "KA09", "KA10"],
    "Kerala": ["KL01", "KL02", "KL03", "KL04", "KL05", "KL06", "KL07", "KL08", "KL09", "KL10"],
    "Ladakh": ["LA01", "LA02"],
    "Lakshadweep": ["LD01"],
    "Madhya Pradesh": ["MP01", "MP02", "MP03", "MP04", "MP05", "MP06", "MP07", "MP08", "MP09", "MP10"],
    "Maharashtra": ["MH01", "MH02", "MH03", "MH04", "MH05", "MH06", "MH07", "MH08", "MH09", "MH10"],
    "Manipur": ["MN01", "MN02"],
    "Meghalaya": ["ML01", "ML02", "ML03", "ML04"],
    "Mizoram": ["MZ01", "MZ02"],
    "Nagaland": ["NL01", "NL02", "NL03"],
    "Odisha": ["OD01", "OD02", "OD03", "OD04", "OD05", "OD06", "OD07", "OD08", "OD09", "OD10"],
    "Puducherry": ["PY01", "PY02", "PY03", "PY04"],
    "Punjab": ["PB01", "PB02", "PB03", "PB04", "PB05", "PB06", "PB07", "PB08", "PB09", "PB10"],
    "Rajasthan": ["RJ01", "RJ02", "RJ03", "RJ04", "RJ05", "RJ06", "RJ07", "RJ08", "RJ09", "RJ10"],
    "Sikkim": ["SK01", "SK02", "SK03", "SK04"],
    "Tamil Nadu": ["TN01", "TN02", "TN03", "TN04", "TN05", "TN06", "TN07", "TN08", "TN09", "TN10"],
    "Telangana": ["TS01", "TS02", "TS03", "TS04", "TS05", "TS06", "TS07", "TS08", "TS09", "TS10"],
    "Tripura": ["TR01", "TR02"],
    "Uttar Pradesh": ["UP01", "UP02", "UP03", "UP04", "UP05", "UP06", "UP07", "UP08", "UP09", "UP10"],
    "Uttarakhand": ["UK01", "UK02", "UK03", "UK04", "UK05"],
    "West Bengal": ["WB01", "WB02", "WB03", "WB04", "WB05", "WB06", "WB07", "WB08", "WB09", "WB10"],
    "Chandigarh": ["CH01"],
    "Dadra & Nagar Haveli and Daman & Diu": ["DN01", "DD01", "DD02"],
    "Delhi (NCT)": ["DL01", "DL02", "DL03", "DL04", "DL05", "DL06", "DL07", "DL08", "DL09", "DL10"]
}

# Internal dataset pointer
_index = 0

def get_all_data():
    """Return the full static dataset."""
    return DATASET

def reset_pointer():
    """Reset dataset iterator pointer."""
    global _index
    _index = 0


def get_next_record():
    """Return next record from dataset in sequence (loops automatically)."""
    global _index
    record = DATASET[_index % len(DATASET)]
    _index += 1
    return record


def get_next_uin():
    """Return next UIN in sequence."""
    return get_next_record()["uin"]


def get_next_iccid():
    """Return next ICCID in sequence."""
    return get_next_record()["iccid"]


def get_next_imei():
    """Return next IMEI in sequence."""
    return get_next_record()["imei"]


def get_next_vin():
    """Return next VIN in sequence."""
    return get_next_record()["vin"]

def get_random_record():
    """Return a random record from the dataset."""
    return random.choice(DATASET)


def get_record_by_index(index: int):
    """Return a record by its fixed index."""
    return DATASET[index % len(DATASET)]
