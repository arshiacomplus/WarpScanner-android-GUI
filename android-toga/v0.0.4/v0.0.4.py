
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, CENTER
import queue
import random
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from icmplib import ping as pinging
import time

from retrying import retry
import urllib.request
import urllib.parse
from urllib.parse import quote
import logging

# تعیین مسیر فایل لاگ
log_path = "sdcard/Download/wwarpscanner/app.log"

if os.path.exists(log_path):
    os.remove(log_path)
with open(log_path, "w") as ff:
    ff.close()

# پیکربندی لاگینگ
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

wire_config_temp=''
wire_c=0
wire_p=0

send_msg_wait=0
results = []
sorted_results=[]
save_result=[]
save_result1=[]
best_result=[]
temp_conf=[]
WoW_v2=''
Wow=''
isIran=''
check="none"
max_workers_number=0



WH_ipVersion=""
best_ip = 0

best_result_avg=""
i_ip_scan=False
is_sub=False
is_v2ray=False
ty=False


check=""
ipv6=""
ipv4=""
Cpu_speed=""
do_you_save=""
wich_pannel=""
port_go=""
ping_range_see=""
timeout_see=""
count_see=""

file_path ="sdcard/Download/wwarpscanner/warp_setting"
try:
    with open(file_path , "r") as f:
                num=f.readlines()
                Cpu_speed=num[0]
                do_you_save=num[1]

                wich_pannel=num[2]
                port_go=num[3]
                ping_range_see=int(num[4])
                timeout_see=int(num[5])
                count_see=int(num[6])
                interval_see=int(num[7])
except Exception:
    if not os.path.exists(file_path):
            if not os.path.exists('sdcard/Download/wwarpscanner'):
                os.makedirs('sdcard/Download/wwarpscanner')
           
            with open("sdcard/Download/wwarpscanner/warp_setting", "w") as f:
                f.write("faster\n")
                f.write("no\n")
                f.write("bpb\n")
                f.write('no\n')
                f.write('500\n')
                f.write("5\n")
                f.write("2\n")
                f.write("1\n")


q = queue.Queue()

