import flet as ft
from typing import List,Tuple
import socket
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import json
import requests
from retrying import retry
from icmplib import ping
import urllib.request
import urllib.parse
import os
import logging
import threading
wire_config_temp=''
wire_c=0
wire_p=0
best_result=[]
temp_conf=[]
WoW_v2=''
Wow=''
isIran=''
check="none"
best_ip = 0
best_result_avg=""
check=""
selected_index = 0
file_path = "/storage/emulated/0/Download/wwarpscanner/save_result.txt"
set_path="/storage/emulated/0/Download/wwarpscanner/settings.json"
width_path="/storage/emulated/0/Download/wwarpscanner/page_width.txt"
error=False
if not os.path.exists('/storage/emulated/0/Download/wwarpscanner'):
    try:
        os.makedirs('/storage/emulated/0/Download/wwarpscanner')
    except Exception:
        pass
async def main(page: ft.Page):
    page.title = "Warp Scanner"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    full_width_controls = []
    def load_settings():
        try:
            with open(set_path, "r") as f:
                settings = json.load(f)
                return {
                    "cpu_speed": settings.get("cpu_speed", "faster"),
                    "ping_range": settings.get("ping_range", 500),
                    "which_pannel": settings.get("which_pannel","bpb"),
                    "with_port": settings.get("with_port","no"),
                    "timeout": settings.get("timeout", 5),
                    "count": settings.get("count", 2),
                    "interval": settings.get("interval", 1),
                    "save_results": settings.get("save_results", "no")
                }
        except FileNotFoundError:
            return {
                "cpu_speed": "faster",
                "ping_range": 500,
                "timeout": 5,
                "count": 2,
                "interval": 1,
                "save_results": "no",
                "which_pannel": "bpb",
                "with_port":"no"
            }
    data=load_settings()
    class State:
        def __init__(self):
            self.results: List[Tuple[str, float, float, float, float]] = []
            self.sorted_results: List[Tuple[str, float, float, float, float]] = []
            self.current_config_type = "IP scanning"
            self.cpu_speed = data.get("cpu_speed","faster")
            self.save_results = data.get("save_results","no")
            self.with_port = data.get("with_port","no")
            self.which_pannel = data.get("which_pannel","bpb")
            self.selected_ip_version = "ipv4"
            self.ping_range = str(data.get("ping_range","500"))
            self.timeout = str(data.get("timeout","5"))
            self.count = str(data.get("count","2"))
            self.interval = str(data.get("interval","1"))
    state = State()
    def upload_to_bashupload(config_data):
            @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda x: isinstance(x, ConnectionError))
            def file_o():
                files = {'file': ('output.json', config_data)}
                try:
                    response = requests.post('https://bashupload.com/', files=files, timeout=30)
                except Exception:
                    response = requests.post('https://bashupload.com/', files=files, timeout=30)
                return response
            response = file_o()
            download_link = response.text.strip()
            download_link_with_query = download_link[59:len(download_link)-27] + "?download=1"
            true=""
            for i in download_link_with_query :
                if true=="":
                    if i != "b":
                        pass
                    else:
                        true="https://"
                        true+=i
                else:
                    true+=i
            return true
    def bind_keys():
        time.sleep(3)
        @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda x: isinstance(x, (ConnectionError, requests.exceptions.RequestException)))
        def file_o():
            try:
                api_url = "http://s9.serv00.com:1074/arshiacomplus/api/wirekey"
                response = requests.get(api_url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.exceptions.Timeout:
                logger.warning("bind_keys API request timed out.")
                raise ConnectionError("API Timeout")
            except requests.exceptions.RequestException as e:
                logger.error(f"bind_keys API request failed: {e}")
                raise ConnectionError(f"API request failed: {e}")
        try:
            response_text = file_o()
            if not response_text:
                logger.error("bind_keys: Received empty response from API.")
                return [None, None, [], None]
            lines = response_text.strip().splitlines()
            data = {}
            for line in lines:
                if ":" in line:
                    parts = line.split(":", 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    data[key] = value
                else:
                    logger.warning(f"bind_keys: Skipping malformed line (no ':'): '{line}'")
            address = data.get("address")
            priv_string = data.get("private_key")
            reserved_str = data.get("reserved")
            pub_key = data.get("public_key")
            if not all([address, priv_string, reserved_str, pub_key]):
                missing = [k for k in ["address", "private_key", "reserved", "public_key"] if k not in data]
                logger.error(f"bind_keys: Missing required keys in API response: {missing}. Received data: {data}")
                return [None, None, [], None]
            reserved = []
            items = reserved_str.split()
            for item in items:
                try:
                    reserved.append(int(item))
                except ValueError:
                    logger.warning(f"bind_keys: Could not convert reserved item '{item}' to int. Skipping.")
            logger.info("bind_keys: Parsed successfully.")
            return [address, priv_string, reserved, pub_key]
        except ConnectionError as e:
            logger.error(f"bind_keys: Failed to get data from API after retries: {e}")
            return [None, None, [], None]
        except Exception as e:
            logger.exception(f"bind_keys: Unexpected error during parsing: {e}")
            return [None, None, [], None]
    def get_wireguard_for_hiddify(best_ip,num):
        global best_result,wire_config_temp,wire_p
        ip, port, ping, loss_rate,jitter, combined_score=best_ip
        best_result=2*[1]
        if state.selected_ip_version=="ipv6":
            ip="["+ip+"]"
        best_result[0]=ip
        best_result[1]=port
        all_key=bind_keys()
        all_key2=bind_keys()
        print(dd_config_type.value)
        hising=f'''
            {{
            "type": "wireguard",
            "tag": "Tel=@arshiacomplus Warp-IR{num}",
            "local_address": [
                "172.16.0.2/32",
                "{all_key[0]}"
            ],
            "private_key": "{all_key[1]}",
            "peer_public_key": "{all_key[3]}",
            "server": "{best_result[0]}",
            "server_port": {best_result[1]},
            "reserved": {all_key[2]},
            "mtu": 1280'''
        if  dd_config_type.value=="wireguard for Hiddify without ip scanning" or dd_config_type.value=="wireguard for Hiddify" or dd_config_type.value=="wireguard for Hiddify with a sub link":
            print("noise")
            hising+=f''',
            "fake_packets":"1-3",
            "fake_packets_size":"10-30",
            "fake_packets_delay":"10-30",
            "fake_packets_mode":"m4"'''
        hising+=f'''
            }},'''
        hising+=f'''{{
            "type": "wireguard",
            "tag": "Tel=@arshiacomplus Warp-Main{num}",
            "detour": "Tel=@arshiacomplus Warp-IR{num}",
            "local_address": [
                "172.16.0.2/32",
                "{all_key2[0]}"
            ],
            "private_key": "{all_key2[1]}",
            "server": "{best_result[0]}",
            "server_port": {best_result[1]},
            "peer_public_key": "{all_key2[3]}",
            "reserved": {all_key2[2]},
            "mtu": 1330'''
        if  dd_config_type.value=="wireguard for Hiddify without ip scanning" or dd_config_type.value=="wireguard for Hiddify" or dd_config_type.value=="wireguard for Hiddify with a sub link":
            hising+=    f''',
            "fake_packets_mode":"m4"'''
        hising+=f"""
        }}"""
        if dd_config_type.value=="wireguard for Hiddify" or dd_config_type.value=="wireguard for Hiddify without ip scanning" or dd_config_type.value=="wireguard for Sing-box and Hiddify| old | without ip scanning":
            label_best.value= f'''{{
            "outbounds":
            [{hising}
            ]
            }}
            '''
            page.update()
            return
        elif dd_config_type.value=="wireguard for Hiddify with a sub link" or dd_config_type.value=="wireguard for Sing-box and Hiddify | old | with a sub link" :
            if wire_p==0:
                wire_config_temp+=hising
            else:
                wire_config_temp+=",\n"+hising
        wire_p+=1
        if str(wire_p)==tf_num_configs.value:
            print("i do")
            wire_config_temp2=f'''{{
            "outbounds":
            [{wire_config_temp}
            ]
            }}
            '''
            print(wire_config_temp2)
            lin=upload_to_bashupload(wire_config_temp2)
            print(lin)
            label_best.value= lin
            page.update()
            return
    def generate_wireguard_url(config, endpoint):
        def urlencode(string):
            if string is None:
                return None
            return urllib.parse.quote(string, safe='a-zA-Z0-9.~_-')
        required_keys = ['PrivateKey', 'PublicKey' ,'Address' ]
        if not all(key in config and config[key] is not None for key in required_keys):
            print("Incomplete configuration. Missing one of the required keys or value is None.")
            return None
        listt=config['Reserved']
        lostt2=''
        for num in range(len(listt)):
            lostt2+=str(listt[num])
            if num != len(listt)-1:
                lostt2+=','
        config['Reserved']=urlencode(lostt2)
        wireguard_urll = (
        f"wireguard://{urlencode(config['PrivateKey'])}@{endpoint}"
        f"?address=172.16.0.2/32,{urlencode(config['Address'])}&"
        f"publickey={urlencode(config['PublicKey'])}"
        )
        if dd_config_type.value=="wireguard for nikaNg and mahsaNg" or dd_config_type.value=="wireguard for nikaNg and mahsaNg without ip scanning":
                    wireguard_urll = (
        f"wireguard://{urlencode(config['PrivateKey'])}@{endpoint}"
        f"?wnoise=quic&address=172.16.0.2/32,{urlencode(config['Address'])}&keepalive=5&wpayloadsize=1-8&"
        f"publickey={urlencode(config['PublicKey'])}&wnoisedelay=1-3&wnoisecount=15&mtu=1330"
        )
    #wireguard://qO6m%2BpxSH677ETSmqykciE7MQ7rp0Jw8qJHSUh7Gj3k%3D@162.159.195.166:878?wnoise=quic&address=172.16.0.2%2F32%2C2606%3A4700%3A110%3A846c%3Ae510%3Abfa1%3Aea9f%3A5247%2F128&reserved=111%2C162%2C171&keepalive=5&wpayloadsize=1-8&publickey=bmXOC%2BF1FxEMF9dyiK2H5%2F1SUtzH0JuVo51h2wPfgyo%3D&wnoisedelay=1-3&wnoisecount=15&mtu=1280#Tel%3D+%40arshiacomplus+wire
        if config.get('Reserved'):
                    wireguard_urll += f"&reserved={config['Reserved']}"
        wireguard_urll += "#Tel= @arshiacomplus wire"
        return wireguard_urll
    def wow_nonoise_sub(n,ip,port):
        global WoW_v2
        all_key3=bind_keys()
        all_key2=bind_keys()
        best_result=2*[1]
        best_result[0]=ip
        best_result[1]=port
        WoW_v2+=f'''
    {{
        "remarks": "Tel= arshiacomplus - WoW",
        "log": {{
            "loglevel": "warning"
        }},
        "dns": {{
            "hosts": {{
                "geosite:category-ads-all": "127.0.0.1",
                "geosite:category-ads-ir": "127.0.0.1"'''
        WoW_v2+=f'''
            }},
            "servers": [
                "https://94.140.14.14/dns-query",
                {{
                    "address": "8.8.8.8",
                    "domains": [
                        "geosite:category-ir",
                        "domain:.ir"
                    ],
                    "expectIPs": [
                        "geoip:ir"
                    ],
                    "port": 53
                }}
            ],
            "tag": "dns"
        }},
        "inbounds": [
            {{
                "port": 10808,
                "protocol": "socks",
                "settings": {{
                    "auth": "noauth",
                    "udp": true,
                    "userLevel": 8
                }},
                "sniffing": {{
                    "destOverride": [
                        "http",
                        "tls"
                    ],
                    "enabled": true,
                    "routeOnly": true
                }},
                "tag": "socks-in"
            }},
            {{
                "port": 10809,
                "protocol": "http",
                "settings": {{
                    "auth": "noauth",
                    "udp": true,
                    "userLevel": 8
                }},
                "sniffing": {{
                    "destOverride": [
                        "http",
                        "tls"
                    ],
                    "enabled": true,
                    "routeOnly": true
                }},
                "tag": "http-in"
            }},
            {{
                "listen": "127.0.0.1",
                "port": 10853,
                "protocol": "dokodemo-door",
                "settings": {{
                    "address": "1.1.1.1",
                    "network": "tcp,udp",
                    "port": 53
                }},
                "tag": "dns-in"
            }}
        ],
        "outbounds": [
            {{
                "protocol": "wireguard",
                "settings": {{
                    "address": [
                        "172.16.0.2/32",
                        "{all_key3[0]}"
                    ],
                    "mtu": 1280,
                    "peers": [
                        {{
                            "endpoint": "{best_result[0]}:{best_result[1]}",
                            "publicKey": "{all_key3[3]}"
                        }}
                    ],
                    "reserved": {all_key3[2]},
                    "secretKey": "{all_key3[1]}"'''
        if dd_config_type.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
                    "keepAlive": 10,
                    "wnoise": "quic",
                    "wnoisecount": "10-15",
                    "wpayloadsize": "1-8",
                    "wnoisedelay": "1-3"'''
        WoW_v2+=f'''
                }},
                "streamSettings": {{
                    "sockopt": {{
                        "dialerProxy": "warp-ir"
                    }}
                }},
                "tag": "warp-out"
            }},
            {{
                "protocol": "wireguard",
                "settings": {{
                    "address": [
                        "172.16.0.2/32",
                        "{all_key2[0]}"
                    ],
                    "mtu": 1280,
                    "peers": [
                        {{
                            "endpoint": "162.159.192.115:864",
                            "publicKey": "{all_key2[3]}"
                        }}
                    ],
                    "reserved": {all_key2[2]},
                    "secretKey": "{all_key2[1]}"'''
        if dd_config_type.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
                    "keepAlive": 10,
                    "wnoise": "quic",
                    "wnoisecount": "10-15",
                    "wpayloadsize": "1-8",
                    "wnoisedelay": "1-3"'''
        WoW_v2+=f'''
                }},
                "tag": "warp-ir"
            }},
            {{
                "protocol": "dns",
                "tag": "dns-out"
            }},
            {{
                "protocol": "freedom",
                "settings": {{}},
                "tag": "direct"
            }},
            {{
                "protocol": "blackhole",
                "settings": {{
                    "response": {{
                        "type": "http"
                    }}
                }},
                "tag": "block"
            }}
        ],
        "policy": {{
            "levels": {{
                "8": {{
                    "connIdle": 300,
                    "downlinkOnly": 1,
                    "handshake": 4,
                    "uplinkOnly": 1
                }}
            }},
            "system": {{
                "statsOutboundUplink": true,
                "statsOutboundDownlink": true
            }}
        }},
        "routing": {{
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                {{
                    "inboundTag": [
                        "dns-in"
                    ],
                    "outboundTag": "dns-out",
                    "type": "field"
                }},
                {{
                    "ip": [
                        "8.8.8.8"
                    ],
                    "outboundTag": "direct",
                    "port": "53",
                    "type": "field"
                }},
                {{
                    "domain": [
                        "geosite:category-ir",
                        "domain:.ir"
                    ],
                    "outboundTag": "direct",
                    "type": "field"
                }},
                {{
                    "ip": [
                        "geoip:ir",
                        "geoip:private"
                    ],
                    "outboundTag": "direct",
                    "type": "field"
                }},
                {{
                    "domain": [
                        "geosite:category-ads-all",
                        "geosite:category-ads-ir"'''
        WoW_v2+=f'''
                    ],
                    "outboundTag": "block",
                    "type": "field"
                }},
                {{
                    "outboundTag": "warp-out",
                    "type": "field",
                    "network": "tcp,udp"
                }}
            ]
        }},
        "stats": {{}}
    }},
    {{
        "remarks": "Tel= arshiacomplus - Warp",
        "log": {{
            "loglevel": "warning"
        }},
        "dns": {{
            "hosts": {{
                "geosite:category-ads-all": "127.0.0.1",
                "geosite:category-ads-ir": "127.0.0.1"'''
        WoW_v2+=f'''
            }},
            "servers": [
                "https://94.140.14.14/dns-query",
                {{
                    "address": "8.8.8.8",
                    "domains": [
                        "geosite:category-ir",
                        "domain:.ir"
                    ],
                    "expectIPs": [
                        "geoip:ir"
                    ],
                    "port": 53
                }}
            ],
            "tag": "dns"
        }},
        "inbounds": [
            {{
                "port": 10808,
                "protocol": "socks",
                "settings": {{
                    "auth": "noauth",
                    "udp": true,
                    "userLevel": 8
                }},
                "sniffing": {{
                    "destOverride": [
                        "http",
                        "tls"
                    ],
                    "enabled": true,
                    "routeOnly": true
                }},
                "tag": "socks-in"
            }},
            {{
                "port": 10809,
                "protocol": "http",
                "settings": {{
                    "auth": "noauth",
                    "udp": true,
                    "userLevel": 8
                }},
                "sniffing": {{
                    "destOverride": [
                        "http",
                        "tls"
                    ],
                    "enabled": true,
                    "routeOnly": true
                }},
                "tag": "http-in"
            }},
            {{
                "listen": "127.0.0.1",
                "port": 10853,
                "protocol": "dokodemo-door",
                "settings": {{
                    "address": "1.1.1.1",
                    "network": "tcp,udp",
                    "port": 53
                }},
                "tag": "dns-in"
            }}
        ],
        "outbounds": [
            {{
                "protocol": "wireguard",
                "settings": {{
                    "address": [
                        "172.16.0.2/32",
                        "{all_key3[0]}"
                    ],
                    "mtu": 1280,
                    "peers": [
                        {{
                            "endpoint": "{best_result[0]}:{best_result[1]}",
                            "publicKey": "{all_key3[3]}"
                        }}
                    ],
                    "reserved": {all_key3[2]},
                    "secretKey": "{all_key3[1]}"'''
        if dd_config_type.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
                    "keepAlive": 10,
                    "wnoise": "quic",
                    "wnoisecount": "10-15",
                    "wpayloadsize": "1-8",
                    "wnoisedelay": "1-3"'''
        WoW_v2+=f'''
                }},
                "tag": "warp"
            }},
            {{
                "protocol": "dns",
                "tag": "dns-out"
            }},
            {{
                "protocol": "freedom",
                "settings": {{}},
                "tag": "direct"
            }},
            {{
                "protocol": "blackhole",
                "settings": {{
                    "response": {{
                        "type": "http"
                    }}
                }},
                "tag": "block"
            }}
        ],
        "policy": {{
            "levels": {{
                "8": {{
                    "connIdle": 300,
                    "downlinkOnly": 1,
                    "handshake": 4,
                    "uplinkOnly": 1
                }}
            }},
            "system": {{
                "statsOutboundUplink": true,
                "statsOutboundDownlink": true
            }}
        }},
        "routing": {{
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                {{
                    "inboundTag": [
                        "dns-in"
                    ],
                    "outboundTag": "dns-out",
                    "type": "field"
                }},
                {{
                    "ip": [
                        "8.8.8.8"
                    ],
                    "outboundTag": "direct",
                    "port": "53",
                    "type": "field"
                }},
                {{
                    "domain": [
                        "geosite:category-ir",
                        "domain:.ir"
                    ],
                    "outboundTag": "direct",
                    "type": "field"
                }},
                {{
                    "ip": [
                        "geoip:ir"
                    ],
                    "outboundTag": "direct",
                    "type": "field"
                }},
                {{
                    "domain": [
                        "geosite:category-ads-all",
                        "geosite:category-ads-ir"'''
        WoW_v2+=f'''
                    ],
                    "outboundTag": "block",
                    "type": "field"
                }},
                {{
                    "outboundTag": "warp",
                    "type": "field",
                    "network": "tcp,udp"
                }}
            ]
        }},
        "stats": {{}}
    }}'''
        if n !=int(tf_num_configs.value)-1:
            WoW_v2+=','
        return
    def wow_nonoise(ip,port):
        global isIran , Wow
        best_result=2*[1]
        best_result[0]=ip
        best_result[1]=port
        all_key=bind_keys()
        time.sleep(1)
        all_key2=bind_keys()
        temp_ip=''
        temp_port=''
        temp_c=0
        if dd_custom_loc.value=="Iran":
            isIran="1"
        elif dd_custom_loc.value=="Germany":
            isIran="2"
        Wow=f'''{{
"dns": {{
    "hosts": {{
    "geosite:category-ads-all": "127.0.0.1",
    "geosite:category-ads-ir": "127.0.0.1"'''
        if isIran=='1' :
                Wow+=f'''
    }},
    "servers": [
    "https://94.140.14.14/dns-query",
    {{
        "address": "8.8.8.8",
        "domains": [
        "geosite:category-ir",
        "domain:.ir"
        ],
        "expectIPs": [
        "geoip:ir"
        ],
        "port": 53
    }}
    ],
    "tag": "dns"
}},
"inbounds": [
    {{
    "port": 10808,
    "protocol": "socks",
    "settings": {{
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
    }},
    "sniffing": {{
        "destOverride": [
        "http",
        "tls"
        ],
        "enabled": true
    }},
    "tag": "socks-in"
    }},
    {{
    "port": 10809,
    "protocol": "http",
    "settings": {{
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
    }},
    "sniffing": {{
        "destOverride": [
        "http",
        "tls"
        ],
        "enabled": true
    }},
    "tag": "http-in"
    }},
    {{
    "listen": "127.0.0.1",
    "port": 10853,
    "protocol": "dokodemo-door",
    "settings": {{
        "address": "1.1.1.1",
        "network": "tcp,udp",
        "port": 53
    }},
    "tag": "dns-in"
    }}
],
"log": {{
    "loglevel": "warning"
}},
"outbounds": [
    {{
    "protocol": "wireguard",
    "settings": {{
        "address": [
        "172.16.0.2/32",
        "{all_key[0]}"
        ],
        "mtu": 1280,
        "peers": [
        {{
            "endpoint": "{best_result[0]}:{best_result[1]}",
            "publicKey": "{all_key[3]}"
        }}
        ],
        "reserved": {all_key[2]},
        "secretKey": "{all_key[1]}"'''
                if dd_config_type.value=="WoW with noise for Nikang or MahsaNg":Wow+=''',
        "keepAlive": 10,
        "wnoise": "quic",
        "wnoisecount": "10-15",
        "wpayloadsize": "1-8",
        "wnoisedelay": "1-3"'''
                Wow+=f'''
    }},
    "tag": "warp"
    }},
    {{
    "protocol": "dns",
    "tag": "dns-out"
    }},
    {{
    "protocol": "freedom",
    "settings": {{}},
    "tag": "direct"
    }},
    {{
    "protocol": "blackhole",
    "settings": {{
        "response": {{
        "type": "http"
        }}
    }},
    "tag": "block"
    }}
],
"policy": {{
    "levels": {{
    "8": {{
        "connIdle": 300,
        "downlinkOnly": 1,
        "handshake": 4,
        "uplinkOnly": 1
    }}
    }},
    "system": {{
    "statsOutboundUplink": true,
    "statsOutboundDownlink": true
    }}
}},
"remarks": "Tel= Arshiacomplus - Warp",
"routing": {{
    "domainStrategy": "IPIfNonMatch",
    "rules": [
    {{
        "inboundTag": [
        "dns-in"
        ],
        "outboundTag": "dns-out",
        "type": "field"
    }},
    {{
        "ip": [
        "8.8.8.8"
        ],
        "outboundTag": "direct",
        "port": "53",
        "type": "field"
    }},
    {{
        "domain": [
        "geosite:category-ir",
        "domain:.ir"
        ],
        "outboundTag": "direct",
        "type": "field"
    }},
    {{
        "ip": [
        "geoip:ir",
        "geoip:private"
        ],
        "outboundTag": "direct",
        "type": "field"
    }},
    {{
        "domain": [
        "geosite:category-ads-all",
        "geosite:category-ads-ir"'''
                Wow+='''
        ],
        "outboundTag": "block",
        "type": "field"
    },
    {
        "network": "tcp,udp",
        "outboundTag": "warp",
        "type": "field"
    }
    ]
},
"stats": {}
}'''
        if isIran == '2' :
                Wow+=f'''
    }},
    "servers": [
    "https://94.140.14.14/dns-query",
    {{
        "address": "8.8.8.8",
        "domains": [
        "geosite:category-ir",
        "domain:.ir"
        ],                                                              "expectIPs": [                                                    "geoip:ir"
        ],
        "port": 53                                                    }}
    ],
    "tag": "dns"                                                  }},
