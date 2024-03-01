import socket
import concurrent.futures
from ping3 import ping, verbose_ping

def ping_host(ip):
    print(f"Pinging {ip}...")
    try:
        result = ping(ip)
        if result != None and result != False:
            return True
        return False
    except Exception as e:
        return False


def map_network(subnet):
    hosts_up = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        if ping_host(ip):
            hosts_up.append(ip)
    return hosts_up


def scan_port(port,host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return port
    except Exception as e:
        pass
    finally:
        sock.close()

def get_service_name(port, protocol='tcp'):
    try:
        name = socket.getservbyport(port, protocol)
        return name
    except Exception as e:
        return None

def main():
    print("Bem vindo ao portscanner!")
    print("Este programa irá escanear as portas de um host e mostrar quais estão abertas.")
    qual = input("Deseja escanear um host ou uma rede? (1 para host, 2 para rede): ")
    if qual == "1":
        host = input("Digite o host para escanear (ex: google.com ou 142.250.189.206): ")
        hosts_up = [host]
        comeco = int(input("Digite a porta inicial para escanear (ex: 10): " ))
        final = int(input("Digite a porta final para escanear (ex: 1000): "))
        quantas = (input("Quantas threads deseja usar?  \n(default:50 -- cuidado, muitas threads pode resultar em resultados imprecisos): "))
    else:
        subnet = input("Digite a rede para escanear (ex: 192.168.0): ")
        comeco = int(input("Digite a porta inicial para escanear (ex: 10): " ))
        final = int(input("Digite a porta final para escanear (ex: 1000): "))
        quantas = (input("Quantas threads deseja usar?  \n(default:50 -- cuidado, muitas threads pode resultar em resultados imprecisos): "))
        hosts_up = map_network(subnet)
        
  
    if quantas.isdigit() == False:	
        quantas = 50
    else:
        quantas = int(quantas)

    portas = range(comeco, final+1)
    print("Hosts up in the network:")

    for host in hosts_up:
        print(host)
        portas_abertas = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=quantas) as executor:
            futures = {executor.submit(scan_port, port, host): port for port in portas}
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                if future.result():
                    portas_abertas.append(port)
        
        for porta in portas_abertas:
            service = get_service_name(porta)
            if service is not None:
                print(f"A porta {porta} está aberta. Serviço: {service}")
            else:
                print(f"A porta {porta} está aberta.")

if __name__ == "__main__":
    main()
