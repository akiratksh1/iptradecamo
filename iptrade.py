import netifaces
import random
import os
import time

def listar_interfaces_disponiveis():
    interfaces = netifaces.interfaces()
    print("Interfaces disponíveis:")
    for interface in interfaces:
        try:
            nome_interface = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            print(f"- {interface}: {nome_interface}")
        except Exception:
            print(f"- {interface}: (nome não disponível)")

def listar_enderecos_ip(interface):
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        print(f"Endereços IP da interface {interface}:")
        for addr in addrs[netifaces.AF_INET]:
            print(f"- {addr['addr']}")
    else:
        print(f"A interface {interface} não possui endereços IPv4.")

def gerar_opcoes_ips(qtd_ips=5):
    opcoes_ips = []
    for _ in range(qtd_ips):
        ip = f"192.168.1.{random.randint(2, 254)}"
        opcoes_ips.append(ip)
    return opcoes_ips

def selecionar_ip(opcoes_ips):
    print("Escolha um dos seguintes IPs disponíveis:")
    for i, ip in enumerate(opcoes_ips, start=1):
        print(f"{i}. {ip}")
    
    escolha = int(input("Digite o número correspondente ao IP desejado: "))
    if escolha < 1 or escolha > len(opcoes_ips):
        raise ValueError("Escolha inválida. Digite um número válido.")
    
    return opcoes_ips[escolha - 1]

def configurar_endereco_ip(interface, novo_ip):
    try:
        
        if interface not in netifaces.interfaces():
            raise ValueError(f"A interface {interface} não é válida ou não está disponível.")

        
        netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'] = novo_ip
        print(f"Endereço IP configurado com sucesso para {novo_ip}")
        listar_enderecos_ip(interface)

        
        print("Tentando renovar o lease DHCP...")
        os.system("ipconfig /renew")

    except ValueError as e:
        print(f"Erro ao configurar o endereço IP: {e}")
    except Exception as e:
        print(f"Erro inesperado ao configurar o endereço IP: {e}")

if __name__ == "__main__":
    listar_interfaces_disponiveis()

    interfaces = netifaces.interfaces()

    
    for interface in interfaces:
        print(f"\nConfigurando novo endereço IP para a interface {interface}:")
        opcoes_ips = gerar_opcoes_ips()
        novo_ip_desejado = selecionar_ip(opcoes_ips)
        configurar_endereco_ip(interface, novo_ip_desejado)