"inbounds": [
    {{
    "port": 10808,
    "protocol": "socks",
    "settings": {{
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
    }},
    "sniffing": {{
        "destOverride": [
        "http",
        "tls"
        ],
        "enabled": true
    }},
    "tag": "socks-in"
    }},
    {{
    "port": 10809,
    "protocol": "http",
    "settings": {{
        "auth": "noauth",
        "udp": true,
        "userLevel": 8
    }},
    "sniffing": {{
        "destOverride": [
        "http",
        "tls"
        ],
        "enabled": true
    }},
    "tag": "http-in"
    }},
    {{
    "listen": "127.0.0.1",
    "port": 10853,
    "protocol": "dokodemo-door",
    "settings": {{
        "address": "1.1.1.1",
        "network": "tcp,udp",
        "port": 53
    }},
    "tag": "dns-in"
    }}
],
"log": {{
    "loglevel": "warning"
}},
"outbounds": [
    {{
    "protocol": "wireguard",
    "settings": {{
        "address": [
        "172.16.0.2/32",
        "{all_key[0]}"
        ],
        "mtu": 1280,
        "peers": [
        {{
            "endpoint": "{best_result[0]}:{best_result[1]}",
            "publicKey": "{all_key[3]}"
        }}
        ],
        "reserved": {all_key[2]},
        "secretKey": "{all_key[1]}"
    }},
    "streamSettings": {{
        "network": "tcp",
        "security": "",
        "sockopt": {{
        "dialerProxy": "warp-ir"
        }}
    }},
    "tag": "warp-out"
    }},
    {{
    "protocol": "wireguard",
    "settings": {{
        "address": [
        "172.16.0.2/32",
        "{all_key2[0]}"
        ],
        "mtu": 1280,
        "peers": [
        {{
            "endpoint": "{best_result[0]}:{best_result[1]}",
            "publicKey": "{all_key[3]}"
        }}
        ],
        "reserved": {all_key2[2]},
        "secretKey": "{all_key2[1]}"'''
                if dd_config_type.value=="WoW with noise for Nikang or MahsaNg":Wow+=''',
        "keepAlive": 10,
        "wnoise": "quic",
        "wnoisecount": "10-15",
        "wpayloadsize": "1-8",
        "wnoisedelay": "1-3"'''
                Wow+=f'''
    }},
    "tag": "warp-ir"
    }},
    {{
    "protocol": "dns",
    "tag": "dns-out"
    }},
    {{
    "protocol": "freedom",
    "settings": {{}},
    "tag": "direct"
    }},
    {{
    "protocol": "blackhole",
    "settings": {{
        "response": {{
        "type": "http"
        }}
    }},
    "tag": "block"
    }}
],
"policy": {{
    "levels": {{
    "8": {{
        "connIdle": 300,
        "downlinkOnly": 1,
        "handshake": 4,
        "uplinkOnly": 1
    }}
    }},
    "system": {{
    "statsOutboundUplink": true,
    "statsOutboundDownlink": true
    }}
}},
"remarks": "Tel = arshiacomplus - WoW",
"routing": {{
    "domainStrategy": "IPIfNonMatch",
    "rules": [
    {{
        "inboundTag": [
        "dns-in"
        ],
        "outboundTag": "dns-out",
        "type": "field"
    }},
    {{
        "ip": [
        "8.8.8.8"
        ],
        "outboundTag": "direct",
        "port": "53",
        "type": "field"
    }},
    {{
        "domain": [
        "geosite:category-ir",
        "domain:.ir"
        ],
        "outboundTag": "direct",
        "type": "field"
    }},
    {{
        "ip": [
        "geoip:ir",
        "geoip:private"
        ],
        "outboundTag": "direct",
        "type": "field"
    }},
    {{
        "domain": [
        "geosite:category-ads-all",
        "geosite:category-ads-ir"'''
        if isIran == '2' :
            Wow+=f'''
        ],
        "outboundTag": "block",
        "type": "field"
    }},
    {{
        "network": "tcp,udp",
        "outboundTag": "warp-out",
        "type": "field"
    }},
    {{
        "network": "tcp,udp",
        "outboundTag": "warp",
        "type": "field"
    }}
    ]
}},
"stats": {{}}
}}'''
        return Wow
    async def start_scan(ip_version):
        try:
            btn_scan_ipv4.disabled = True
            btn_scan_ipv6.disabled = True
            btn_clean.disabled= True
            page.update()
            state.results.clear()
            state.sorted_results.clear()
            tbl_results.rows.clear()
            page.update()
            if dd_config_type.value=="wireguard for Hiddify without ip scanning" or dd_config_type.value=="wireguard for Sing-box and Hiddify| old | without ip scanning":
                get_wireguard_for_hiddify((tf_custom_ip.value,int(tf_custom_port.value),0,0,0,0),1)
                btn_scan_ipv4.disabled = False
                btn_scan_ipv6.disabled = False
                btn_clean.disabled= False
                page.update()
                return
            elif dd_config_type.value=="wireguard for v2ray and mahsaNG without ip scanning" or dd_config_type.value=="wireguard for nikaNg and mahsaNg without ip scanning":
                        print("w_no")
                        def go():
                            bi=bind_keys()
                            bi={
                                'PrivateKey': bi[1],
                                'PublicKey': bi[3],
                                'Reserved': bi[2],
                                'Address': bi[0]
                            }
                            wrg=generate_wireguard_url(bi,str(tf_custom_ip.value)+":"+str(tf_custom_port.value))
                            label_best.value=wrg
                            page.update()
                        go()
                        btn_scan_ipv4.disabled = False
                        btn_scan_ipv6.disabled = False
                        btn_clean.disabled= False
                        page.update()
                        return
        except Exception as e:
            snake.content=ft.Text(f"Error: {str(e)}", color=ft.Colors.RED)
            snake.open = True
            page.update()
        try:
            state.ping_range = int(tf_ping_range.value)
            state.timeout = int(tf_timeout.value)
            state.count = int(tf_count.value)
            state.interval = float(tf_interval.value)
            ips = []
            ports = []
            if ip_version == "ipv4":
                start_ips = ["188.114.96.0", "162.159.192.0", "162.159.195.0"]
                end_ips = ["188.114.99.224", "162.159.193.224", "162.159.195.224"]
                for start, end in zip(start_ips, end_ips):
                    ips.extend(generate_ipv4_range(start, end))
                ports = [1074, 894]
            else:
                ips = [generate_ipv6() for _ in range(101)]
                ports = [1074, 864]
            await asyncio.get_event_loop().run_in_executor(
                ThreadPoolExecutor(),
                lambda: run_scan(page, ips, ports, ip_version)
            )
            wich_pannel=state.which_pannel
            port_go=state.with_port
            ping_range_see=int(state.ping_range)
            save_result=[]
            if state.save_results=="yes":
                if wich_pannel!="with score":
                            for ip, port, ping, loss_rate,jitter, combined_score in state.sorted_results:
                                    if loss_rate == 0.00 and ping != 0.0 and ping < ping_range_see:
                                        if port_go=="no":
                                                if wich_pannel=="bpb":
                                                    save_result.append(",")
                                                    save_result.append(str(ip))
                                                else:
                                                    save_result.append("\n")
                                                    save_result.append(str(ip))
                                        else:
                                                if wich_pannel=="bpb":
                                                    save_result.append(",")
                                                    save_result.append(str(ip)+":"+str(port))
                                                else:
                                                    save_result.append("\n")
                                                    save_result.append(str(ip)+":"+str(port))
                if wich_pannel=="with score":
                    for ip, port, ping, loss_rate,jitter, combined_score in state.sorted_results:
                        if ping <=ping_range_see:
                            if port_go=="no":
                                        save_result.append("\n")
                                        save_result.append(ip+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter))
                            else:
                                        save_result.append("\n")
                                        save_result.append(ip+":"+str(port)+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter))
                with open(file_path,"w") as f:
                    f.writelines(save_result)
            print("ifin")
        except Exception as e:
            snake.content=ft.Text(f"Error: {str(e)}", color=ft.Colors.RED)
            snake.open = True
            page.update()
        btn_scan_ipv4.disabled = False
        btn_scan_ipv6.disabled = False
        btn_clean.disabled= False
        page.update()
        st=dd_scan_type.value
        if st!="IP scanning":
            st=dd_config_type.value
            if st=="wireguard for Hiddify with a sub link"  or st=="wireguard for Sing-box and Hiddify | old | with a sub link":
                print("issub")
                for i in range(int(tf_num_configs.value)):
                        get_wireguard_for_hiddify(state.sorted_results[0],i)
                page.update()
                return
            elif st=="wireguard for Hiddify" or st=="wireguard for Sing-box and Hhidify | old |":
                print("i went")
                get_wireguard_for_hiddify(state.sorted_results[0],1)
                page.update()
                return
            elif st=="wireguard for v2ray and mahsaNG" or st=="wireguard for nikaNg and mahsaNg":
                def go():
                    bi=bind_keys()
                    bi={
                        'PrivateKey': bi[1],
                        'PublicKey': bi[3],
                        'Reserved': bi[2],
                        'Address': bi[0]
                    }
                    rgg=generate_wireguard_url(bi,str(state.sorted_results[0][0])+":"+str(state.sorted_results[0][1]))
                    label_best.value=rgg
                    page.update()
                go()
                return
            elif st=="WoW with noise for Nikang or MahsaNg" or st=="WoW for v2ray or mahsaNG":
                tet=wow_nonoise(state.sorted_results[0][0],state.sorted_results[0][1])
                label_best.value= tet
                page.update()
                return
            elif st=="WoW with noise for Nikang or MahsaNg in sub link" or st=="WoW for v2ray or mahsaNG in sub link":
                WoW_v2 = ""
                for ii in range(int(tf_num_configs.value)):
                        b=wow_nonoise_sub(ii,state.sorted_results[0][0],state.sorted_results[0][1])
                WoW_v2=upload_to_bashupload("["+WoW_v2+"]")
                label_best.value=WoW_v2
                page.update()
                WoW_v2=""
                return
    async def copy_result(page: ft.Page):
        page.set_clipboard(label_best.value)
        page.update()
    def run_scan(page: ft.Page, ips, ports, ip_version):
        results = []
        try:
            with ThreadPoolExecutor(max_workers=100 if dd_cpu_speed.value == "faster" else 50) as executor:
                futures = [
                    executor.submit(
                        ping_ip,
                        ip,
                        random.choice(ports),
                        state.timeout,
                        state.count,
                        state.interval,
                        ip_version
                    )
                    for ip in ips
                ]
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                    except Exception as e:
                        print(f"Scan error: {e}")
                page.run_task(process_results, page, results)
        except Exception as E:
            print(E)
    def change_state(page: ft.Page):
        st=dd_scan_type.value
        if st!="IP scanning":
            dd_config_type.visible=True
            change_config_format(page)
        else:
            dd_config_type.visible=False
            tf_num_configs.visible=False
            tf_custom_ip.visible=False
            tf_custom_port.visible=False
            dd_custom_loc.visible=False
        state.current_config_type=st
        page.update()
    def change_config_format(page: ft.Page):
        val=dd_config_type.value
        tf_num_configs.visible=False
        tf_custom_ip.visible=False
        tf_custom_port.visible=False
        dd_custom_loc.visible=False
        if val=="wireguard for Sing-box and Hiddify | old | with a sub link" or val=="WoW with noise for Nikang or MahsaNg in sub link" or val=="WoW for v2ray or mahsaNG in sub link" or val=="wireguard for Hiddify with a sub link":
            tf_num_configs.visible=True
        elif val=="wireguard for Hiddify without ip scanning" or val=="wireguard for Sing-box and Hiddify| old | without ip scanning" or val=="wireguard for v2ray and mahsaNG without ip scanning" or val=="wireguard for nikaNg and mahsaNg without ip scanning":
            tf_custom_ip.visible=True
            tf_custom_port.visible=True
        elif val=="WoW for v2ray or mahsaNG" or val == "WoW with noise for Nikang or MahsaNg":
            dd_custom_loc.visible=True
        page.update()
    lbl_ipv4 = ft.Text(value="IPv4: Checking...", color=ft.Colors.GREY)
    lbl_ipv6 = ft.Text(value="IPv6: Checking...", color=ft.Colors.GREY)
    page_width=page.width
    if not  os.path.exists(width_path):
        if page.width!=0.0:
            with open(width_path, "w") as f:
                f.write(str(page.width))
    else:
        if page.width==0.0:
            with open(width_path, "r") as f:
                page_width=float(f.readline())
    dd_scan_type = ft.Dropdown(
        width=page_width,
        label="Scan Type",
        options=[
            ft.dropdown.Option("IP scanning"),
            ft.dropdown.Option("Get config")
        ],
        value="IP scanning",
        on_change=lambda _:change_state(page),
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_scan_type)
    dd_config_type = ft.Dropdown(
        width=page_width,
        label="Config Type",
        options=[
            ft.dropdown.Option("wireguard for Hiddify"),
            ft.dropdown.Option("wireguard for Hiddify without ip scanning"),
            ft.dropdown.Option("wireguard for Hiddify with a sub link"),
            ft.dropdown.Option("wireguard for v2ray and mahsaNG"),
            ft.dropdown.Option("wireguard for v2ray and mahsaNG without ip scanning"),
            ft.dropdown.Option("WoW for v2ray or mahsaNG"),
            ft.dropdown.Option("WoW for v2ray or mahsaNG in sub link"),
            ft.dropdown.Option("wireguard for nikaNg and mahsaNg"),
            ft.dropdown.Option("wireguard for nikaNg and mahsaNg without ip scanning"),
            ft.dropdown.Option("WoW with noise for Nikang or MahsaNg"),
            ft.dropdown.Option("WoW with noise for Nikang or MahsaNg in sub link"),
            ft.dropdown.Option("wireguard for Sing-box and Hiddify | old |"),
            ft.dropdown.Option("wireguard for Sing-box and Hiddify| old | without ip scanning"),
            ft.dropdown.Option("wireguard for Sing-box and Hiddify | old | with a sub link")
        ],
        on_change=lambda _:change_config_format(page),
        visible=False,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_config_type)
    tf_num_configs = ft.TextField(
        label="Number of Configs",
        visible=False,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    tf_custom_ip = ft.TextField(
        label="Custom IP",
        visible=False,
        expand=True
    )
    tf_custom_port = ft.TextField(
        label="Custom Port",
        visible=False,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    dd_custom_loc= ft.Dropdown(
        width=page_width,
        label="Location",
        options=[
            ft.dropdown.Option("Iran"),
            ft.dropdown.Option("Germany")
        ],
        on_change=lambda _:change_config_format(page),
        visible=False,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_custom_loc)
    def check_ipv6():
        try:
            ipv6 = requests.get('http://v6.ipv6-test.com/api/myip.php',timeout=30)
            if ipv6.status_code == 200:
                ipv6 ="Available"
        except Exception:
            ipv6 = "Unavailable"
        try:
            ipv4 = requests.get('http://v4.ipv6-test.com/api/myip.php',timeout=30)
            if ipv4.status_code == 200:
                ipv4= "Available"
        except Exception:
            ipv4 = "Unavailable"
        return  [ipv4,ipv6]
    async def clean2():
        if not os.path.exists(file_path):
            result_view.controls = [
                ft.Text("No results file found to clean. Please run a scan first with 'Save Results' enabled.", color=ft.Colors.YELLOW)
            ]
            page.update()
            return
        with open(file_path, 'r') as f:
                b=f.readlines()
                with open('/storage/emulated/0/Download/wwarpscanner/clean_result.txt', 'w') as ff:
                    for j in b:
                            try:
                                if state.which_pannel =='bpb':
                                    ff.write(j[:j.index('|')-1])
                                    if j != b[len(b)-1]:
                                        ff.write(',')
                                else:
                                    ff.write(j[:j.index('|')-1])
                                    ff.write('\n')
                            except Exception:
                                pass
        result_view.controls = [
            ft.Text("cleaned saved to /storage/emulated/0/Download/wwarpscanner/clean_result.txt!", color=ft.Colors.GREEN)
        ]
    def theard_check_ip6_again():
            def check_ip6_again():
                            global check
                            print("go")
                            check="none"
                            check=  check_ipv6()
                            color1="red"
                            color2="red"
                            if  check[0] == "Available":
                                color1=ft.Colors.GREEN
                            else:
                                color1=ft.Colors.RED
                            if  check[1] == "Available":
                                color2=ft.Colors.GREEN
                            else:
                                color2=ft.Colors.RED
                            lbl_ipv4.value= f"ipv4 : {check[0]}"
                            lbl_ipv4.color=color1
                            lbl_ipv6.value= f"ipv6 : {check[1]}"
                            lbl_ipv6.color=color2
                            main_tab.update()
            lbl_ipv4.value= "IPv4: Checking..."
            lbl_ipv4.color=ft.Colors.GREY
            lbl_ipv6.value="IPv6: Checking..."
            lbl_ipv6.color= ft.Colors.GREY
            main_tab.update()
            threading.Thread(target=check_ip6_again).start()
    btn_check = ft.ElevatedButton(
        "Check Connectivity",
        icon=ft.Icons.WIFI_FIND,
        on_click=lambda e: theard_check_ip6_again()
    )
    btn_scan_ipv4 = ft.ElevatedButton(
        "Scan IPv4",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: page.run_task(start_scan, "ipv4")
    )
    btn_scan_ipv6 = ft.ElevatedButton(
        "Scan IPv6",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: page.run_task(start_scan, "ipv6"),
        color=ft.Colors.BLUE
    )
    btn_clean = ft.ElevatedButton(
        "Clean",
        icon=ft.Icons.CLEAN_HANDS,
        on_click=lambda e: page.run_task(clean2),
        color=ft.Colors.RED_900
    )
    result_view = ft.ListView(expand=True)
    tbl_results = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("IP")),
            ft.DataColumn(ft.Text("Ping (ms)")),
            ft.DataColumn(ft.Text("Loss %")),
            ft.DataColumn(ft.Text("Jitter")),
            ft.DataColumn(ft.Text("Score")),
        ],
        rows=[],
        #
        column_spacing=40,
        sort_column_index=0,
        sort_ascending=True
    )
    dd_cpu_speed = ft.Dropdown(
        width=page_width,
        label="CPU Speed",
        options=[ft.dropdown.Option("faster"), ft.dropdown.Option("slower")],
        value=state.cpu_speed,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_cpu_speed)
    dd_save_results = ft.Dropdown(
        width=page_width,
        label="Save Results",
        options=[ft.dropdown.Option("yes"), ft.dropdown.Option("no")],
        value=state.save_results,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_save_results)
    dd_which_pannl = ft.Dropdown(
        width=page_width,
        label="Which Pannel",
        options=[ft.dropdown.Option("bpb"),
                 ft.dropdown.Option("vahid"),
                 ft.dropdown.Option("with score")
                 ],
        value=state.which_pannel,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_which_pannl)
    dd_with_port = ft.Dropdown(
        width=page_width,
        label="With Port",
        options=[ft.dropdown.Option("yes"), ft.dropdown.Option("no")],
        value=state.with_port,
        bgcolor=ft.Colors.GREY_900
    )
    full_width_controls.append(dd_with_port)
    tf_ping_range = ft.TextField(
        label="Ping Range (ms)",
        value=state.ping_range,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    tf_timeout = ft.TextField(
        label="Timeout (s)",
        value=state.timeout,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    tf_count = ft.TextField(
        label="Ping Count",
        value=state.count,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    tf_interval = ft.TextField(
        label="Interval (s)",
        value=state.interval,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )
    btn_save_settings = ft.ElevatedButton(
        "Save Settings",
        icon=ft.Icons.SAVE,
        on_click=lambda _: save_settings()
    )
    label_best = ft.TextField(
        label="config",
        value="",
        multiline=True,
        text_size=12,
        height=60,
        adaptive=True,
        expand=True
    )
    btn_copy_best = ft.IconButton(
        icon=ft.Icons.COPY,
        tooltip="Copy config",
        on_click=lambda _: page.run_task( copy_result,page),
        adaptive=True
    )
    snake=ft.SnackBar(
        content=ft.Text("Settings saved successfully!", color=ft.Colors.GREEN)
    )
    dlg = ft.AlertDialog(
        title=ft.Text("Need Premission"),
        actions_alignment=ft.MainAxisAlignment.END
    )
    responsive_table_container = ft.ResponsiveRow(
        [tbl_results],
        expand=True,
        adaptive=True,
        vertical_alignment=ft.CrossAxisAlignment.START
    )
    main_tab = ft.Container(
        expand=True,
        margin=ft.margin.only(bottom=65),
        content=ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
             expand=True,
            controls=[
            snake,
            ft.ResponsiveRow([lbl_ipv4, lbl_ipv6, btn_check]),
            ft.Divider(),
            ft.ResponsiveRow([
                dd_scan_type,
                dd_config_type,
                tf_num_configs,
                tf_custom_ip,
                tf_custom_port,
                dd_custom_loc
            ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                adaptive=True
            ),
            ft.ResponsiveRow([btn_scan_ipv4, btn_scan_ipv6, btn_clean]),
            ft.Divider(),
            ft.Text("Results:", size=20, weight=ft.FontWeight.BOLD),
            ft.ResponsiveRow(controls=[label_best,btn_copy_best]),
            result_view
        ])
    )
    table_tab = ft.Container(
        expand=True,
        visible=False,
        margin=ft.margin.only(bottom=65),
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                snake,
                ft.Text("Scan Results", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(responsive_table_container, padding=10,expand=True)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            ),
    )
    settings_tab = ft.Container(
        expand=True,
        visible=False,
        padding=ft.padding.only(bottom=65, left=10, right=10, top=10),
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
            controls=[
            snake,
            ft.Text("Configuration", size=20, weight=ft.FontWeight.BOLD),
            ft.ResponsiveRow([dd_cpu_speed, dd_save_results,
                            dd_which_pannl,dd_with_port,
                            tf_ping_range, tf_timeout,
                            tf_count, tf_interval,
                            ]),
            ft.Divider(),
            btn_save_settings
        ])
    )
    bottom_nav = ft.Container(
        height=60,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.OUTLINE)),
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    icon_color=ft.Colors.ON_SURFACE,
                    selected_icon_color=ft.Colors.PRIMARY,
                    on_click=lambda e: switch_tab(0),
                    selected=(selected_index == 0)
                ),
                ft.IconButton(
                    icon=ft.Icons.TABLE_VIEW_OUTLINED,
                    selected_icon=ft.Icons.TABLE_VIEW,
                    icon_color=ft.Colors.ON_SURFACE,
                    selected_icon_color=ft.Colors.PRIMARY,
                    on_click=lambda e: switch_tab(1),
                    selected=(selected_index == 1)
                ),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    icon_color=ft.Colors.ON_SURFACE,
                    selected_icon_color=ft.Colors.PRIMARY,
                    on_click=lambda e: switch_tab(2),
                    selected=(selected_index == 2)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40,
            expand=True
        ),
        bottom=0,
        left=0,
        right=0,
        shadow=ft.BoxShadow(
            spread_radius=0.5,
            blur_radius=15,
            color=ft.Colors.SHADOW,
            offset=ft.Offset(0, -2))
    )
    full_width_controls.append(bottom_nav)
    def switch_tab(index):
        global selected_index
        selected_index = index
        main_tab.visible = (index == 0)
        table_tab.visible = (index == 1)
        settings_tab.visible = (index == 2)
        for i, btn in enumerate(bottom_nav.content.controls):
            btn.selected = (i == index)
        page.update()
    def handle_resize(e=None):
        page_padding = page.padding
        h_padding = 0
        if isinstance(page_padding, (int, float)):
            h_padding = page_padding * 2
        elif page_padding:
            h_padding = getattr(page_padding, 'left', 0) + getattr(page_padding, 'right', 0)
        effective_page_width = page.width - h_padding
        logger.debug(f"Page resized: W={page.width}, H={page.height}, Padding={h_padding}, EffectiveW={effective_page_width}")
        if effective_page_width <= 0:
            logger.warning("Effective page width is zero or negative, skipping resize.")
            return
        needs_update = False
        for control in full_width_controls:
            if getattr(control, 'visible', True) and control.width != effective_page_width:
                try:
                    control.width = effective_page_width
                    needs_update = True
                except Exception as resize_err:
                    logger.error(f"Error resizing control {control}: {resize_err}")
        if needs_update:
            logger.debug("Updating page due to control resize.")
            page.update()
    page.on_resized = handle_resize
    page.add(
        ft.Stack(
            [
                ft.Column(
                    [
                        main_tab,
                        table_tab,
                        settings_tab
                    ],
                    expand=True
                ),
                bottom_nav,
            ],
            expand=True
        )
    )
    theard_check_ip6_again()
    def generate_ipv4_range(start_ip, end_ip):
        start = list(map(int, start_ip.split('.')))
        end = list(map(int, end_ip.split('.')))
        ip_range = []
        while start <= end:
            ip_range.append('.'.join(map(str, start)))
            if start == end:
                break
            start[3] += 1
            for i in (3, 2, 1):
                if start[i] > 255:
                    start[i] = 0
                    start[i-1] += 1
        return ip_range
    def generate_ipv6():
        return f"2606:4700:d{random.randint(0, 1)}::{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}"
    def ping_ip(ip, port, timeout, count, interval, ip_version):
        try:
            family = socket.AF_INET6 if ip_version == "ipv6" else socket.AF_INET
            result = ping(
                ip,
                count=count,
                interval=interval,
                timeout=timeout,
                family=family,
                privileged=False
            )
            if result.is_alive:
                ping_time = result.avg_rtt or 1000
                loss = result.packet_loss * 100
                jitter = result.jitter or 100
                score = (0.5 * ping_time) + (0.3 * loss) + (0.2 * jitter)
                return (ip, port, ping_time, loss, jitter, score)
        except Exception as e:
            print(f"Ping error for {ip}: {e}")
        return None
    async def process_results(page: ft.Page, results):
        try:
            if not results:
                raise ValueError("No results to process")
            state.sorted_results = sorted(results, key=lambda x: x[5])
            def update_table():
                print("Updating table...")
                rows = []
                for item in state.sorted_results[:10]:
                    if len(item) != 6:
                        raise ValueError(f"Unexpected result format: {item}")
                    ip, port, ping, loss, jitter, score = item
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{ip}:{port}")),
                                ft.DataCell(ft.Text(f"{ping:.2f}")),
                                ft.DataCell(ft.Text(f"{loss:.2f}%")),
                                ft.DataCell(ft.Text(f"{jitter:.2f}")),
                                ft.DataCell(ft.Text(f"{score:.2f}")),
                            ],
                            on_select_changed=lambda e, ip=item[0]: page.run_task(copy_ip, page, ip)
                        )
                    )
                tbl_results.rows = rows
                result_view.controls = [
                    ft.Text("Scan completed!", color=ft.Colors.GREEN),
                    ft.Text(f"Best IP: {state.sorted_results[0][0]}:{state.sorted_results[0][1]}", color=ft.Colors.LIGHT_GREEN)
                ]
                page.update()
            print("Calling update_table...")
            update_table()
        except Exception as e:
            print(f"Results processing error: {str(e)}")
            snake.content =ft.Text(f"Processing failed: {str(e)}", color=ft.Colors.RED)
            snake.open = True
            page.update()
    async def copy_ip(page: ft.Page, ip):
        try:
            page.set_clipboard(ip)
            snake.content= ft.Text("IP copied to clipboard!")
            snake.open = True
            page.update()
        except Exception as e:
            print(f"Copy error: {e}")
    def save_settings():
        nonlocal state
        try:
            settings = {
                "cpu_speed": dd_cpu_speed.value,
                "ping_range": int(tf_ping_range.value),
                "timeout": int(tf_timeout.value),
                "count": int(tf_count.value),
                "interval": int(tf_interval.value),
                "save_results": dd_save_results.value,
                "which_pannel":dd_which_pannl.value,
                "with_port": dd_with_port.value
            }
            with open(set_path, "w") as f:
                json.dump(settings, f, indent=4)
            snake.content=ft.Text(f"Settings saved successfully!", color=ft.Colors.GREEN)
            snake.open=True
            state.cpu_speed = settings["cpu_speed"]
            state.ping_range = str(settings["ping_range"])
            state.timeout = str(settings["timeout"])
            state.count = str(settings["count"])
            state.interval = str(settings["interval"])
            state.save_results = settings["save_results"]
            state.which_pannel = settings["which_pannel"]
            state.with_port = settings["with_port"]
            page.update()
        except Exception as e:
            print(f"Save error: {e}")
            snake.content=ft.Text(f"Save failed: {str(e)}", color=ft.Colors.RED)
            snake.open=True
            page.update()
    if not os.path.exists(set_path):
        save_settings()
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/storage/emulated/0/Download/wwarpscanner/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
ft.app(target=main, assets_dir="assets")
