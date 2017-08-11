import requests
import re
import argparse

countrys={
"AF":["DZ","AO","BJ","BW","BF","BI","CM","CV","CF","TD","KM","CG","CD","CI","DJ","EG","GQ","ER","ET","GA","GM","GH","GN","GW","KE","LS","LR","LY","MG","MW","ML","MR","MU","YT","MA","MZ","NA","NE","NG","RE","RW","EH","SH","ST","SN","SC","SL","SO","ZA","SS","SD","SZ","TZ","TG","TN","UG","ZM","ZW"],
"AS":["AF","AM","AZ","BH","BD","BT","BN","KH","CN","CX","CC","CY","GE","HK","IN","ID","IR","IQ","IL","JP","JO","KZ","KW","KG","LA","LB","MO","MY","MV","FM","MN","ME","MM","NP","KP","OM","PK","PS","PH","QA","SA","RS","SG","KR","LK","SY","TW","TJ","TH","TM","AE","UZ","VN","YE"],
"AN":["AQ","BV","TF","HM","GS"],
"EU":["AX","AL","AD","AT","BY","BE","BA","IO","BG","HR","CZ","DK","EE","FO","FI","FR","DE","GI","GR","GG","HU","IS","IE","IM","IT","JE","XK","LV","LI","LT","LU","MK","MT","MD","MC","NL","AN","NO","PL","PT","RO","RU","SM","SK","SI","ES","SJ","SE","CH","TR","UA","GB","VA"],
"NA":["AI","AG","AW","BS","BB","BM","BQ","VG","CA","KY","CU","CW","DM","DO","GL","GD","GP","HT","JM","MQ","MX","MS","PR","BL","KN","LC","MF","PM","VC","SX","TT","TC","US","UM","VI"],
"OC":["AS","AU","CK","TL","FJ","PF","GU","KI","MH","NR","NC","NZ","NU","NF","MP","PW","PG","PN","WS","SB","TK","TO","TV","VU","WF"],
"SA":["AR","BZ","BO","BR","CL","CO","CR","EC","SV","FK","GF","GT","GY","HN","NI","PA","PY","PE","SR","UY","VE"]
}

# countrys={
# "AF1":["DZ","AO","BJ","BW","BF","BI","CM","CV","CF","TD","KM","CG","CD","CI","DJ","EG","GQ","ER","ET","GA","GM","GH","GN","GW","KE","LS","LR","LY"],
# "AF2":["MG","MW","ML","MR","MU","YT","MA","MZ","NA","NE","NG","RE","RW","EH","SH","ST","SN","SC","SL","SO","ZA","SS","SD","SZ","TZ","TG","TN","UG","ZM","ZW"],
# "AS1":["AF","AM","AZ","BH","BD","BT","BN","KH","CN","CX","CC","CY","GE","HK","IN","ID","IR","IQ","IL","JP","JO","KZ","KW","KG","LA","LB","MO"],
# "AS2":["MY","MV","FM","MN","ME","MM","NP","KP","OM","PK","PS","PH","QA","SA","RS","SG","KR","LK","SY","TW","TJ","TH","TM","AE","UZ","VN","YE"],
# "AN":["AQ","BV","TF","HM","GS"],
# "EU1":["AX","AL","AD","AT","BY","BE","BA","IO","BG","HR","CZ","DK","EE","FO","FI","FR","DE","GI","GR","GG","HU","IS","IE","IM","IT"],
# "EU2":["JE","XK","LV","LI","LT","LU","MK","MT","MD","MC","NL","AN","NO","PL","PT","RO","RU","SM","SK","SI","ES","SJ","SE","CH","TR","UA","GB","VA"],
# "NA":["AI","AG","AW","BS","BB","BM","BQ","VG","CA","KY","CU","CW","DM","DO","GL","GD","GP","HT","JM","MQ","MX","MS","PR","BL","KN","LC","MF","PM","VC","SX","TT","TC","US","UM","VI"],
# "OC":["AS","AU","CK","TL","FJ","PF","GU","KI","MH","NR","NC","NZ","NU","NF","MP","PW","PG","PN","WS","SB","TK","TO","TV","VU","WF"],
# "SA":["AR","BZ","BO","BR","CL","CO","CR","EC","SV","FK","GF","GT","GY","HN","NI","PA","PY","PE","SR","UY","VE"]
# }