class MyApp(toga.App):



    def startup(self):
      
        global Cpu_speed
        global do_you_save, ping_range_see , timeout_see , count_see , interval_see,wich_pannel,port_go
        

        selff=self
        file_path ="sdcard/Download/wwarpscanner/warp_setting"
 
        
        
            
        
        

        with open(file_path , "r") as f:
            num=f.readlines()
       
            if len(num)!=8:
                os.remove("sdcard/Download/wwarpscanner/warp_setting")
                with open("sdcard/Download/wwarpscanner/warp_setting", "w") as f:
                    f.write("faster\n")
                    f.write("no\n")
                    f.write("bpb\n")
                    f.write('no\n')
                    f.write('500\n')
                    f.write("5\n")
                    f.write("2\n")
                    f.write("1\n")

        Cpu_speed=num[0]
        do_you_save=num[1]
        
        wich_pannel=num[2]
        port_go=num[3]
        ping_range_see=int(num[4])
        timeout_see=int(num[5])
        count_see=int(num[6])
        interval_see=int(num[7])

        warp1111=list(num)
        warp111=list(num)
        def update_ui():
                while True:
                    task = q.get()
                    if task is None:
                        break
                    task()
                self.main_window.content.refresh()
           
        def run_on_ui_thread(task):
            go=threading.main_thread()
            go.run(task)

        def clean2(elr):
            with open("sdcard/Download/wwarpscanner/result.txt", 'r') as f:
                    b=f.readlines()
                    with open('sdcard/Download/wwarpscanner/clean_result.txt', 'w') as ff:
                        for j in b:
                                try:
                                    if wich_pannel =='bpb\n':
                                        ff.write(j[:j.index('|')-1])
                                        if j != b[len(b)-1]:
                                            ff.write(',')
                                    else:
                                        ff.write(j[:j.index('|')-1])
                                        ff.write('\n')
                                except Exception:
                                    pass

            
            
            label_best.value="saved in sdcard/Download/clean_result.txt !'"         
            
         
    
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

        def check_ip6_again():
                global check
      
                print("go")
                
                
                label_ipv4.text = "ipv4 : Checking ... "
                label_ipv6.text = "ipv6 : Checking  ...."


                check="none"
            
        
                check=  selff.check_ipv6()
                if  check[0] == "Available":
                
                    color1="green"
                else:
    
                    color1="red"
                
                if  check[1] == "Available":
        
                    color2="green"
                else:
    
                    color2="red"
    

                label_ipv4.text=f"ipv4 : {check[0]}"
                label_ipv4.style.update(color=color1)
                label_ipv6.text=f"ipv6 : {check[1]}"
                label_ipv6.style.update(color=color2)

        def theard_check_ip6_again(self):

            


            thread3=threading.Thread(target=check_ip6_again)
            thread3.start()
            
        def change(rer):
    
            
            global Cpu_speed,do_you_save,wich_pannel,port_go,ping_range_see,timeout_see,count_see,interval_see
            file_path ="sdcard/Download/wwarpscanner/warp_setting"
   
            with open(file_path , "r") as f:
                saved=f.readlines()
            saved[0]=f_s.value.strip()+"\n"
            saved[1]=save_reys.value.strip()+"\n"
            saved[2]=wich.value.strip()+"\n"
            saved[3]=with_port.value.strip()+"\n"
            saved[4]=ping_range.value.strip()+"\n"
            saved[5]=timeout.value.strip()+"\n"
            saved[6]=count.value.strip()+"\n"
            saved[7]=interval.value.strip()+"\n"


            with open(file_path , "w") as f :
                for k in saved:
                    f.write(k)
            Cpu_speed=saved[0]
        def on_select(widget):
            if widget.value =="IP scanning":
                try:
                    ip_box.remove(optionmenu)
                    ip_box.remove(how_menypp)
                    ip_box.remove(no_ip)
                    ip_box.remove(no_port)
                    ip_box.remove(wich_loc)
                    
                except Exception:
                    pass
            else:
                ip_box.remove(button_ipv4)
                ip_box.remove(button_ipv6)
                ip_box.remove(button_clean)
                ip_box.add(optionmenu)
                if is_sub==True:
                    ip_box.add(how_menypp)
                if i_ip_scan==True:
                    ip_box.add(no_ip)
                    ip_box.add(no_port)
                val=optionmenu.value
                if val=="WoW for v2ray or mahsaNG" or val == "WoW with noise for Nikang or MahsaNg":
                    ip_box.add(wich_loc)
 
                ip_box.add(button_ipv4)
                ip_box.add(button_ipv6)
                ip_box.add(button_clean)
        def issub(widget):
            global is_sub, i_ip_scan
            val=widget.value
            if val=="wireguard for Sing-box and Hiddify | old | with a sub link" or val=="WoW with noise for Nikang or MahsaNg in sub link" or val=="WoW for v2ray or mahsaNG in sub link" or val=="wireguard for Hiddify with a sub link":
                is_sub=True

                ip_box.remove(button_ipv4)
                ip_box.remove(button_ipv6)
                ip_box.remove(button_clean)
                ip_box.add(how_menypp)
                ip_box.add(button_ipv4)
                ip_box.add(button_ipv6)
                ip_box.add(button_clean)
            else:
                if is_sub==True:
                    ip_box.remove(how_menypp)
                    is_sub=False

            if val=="wireguard for Hiddify without ip scanning" or val=="wireguard for Sing-box and Hiddify| old | without ip scanning" or val=="wireguard for v2ray and mahsaNG without ip scanning" or val=="wireguard for nikaNg without ip scanning":
                i_ip_scan=True
                ip_box.remove(button_ipv4)
                ip_box.remove(button_ipv6)
                ip_box.remove(button_clean)
                ip_box.add(no_ip)
                ip_box.add(no_port)
                ip_box.add(button_ipv4)
                ip_box.add(button_ipv6)
                ip_box.add(button_clean)
            else:
                i_ip_scan=False
                ip_box.remove(no_ip)
                ip_box.remove(no_port)
            if val=="WoW for v2ray or mahsaNG" or val == "WoW with noise for Nikang or MahsaNg":
                ip_box.remove(button_ipv4)
                ip_box.remove(button_ipv6)
                ip_box.remove(button_clean)
                ip_box.add(wich_loc)
                ip_box.add(button_ipv4)
                ip_box.add(button_ipv6)
                ip_box.add(button_clean)
            else:
                ip_box.remove(wich_loc)

            
                
            
        def main_v4():
            global save_result,  max_workers_number , WH_ipVersion

            if Cpu_speed=="faster\n":
                max_workers_number=100
            elif Cpu_speed=="slower\n":
                max_workers_number=50
            print(max_workers_number)       
 
            
            sorted_results=[]



            

                        

            def main_menu():
                global WH_ipVersion
                global save_result
                global sorted_results
                global best_result
                global WoW_v2
                global max_workers_number
                global q
                

                print("whuy")


                
                
                if Cpu_speed == "1": max_workers_number=100
                elif Cpu_speed == "2": max_workers_number=50
                




                def bind_keys():
                    @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda x: isinstance(x, ConnectionError))
                    def file_o():
                            try:
                                response = requests.get("", timeout=30)
                                return response.text
                            except Exception:
                                response = requests.get("", timeout=30)
                                return response.text
                  
                    b=file_o()
                    b=b.split("\n")
                    address=b[0][b[0].index(":")+2:]
                    priv_string=b[1][b[1].index(":")+2:]
                    reserved=b[2][b[2].index(":")+2:].split(" ")

                    reserved.pop(3)
                    reserved = [int(item) for item in reserved]
                    pub_key=b[3][b[3].index(":")+2:]
                    print(address,priv_string,reserved,pub_key)
                    
                    
                    return [address,priv_string,reserved, pub_key]
                
                def get_wireguard_for_hiddify(best_ip):
                    global best_result,wire_config_temp,wire_p
                    ip, port, ping, loss_rate,jitter, combined_score=best_ip
                    best_result=2*[1]
                    if WH_ipVersion=="ipv6":
                        ip="["+ip+"]"
                    best_result[0]=ip
                    best_result[1]=port
                    all_key=bind_keys()

                    all_key2=bind_keys()
                    print(optionmenu.value)
                    hising=f'''
                    

                        {{
                        "type": "wireguard",
                        "tag": "Tel=@arshiacomplus Warp-IR1",
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
                 
                    if  optionmenu.value=="wireguard for Hiddify without ip scanning" or optionmenu.value=="wireguard for Hiddify" or optionmenu.value=="wireguard for Hiddify with a sub link":
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
                        "tag": "Tel=@arshiacomplus Warp-Main1",
                        "detour": "Tel=@arshiacomplus Warp-IR1",
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
                    if  optionmenu.value=="wireguard for Hiddify without ip scanning" or optionmenu.value=="wireguard for Hiddify" or optionmenu.value=="wireguard for Hiddify with a sub link":
                        hising+=    f''',
                        "fake_packets_mode":"m4"'''
                    hising+=f'''
                        }}
                    
            
                    '''
                    
                    if optionmenu.value=="wireguard for Hiddify" or optionmenu.value=="wireguard for Hiddify without ip scanning" or optionmenu.value=="wireguard for Sing-box and Hiddify| old | without ip scanning":
                   
                        
            
                        q.put(lambda: setattr(label_best, 'value', hising))              
                        update_ui()
                        return
                    elif optionmenu.value=="wireguard for Hiddify with a sub link" or optionmenu.value=="wireguard for Sing-box and Hiddify | old | with a sub link" :
                        if wire_p==0:
                            wire_config_temp+=hising
                            
                        else:
                            wire_config_temp+=",\n"+hising

                    
                    wire_p+=1
                    if str(wire_p)==how_menypp.value:
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
                    
             
                        
                        
                        q.put(lambda: setattr(label_best, 'value', lin))              
                        update_ui()
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
                    if optionmenu.value=="wireguard for nikaNg" or optionmenu.value=="wireguard for nikaNg without ip scanning":
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
                    if optionmenu.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
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
                    if optionmenu.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
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
                    if optionmenu.value=="WoW with noise for Nikang or MahsaNg in sub link":WoW_v2+=''',
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
                    if n !=int(how_menypp.value)-1:
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
                    if wich_loc.value=="Iran":
                        isIran="1"
                    elif wich_loc.value=="German":
                        isIran="2"
                    Wow=""


           
        
             
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
                            if optionmenu.value=="WoW with noise for Nikang or MahsaNg":Wow+=''',
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
                            if optionmenu.value=="WoW with noise for Nikang or MahsaNg":Wow+=''',
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
               
                        Wow+='''
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
            "stats": {}
            }}'''

                
                    return Wow

                def copy_ip(text):
                    global  sorted_results

        
                    
                    
                    # sel_it=table.selection()
                    # print(sel_it)
                    # sel_it=sel_it[0]
                    # column=table.identify_column(event.x)
                    # value=table.set(sel_it,column)
                    print(text)
                    text=str(text)
                    text=list(text)
                    y=text.index("y")
                    
                    vv=text.index(">")

                    nnn=text[y+2:vv]
                    nn2=""
                    for i in nnn:
                        nn2+=i
                    nnn=int(nn2)//20
                
                    print(nnn)
                    sorted_results2=sorted_results[nnn-1]
                    ip, port, ping, loss_rate,jitter , combined_score=sorted_results2

                    # tabview.tab("main").clipboard_clear()
                    # if WH_ipVersion=="ipv4":
                    #     tabview.tab("main").clipboard_append(ip+":"+str(port))
                    # else:
                    #     tabview.tab("main").clipboard_append("["+ip+"]"+":"+str(port))
                    
                def generate_ipv6():
                        return f"2606:4700:d{random.randint(0, 1)}::{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}:{random.randint(0, 65535):x}"

                def ping_ip(ip, port):
                        global results
                        global best_ip
                        global best_result_avg

                        
                        
                        
                        icmp=pinging(ip, count=count_see ,interval=interval_see,timeout=timeout_see,family="ipv6" ,privileged=False)
                        ping=float(icmp.avg_rtt)
                        jitter=icmp.jitter
                        loss_rate=icmp.packet_loss
                        if ping == 0.0:
                            ping=1000
                        if jitter== 0.0:
                            jitter=100
                        if loss_rate==1.0:
                            loss_rate=100
                        loss_rate=loss_rate*100
                        if (0.5 *ping + +0.2 * jitter+ 0.3* loss_rate  ) > best_ip:
                            best_ip=(0.5 * float(icmp.avg_rtt) +0.2 *icmp.jitter + 0.3* icmp.packet_loss )
                            best_result_avg=ip
                        if icmp.is_alive:
                    
                            results.append((ip, port, ping,loss_rate ,jitter ))
                        
                        


                def check_ac_v6(mn):
                    global best_result
                    global save_result
                    global do_you_save
                    global sorted_results
                    global save_result
                    
                
                    best_result=mn
                    for ip, port, ping, loss_rate,jitter , combined_score in sorted_results[:10]:

                        q.put(lambda ip=ip, port=port, ping=ping, loss_rate=loss_rate, jitter=jitter, combined_score=combined_score:table.data.append({"ip": ip, "ping": ping, "lost": loss_rate, "jitter": jitter, "score": combined_score}))
                        
                        # table.bind("<Button-1>", lambda event , ip=ip:copy_ip(event))
                
                    best_result = sorted_results[0] if sorted_results else None
                    
                    ip, port, ping, loss_rate,jitter, combined_score = best_result
                   
         
                    
                    
                    q.put(lambda: setattr(label_best, 'value', f"The best IP: [{ip}]:{port if port else 'N/A'} , ping: {ping:.2f} ms, packet loss: {loss_rate:.2f}% ,{jitter} ms , score: {combined_score:.2f}" ))              
                   
                    best_result=2*[1]
                    best_result[0]=f"{ip}"
                    best_result[1]=878
                  
                  
                    
                    q.put(lambda: setattr(labelmain1, 'text', "Finished"))              
                    update_ui()
                    

                    # do_you_save=""
    
                    # print(do_you_save)
                    # print(best_result)
                    # os.remove("result.txt")
                    # filef=open("result.txt" , "w")
                    # t=0

                    # if do_you_save =="1\n":
                    #     for i in save_result:
                    #         if t==0:
                
                    #             filef.write(i[1:])
                    #             t=1
                    #         else:
                                
                    #             filef.write(i)

                    # filef.close()
                def check_ac():
        
                    global save_result
                    global best_result
                    global sorted_results
                    global do_you_save
     
                    
            
                    
                # "IP", "Ping", "lost", "jitter", "score"
                    for ip, port, ping, loss_rate,jitter, combined_score in sorted_results[:10]:

                        q.put(lambda ip=ip, port=port, ping=ping, loss_rate=loss_rate, jitter=jitter, combined_score=combined_score:table.data.append({"ip": ip, "ping": ping, "lost": loss_rate, "jitter": jitter, "score": combined_score}))
                        
                        # table.bind("<Button-1>", lambda event , ip=ip:copy_ip(event))
                    
                    try:
                        best_result = sorted_results[0]
                    except Exception:
                        best_result="1","1","1","1","1","1"
                    ip, port, ping, loss_rate,jitter, combined_score = best_result
                    
                    
                                 
                 

      
                    
                    try:
                          
                            q.put(lambda: setattr(label_best, 'value', f"The best IP: {ip}:{port if port else 'N/A'} , ping: {ping:.2f} ms, packet loss: {loss_rate:.2f}%,  jitter {jitter} ms , score: {combined_score:.2f}")) 
                    except TypeError:
                            q.put(lambda: setattr(label_best, 'value',f"The best IP: {ip}:{port if port else '878'} , ping: None, packet loss: {loss_rate:.2f}%, jitter: {jitter} ms , score: {combined_score:.2f}")) 
                    update_ui()
                           
                    
                    best_result=2*[1]
                    best_result[0]=f"{ip}"
                    best_result[1]=878
                    # do_you_save="2"


                    # fileff=open("result.txt" , "w")
                    
                    # t=0

                    # if do_you_save =="1\n":
                    #     for i in save_result:
                    #         if t==0:
                
                    #             fileff.write(i[1:])
                    #             t=1
                    #         else:
                                
                    #             fileff.write(i)

                    # fileff.close()
                            
                    return best_result
                def create_ip_range(start_ip, end_ip):
                    start = list(map(int, start_ip.split('.')))
                    end = list(map(int, end_ip.split('.')))
                    temp = start[:]
                    ip_range = []

                    while temp != end:
                        ip_range.append('.'.join(map(str, temp)))
                        temp[3] += 1
                        for i2 in (3, 2, 1):
                            if temp[i2] == 256:
                                temp[i2] = 0
                                temp[i2-1] += 1
                    ip_range.append(end_ip)
                    return ip_range
                

                def scan_ip_port(ip, port):
                    global best_result
                    global sorted_results
                    global results
                    global save_result
                    global do_you_save
                    
                    icmp=pinging(ip, count=count_see ,interval=interval_see,timeout=timeout_see,family="ipv4" ,privileged=False)
                    # if icmp.avg_rtt != 0 and icmp.packet_loss!=1 and icmp.jitter!=0:
                    #         print(icmp)
                    #         progress2["value"] += 1
                    if icmp.is_alive:
                            
                

                        results.append((ip, port, float(icmp.avg_rtt) ,float(icmp.packet_loss),float(icmp.jitter)))
                
                # labelmain1.text ="Please wait scannig ip ..."
                if i_ip_scan==True:
                    print("no ip")
                    
                    ip=no_ip.value
                    port=no_port.value
                    if optionmenu.value=="wireguard for Hiddify without ip scanning" or optionmenu.value=="wireguard for Sing-box and Hiddify| old | without ip scanning":
                        
                       
                        get_wireguard_for_hiddify((ip,int(port),0,0,0,0))
                       

                    elif optionmenu.value=="wireguard for v2ray and mahsaNG without ip scanning" or optionmenu.value=="wireguard for nikaNg without ip scanning":
                                print("w_no")
                                ip=no_ip.value
                                port=no_port.value
                                def go():
                                    bi=bind_keys()
                                    bi={
        'PrivateKey': bi[1],
        'PublicKey': bi[3],
        'Reserved': bi[2],
        'Address': bi[0]
    }

                                    wrg=generate_wireguard_url(bi,str(ip)+":"+str(port))
                                    
                                 
                                    q.put(lambda: setattr(label_best, 'value', wrg))              
                                    update_ui()
                                go()

                        
                      
                save_result=[]
                
                if WH_ipVersion=="ipv6":
                    

                    print("ipv6")
           
                    save_result=[]
                    sorted_results=[]


                    ports_to_check = [1074 , 864]
                    

                    random_ip=generate_ipv6()
                    

                    executor= ThreadPoolExecutor(max_workers=max_workers_number)
                    try:
                        for _  in range(101):
                            executor.submit(ping_ip, generate_ipv6(), ports_to_check[random.randint(0,1)])
                    except Exception:
                        print("AN Error")
                    finally:
                        executor.shutdown(wait=True)
                   

                    extended_results=[]

                    for result in results:
                        ip, port, ping , loss_rate, jitter= result

                        combined_score = (0.5 * ping +0.2 *jitter + 0.3* loss_rate)
                        extended_results.append((ip, port, ping, loss_rate,jitter, combined_score))

                    sorted_results=sorted(extended_results, key=lambda x: x[5])
                    if wich_pannel!="with score\n": 
                        for ip, port, ping, loss_rate,jitter, combined_score in sorted_results:
                        
                                if loss_rate == 0.00 and ping != 0.0 and ping < ping_range_see:

                                    if port_go=="no\n":
                                        
            
                                            if wich_pannel=="bpb\n":
                                                save_result.append(",")
                                                save_result.append(str(ip))
                                            else:
                                                save_result.append("\n")
                                                save_result.append(str(ip))
                                    else:
                           
 
                                            if wich_pannel=="bpb\n":
                                                save_result.append(",")
                                                save_result.append(str(ip)+":"+str(port))
                                            else:
                                                save_result.append("\n")
                                                save_result.append(str(ip)+":"+str(port))
                    if wich_pannel=="with score\n": 

                        for ip, port, ping, loss_rate,jitter, combined_score in sorted_results:
                            if ping <=ping_range_see:
                                if port_go=="no\n":
                                            save_result.append("\n")
                                            save_result.append(ip+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter)) 
                                else:
                                            save_result.append("\n")
                                            save_result.append(ip+":"+str(port)+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter)) 

                    best_result=sorted_results[0]
                    
                    


                    port_random = ports_to_check[random.randint(0, len(ports_to_check) - 1)]
                    if best_ip:

                        best_ip_mix = [1] * 2
                        best_ip_mix[0] = "[" + best_result_avg + "]"
                        best_ip_mix[1] = port_random
                    else:

                        best_ip_mix = [1] * 2
                        best_ip_mix[0] = "[" + random_ip + "]"
                        best_ip_mix[1] = port_random
                    print(best_ip_mix)
                    if radio_var.value=="Get config":
                            print("yes")
                 
                            if optionmenu.value=="wireguard for Hiddify with a sub link"  or optionmenu.value=="wireguard for Sing-box and Hiddify | old | with a sub link":
                                print("issub")
                                
                                for i in range(int(how_menypp.value)):
                                        get_wireguard_for_hiddify(sorted_results[0])
                              
                           
                                return
                            elif optionmenu.value=="wireguard for Hiddify" or optionmenu.value=="wireguard for Sing-box and Hhidify | old |" :
                                print("i went")
                     
                                get_wireguard_for_hiddify(sorted_results[0])
                               
                                return
                            elif optionmenu.value=="wireguard for v2ray and mahsaNG" or optionmenu.value=="wireguard for nikaNg":
                                def go():
                                    bi=bind_keys()
                                    bi={
        'PrivateKey': bi[1],
        'PublicKey': bi[3],
        'Reserved': bi[2],
        'Address': bi[0]
    }

                                    ip, port, ping, loss_rate,jitter, combined_score=sorted_results[0]
                                    wrg2=generate_wireguard_url(bi,"["+str(ip)+"]"+":"+str(port))
                                    
                                   

                                    q.put(lambda: setattr(label_best, 'value', wrg2))              
                                    update_ui()
                                go()
                                
                                return
                            elif optionmenu.value=="WoW with noise for Nikang or MahsaNg" or optionmenu.value=="WoW for v2ray or mahsaNG":
                                ip, port, ping, loss_rate,jitter, combined_score=sorted_results[0]              
                     
                                wowp=wow_nonoise("["+ip+"]",port)
                                
                                 
                                q.put(lambda: setattr(label_best, 'value', wowp))              
                                update_ui()
                           
                                return
                            elif optionmenu.value=="WoW with noise for Nikang or MahsaNg in sub link" or optionmenu.value=="WoW for v2ray or mahsaNG in sub link":
                                ip, port, ping, loss_rate,jitter, combined_score=sorted_results[0]
                                  
                     
                                   
                                for ii in range(int(how_menypp.value)):
                                        b=wow_nonoise_sub(ii,"["+ip+"]",port)
                              
                           
                                WoW_v2=upload_to_bashupload(WoW_v2)
                              
                                 
                                q.put(lambda: setattr(label_best, 'value', WoW_v2))              
                                update_ui()
                                WoW_v2=""
                                
                                    
                       
                                

                                return
                    if do_you_save =="yes\n":
              
                        with open("sdcard/Download/wwarpscanner/result.txt" ,"w") as f:
                            for i in save_result:
                                f.write(i)                                                                     
                    check_ac_v6(best_ip_mix)
                    save_result=[]
                    
                    return
                else:
                    print("ipv4")
                    

                    sorted_results=[]



       
             
                    save_result=[]
                    
                    
                    
                    start_ips = ["188.114.96.0", "162.159.192.0", "162.159.195.0"]
                    end_ips = ["188.114.99.224", "162.159.193.224", "162.159.195.224"]
             
                    ports = [1074, 894, 908, 878]
                    
        
                    # except Exception:
                    #      executor_bar.shutdown(wait=True)
               
                            

                    for start_ip, end_ip in zip(start_ips, end_ips):
                        ip_range = create_ip_range(start_ip, end_ip)
                        
                        executor= ThreadPoolExecutor(max_workers=int(max_workers_number))
                        try:
                            for ip in ip_range:

                                futures=executor.submit(scan_ip_port, ip, ports[random.randint(0,3)])
                            
                                
                        
            
                        except Exception as e:
                            print("AN Error", e)
                        finally:
                            executor.shutdown(wait=True)


                    
           

                        
                    
                    
                    
                    extended_results = []

                    for result in results:
                        ip, port, ping , loss_rate, jitter= result
                        
                        if ping==0.0 :
                            ping=1000
                        
                        if  jitter==0.0:
                            
                            jitter=1000
                        if loss_rate == 1.0:
                            loss_rate=100
                        loss_rate=loss_rate*100
                        
                        
                                    


                        combined_score = (0.5 * ping +0.2 *jitter + 0.3* loss_rate)
                        extended_results.append((ip, port, ping, loss_rate,jitter, combined_score))
                                

                    sorted_results = sorted(extended_results, key=lambda x: x[5])

                    
                   
                    if wich_pannel!="with score\n": 
                            for ip, port, ping, loss_rate,jitter, combined_score in sorted_results:
                                if loss_rate == 0.00 and ping != 0.0 and ping < ping_range_see:
                                    if port_go=="no\n":
                                        
                                        
                                   
          
                                            if wich_pannel=="bpb\n":
                                                save_result.append(",")
                                                save_result.append(str(ip))
                                            else:
                                                save_result.append("\n")
                                                save_result.append(str(ip))
                                    else:
                             

                                        if wich_pannel=="bpb\n":
                                            save_result.append(",")
                                            save_result.append(str(ip)+":"+str(port))
                                        else:
                                            save_result.append("\n")
                                            save_result.append(str(ip)+":"+str(port))
                    if wich_pannel=="with score\n": 

                        for ip, port, ping, loss_rate,jitter, combined_score in sorted_results:
                            if ping <=ping_range_see:
                                            

                                if port_go=="no\n":
                                            save_result.append("\n")
                                            save_result.append(ip+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter)) 
                                else:
                                            save_result.append("\n")
                                            save_result.append(ip+":"+str(port)+" | "+"ping: "+ str(   ping) +"packet_loss: "+ str( loss_rate)+"jitter: "+str(   jitter))             
                    print("igo")
                    if radio_var.value=="Get config":
                 
                            if optionmenu.value=="wireguard for Hiddify with a sub link"  or optionmenu.value=="wireguard for Sing-box and Hiddify | old | with a sub link":
                                print("issub")
                                
                                for i in range(int(how_menypp.value)):
                                        get_wireguard_for_hiddify(sorted_results[0])
                               
                                
                           
                                return
                            elif optionmenu.value=="wireguard for Hiddify" or optionmenu.value=="wireguard for Sing-box and Hhidify | old |":
                                print("i went")
                     
                             
                                get_wireguard_for_hiddify(sorted_results[0])
                                
                                
                                return
                            elif optionmenu.value=="wireguard for v2ray and mahsaNG" or optionmenu.value=="wireguard for nikaNg":
                                def go():
                                    bi=bind_keys()
                                    bi={
        'PrivateKey': bi[1],
        'PublicKey': bi[3],
        'Reserved': bi[2],
        'Address': bi[0]
    }

                                    
                                    rgg=generate_wireguard_url(bi,str(ip)+":"+str(port))
                                    
                                 
                                    q.put(lambda: setattr(label_best, 'value', rgg))              
                                    update_ui()
                                
                                go()
                                return
                            elif optionmenu.value=="WoW with noise for Nikang or MahsaNg" or optionmenu.value=="WoW for v2ray or mahsaNG":
                                ip, port, ping, loss_rate,jitter, combined_score=sorted_results[0]              
                                tet=wow_nonoise(ip,port)
                                
                                                                 
                                q.put(lambda: setattr(label_best, 'value', tet))              
                                update_ui()
                                
                                return
                            elif optionmenu.value=="WoW with noise for Nikang or MahsaNg in sub link" or optionmenu.value=="WoW for v2ray or mahsaNG in sub link":
                                ip, port, ping, loss_rate,jitter, combined_score=sorted_results[0]
                                print("jhj")              
                     
                                   
                                for ii in range(int(how_menypp.value)):
                                        b=wow_nonoise_sub(ii,ip,port)
                              
                           
                                WoW_v2=upload_to_bashupload(WoW_v2)
                                                                 
                                q.put(lambda: setattr(label_best, 'value', WoW_v2))              
                                update_ui()
                  
                                WoW_v2=""
                          
                                
                                    
                       
                                

                                return
                    
                    print("create file and")
                    if do_you_save =="yes\n":
     
                    
                        with open("sdcard/Download/wwarpscanner/result.txt" ,"w") as f:
                            for i in save_result:
                                f.write(i)
                    # else:
                    #     print("create file win ")
                    #     with open("C:/Users/intel/Desktop/result.txt", "w") as f:
                    #         for i in save_result:
                    #             f.write(i)
                            
                    try:
                        check_ac()
                    except Exception as E:
                        print(E)
                        exit()
                    save_result=[]
                   

                  
         
                    return
            print("v4")
            
        

            main_menu()
            self.main_window.content.refresh()



        def main_move(self):
            global WH_ipVersion
            WH_ipVersion="ipv4"
            label_best.value = ""
            labelmain1.text= "please wait scanning ip ..."
            label_best.value="best result: "
           
            
                
            
            print("iiiiiiiiiiiiiiii")
            theard=threading.Thread(target=main_v4)
            theard.start()
            
        
        def main_move_v6(self):
            global WH_ipVersion
            WH_ipVersion="ipv6"
            label_best.value = ""
            labelmain1.text= "please wait scanning ip ..."
            label_best.value="best result: "
            print("iiiiiiiiiiiiiiii")
            theard2=threading.Thread(target=main_v4)
            theard2.start()
        
     

        
        main_box = toga.Box(style=Pack(flex=1,direction=ROW))
        ip_box= toga.Box(style=Pack( direction=COLUMN,flex=1,padding=(10)))
        
        table_box= toga.Box(style=Pack(direction=COLUMN,padding=(10),flex=1))

        set_box= toga.Box(style=Pack( direction=COLUMN,flex=1,padding=(10)))
        scrollable_box = toga.ScrollContainer(content=set_box,style=Pack(flex=1, direction=COLUMN), horizontal=False, vertical=True)
        scrollable_box2 = toga.ScrollContainer(content=table_box,style=Pack(flex=1, direction=COLUMN), horizontal=False, vertical=True)
        scrollable_box3 = toga.ScrollContainer(content=ip_box,style=Pack(flex=1, direction=COLUMN), horizontal=False, vertical=True)

        self.main_window = toga.MainWindow(title=self.formal_name)
        width=self.main_window.screen.size.width
  
        
        container = toga.OptionContainer(style=Pack(flex=1),
            content=[
            toga.OptionItem("main ", scrollable_box3),
            toga.OptionItem("table", scrollable_box2),
            toga.OptionItem("setting", scrollable_box )
            ]
        )
        main_box.add(container)
   
        label_ipv4 = toga.Label('ipv4 : none', style=Pack(padding=(0, 5)))
        ip_box.add(label_ipv4)

        label_ipv6 = toga.Label('ipv6 : none', style=Pack(padding=(0, 5)))
        ip_box.add(label_ipv6)

        ch_ag = toga.Button('Check', style=Pack(padding=(0, 580, 0 , 0)
                                                , width=100, color='green'
                                                )) # top, right, bottom, left
        ch_ag.on_press = theard_check_ip6_again
        ip_box.add(ch_ag)

        labelmain1 = toga.Label('Click to scan ip', style=Pack(padding=(25, 0,5,0)))
        ip_box.add(labelmain1)

        label_best = toga.TextInput(style=Pack(padding=(10, 20, 10, 20)),placeholder="result:")

        ip_box.add(label_best)

        how_menypp = toga.TextInput(placeholder='how many? (2~4)', style=Pack(padding=(0, 5)))

        no_ip = toga.TextInput(placeholder='ipv4 or ipv6', style=Pack(padding=(3,0,0, 5)))
        
        no_port = toga.TextInput(placeholder='port', style=Pack(padding=(3,0,0, 5)))

        radio_var = toga.Selection(items=['IP scanning', 'Get config'], on_select=on_select, style=Pack(padding=(5, 5)))
        ip_box.add(radio_var)

        optionmenu = toga.Selection(on_select=issub,items=[
        "wireguard for Hiddify",
        "wireguard for Hiddify without ip scanning",
        "wireguard for Hiddify with a sub link",
        "wireguard for v2ray and mahsaNG",
        "wireguard for v2ray and mahsaNG without ip scanning",
        "WoW for v2ray or mahsaNG",
        "WoW for v2ray or mahsaNG in sub link",
        "wireguard for nikaNg",
        "wireguard for nikaNg without ip scanning",
        "WoW with noise for Nikang or MahsaNg",
        "WoW with noise for Nikang or MahsaNg in sub link",
        "wireguard for Sing-box and Hhidify | old |",
        "wireguard for Sing-box and Hiddify| old | without ip scanning",
        "wireguard for Sing-box and Hiddify | old | with a sub link",
        ], style=Pack(padding=(5, 5)))

        wich_loc = toga.Selection(items=['Iran', 'German'], style=Pack(padding=(2, 5)))



        button_ipv4 = toga.Button('ipV4', on_press=main_move, style=Pack(padding=(0, 5)))
        ip_box.add(button_ipv4)

        button_ipv6 = toga.Button('ipV6', on_press=main_move_v6, style=Pack(padding=(0, 5)))
        ip_box.add(button_ipv6)

        button_clean = toga.Button('clean', on_press=clean2, style=Pack(padding=(0, 5)))
        ip_box.add(button_clean)
        file_path ="sdcard/Download/wwarpscanner/warp_setting"
        with open(file_path , "r") as f:
            saved=f.readlines()
        power = toga.Label('Scanpower', style=Pack(padding=(25, 0,5,0)))
        set_box.add(power)

        f_s = toga.Selection(items=['slower', 'faster'], value=saved[0][:len(saved[0])-1], on_select=change, style=Pack(padding=(0, 5)))
        set_box.add(f_s)

        save_re = toga.Label('save result', style=Pack(padding=(25, 0,5,0)))
        set_box.add(save_re)

        save_reys = toga.Selection(items=['yes', 'no'], value=saved[1][:len(saved[1])-1], on_select=change, style=Pack(padding=(0, 5)))
        set_box.add(save_reys)

        wich_la = toga.Label('whcih pannel', style=Pack(padding=(25, 0,5,0)))
        set_box.add(wich_la)

        wich = toga.Selection(items=['bpb', 'vahid', "with score"], value=saved[2][:len(saved[2])-1], on_select=change, style=Pack(padding=(0, 5)))
        set_box.add(wich)

        with_port_la = toga.Label('with port', style=Pack(padding=(25, 0,5,0)))
        set_box.add(with_port_la)

        with_port = toga.Selection(items=['yes', 'no'], value=saved[3][:len(saved[3])-1], on_select=change, style=Pack(padding=(0, 5)))
        set_box.add(with_port)


        ping_range_la = toga.Label('ping_range', style=Pack(padding=(25, 0,5,0)))
        set_box.add(ping_range_la)

        ping_range = toga.TextInput(style=Pack(padding=(25, 0,5,0)),value=saved[4][:len(saved[4])-1],on_lose_focus=change,placeholder="from zero to what?: ")        
        set_box.add(ping_range)



        timeout_la = toga.Label('icmp_timeout', style=Pack(padding=(25, 0,5,0)))
        set_box.add(timeout_la)

        timeout = toga.TextInput(style=Pack(padding=(25, 0,5,0)),value=saved[5][:len(saved[5])-1],on_lose_focus=change,placeholder="1~5")        
        set_box.add(timeout)

        count_la = toga.Label('icmp_count', style=Pack(padding=(25, 0,5,0)))
        set_box.add(count_la)

        count = toga.TextInput(style=Pack(padding=(25, 0,5,0)),value=saved[6][:len(saved[6])-1],on_lose_focus=change,placeholder="1~5")        
        set_box.add(count)

        interval_la = toga.Label('icmp_interval', style=Pack(padding=(25, 0,5,0)))
        set_box.add(interval_la)

        interval = toga.TextInput(style=Pack(padding=(25, 0,5,0)),value=saved[7][:len(saved[7])-1],on_lose_focus=change,placeholder="1~5")        
        set_box.add(interval)


        table = toga.Table(style=Pack(flex=1),
    headings=["IP", "Ping", "lost", "jitter", "score"],
    data=[

    ]
)
        
        # table.data[0] =  {"name": "Arthur bvb", "age": 50}
    

        table_box.add(table)
        # scrollable_box.content=main_box
        
        self.main_window.content = main_box
        self.main_window.show()
    
    def check_ipv6(seslff):
        
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


    

   

def main():
    return MyApp("warpscanner" , "com.warpscanner.warpscanner")


if __name__ == '__main__':
    main().main_loop()

