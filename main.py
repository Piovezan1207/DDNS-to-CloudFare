import requests 
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

#Parâmetros para a API
Name_dns = os.getenv("NAME_DNS")         #Nome do DNS cadastrado na cloudfare
X_Auth_Email = os.getenv("X_AUTH_EMAIL") #Email cloudfare   
X_Auth_Key = os.getenv("X_AUTH_KEY")     #CLoudfare Global API Token
Zone_ID = os.getenv("ZONE_ID")           #Cloudfare Zone ID Token
Account_ID = os.getenv("ACCOUNT_ID")     #Cloudfare Account ID TOken

#Configurações do DNS na cloudfare
Type = os.getenv("TYPE")        #Cloudfare DNS type 
ttl = os.getenv("TTL")          #Cloudfare DNS tll
proxied = os.getenv("PROXIED")  #Cloudfare Proxy

while True:
   
    CF = "" 
    #Verifica IP cadastrado atualmente 

    try: #Tenta efetuar a requisição para a API da cloudfare
        headers={"X-Auth-Email" : X_Auth_Email , "X-Auth-Key" : X_Auth_Key}
        CF = requests.get("https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(Zone_ID , Account_ID), headers=headers )
    
    except: #Caso tenha um erro, é considerado que está sem internet
        print("Sem conexão com a internet.")
        time.sleep(10)
        continue    

    CF_JSON = json.loads(CF.text) #Carrega JSON
    CF_IP = ""

    if "success" in CF_JSON: #Verifica se houve sucesso na requisição
        if not CF_JSON["success"]:
            print("Houve um erro na requisição da API, tentando novamente...")
            print(CF_JSON)
            continue

    if "result" in CF_JSON: #Busca o IP cadastrado na CF nos resultados da consulta
        if "content" in CF_JSON["result"]:
            CF_IP = CF_JSON["result"]["content"]
    else:
        print("Falta 'result' na resposta")
        continue

    try: #Tenta efetuar a requisição para obter o IP externo
        ip = requests.get('https://api.ipify.org').content.decode('utf8')

    except:#Caso tenha um erro, é considerado que está sem internet
        print("Sem conexão com a internet.")
        time.sleep(10)
        continue

    print("IP externo: {} / IP da cloudfare: {}".format(ip, CF_IP)) #Printa a informação dos dois IPs

    if ip == CF_IP: #Caso os dois sejam iguais, não é necessário nenhuma atualizaçaõ da CF
        print("Os dois IPs estão iguais")
        time.sleep(100) #Aguarda 100 segundos e verifica novamente
    else:
        print("Ip externo mudou, atualizando na cloudfare...")

        #Faz a requisição para a API da CF, para atualizar o IP ligado ao DNS de escolha

        headers={"X-Auth-Email" : X_Auth_Email , "X-Auth-Key" : X_Auth_Key, "Content-type" : "application/json"}
        data=json.dumps({"type" : Type , 
                        "name" : Name_dns,
                        "content" : ip,
                        "ttl" : ttl,
                        "proxied" : True if proxied == 1 else False})

        try:#Tenta efetuar a requisição
            CF_att = requests.put("https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(Zone_ID , Account_ID) , headers=headers, data=data)
            CF_att_JSON = json.loads(CF_att.text)
            print("IP Atualizado com sucesso!") if CF_att_JSON["success"] else print("Houve um erro na atualização de IP - JSON : {}".format(CF_att_JSON))

        except: 
            print("Sem conexão com a internet.")
            continue
            