def get_zones():
    '''
    Return a Set with the name of zones in ipdeny.com
    '''
    url_zones="http://www.ipdeny.com/ipblocks/data/aggregated/"
    resp=requests.get(url_zones)
    expre=re.compile("..-aggregated.zone")
    all_zones=expre.findall(resp.text)
    zones={i for i in all_zones}
    if debug:
        print("[/] Returned all zones")
    return zones
def get_blocks_ip_in_zone(zone):
    '''
    Return a List with blocks of IP in one zone
    '''
    url_zones="http://www.ipdeny.com/ipblocks/data/aggregated/" + zone
    resp=requests.get(url_zones)
    blocks=resp.text.split("\n")[:-1]
    if debug:
        print("[/] Requested IP blocks from {}".format(zone))
    return blocks
def continent_of_one_zone(zone):
    '''
    Returns a string with the ISO code of the continent to which the zone corresponds
    '''
    country=zone[:2].upper()
    for continent in countrys.keys():
        if country in countrys[continent]:
            return continent
    return "OT"
def generate_acl_dic_by_country():
    '''
    Return a Dic with this format {"country iso":["block1", "block2", "block3", ...]}
        Ej:
        {"ES":["1.1.0.0/24", "2.2.2.0/24",...],"DE":["3.3.3.0/24", ...]}
    '''
    acl_dic={}
    for zone in get_zones():
        country=zone[:2].upper()
        acl_dic[country]=get_blocks_ip_in_zone(zone)
        if debug:
            print("[/] Add {0} to the acl_dic".format(country))
    return acl_dic
def generate_acl_dic_by_continent():
    '''
    Return a Dic with this format {"continent":["block1", "block2", "block3", ...]}
        Ej:
        {"EU":["1.1.0.0/24", "2.2.2.0/24",...],"AF":["3.3.3.0/24", ...]}
    '''
    acl_dic={}
    cont_zones={}
    for zone in get_zones():
        continent=continent_of_one_zone(zone)
        try:
            cont_zones[continent].append(zone)
        except:
            cont_zones[continent]=[]
            cont_zones[continent].append(zone)
    for continent in cont_zones.keys():
        acl_dic[continent]=[]
        for zone in cont_zones[continent]:
                acl_dic[continent].extend(get_blocks_ip_in_zone(zone))
    return acl_dic

def generate_acl_file(acl_dic,path="./geo_acl.conf"):
    '''
    Generate a file with the acls for use in bind server
    '''
    acl_file=open(path, "w")
    for key in acl_dic.keys():
        acl_file.write('acl "%s" {\n' % key)
        for block in acl_dic[key]:
            acl_file.write('   {0};\n'.format(block))
        acl_file.write('};\n')
    acl_file.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Whit this tool you can generate files for use as acl in bind9 for example for configurate a CDN')
    parser.add_argument('-d', action="store_true", default=False, help='Debug mode', dest='debug')
    parser.add_argument('--country', action="store_true", help='Acl by country', dest='country')
    parser.add_argument('--continent', action="store_true", help='Acl by continent', dest='continent')
    parser.add_argument('-p', action='store', dest='path',help='Path to save the conf file',default="./geo_acl.conf")
    args=parser.parse_args()
    debug = args.debug
    if args.country:
        generate_acl_file(acl_dic=generate_acl_dic_by_country(), path=args.path)
    if args.continent:
        generate_acl_file(path=args.path, acl_dic=generate_acl_dic_by_continent())
