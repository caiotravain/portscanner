import socket
import concurrent.futures

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
    host = input("Digite o host para escanear (ex: google.com ou 142.250.189.206): ")
    comeco = int(input("Digite a porta inicial para escanear (ex: 10): " ))
    final = int(input("Digite a porta final para escanear (ex: 1000): "))
    quantas = (input("Quantas threads deseja usar?  \n(default:50 -- cuidado, muitas threads pode resultar em resultados imprecisos): "))
    if quantas.isdigit() == False:	
        quantas = 50
    else:
        quantas = int(quantas)
    portas = range(comeco, final+1)
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
