import ipaddress
import os
from colorama import init, Fore

# Inisialisasi colorama
init(autoreset=True)

def process_ip_prefix_file(input_file, output_base_filename, output_folder, batch_size=20000):
    try:
        with open(input_file, 'r') as infile:
            ip_prefixes = infile.readlines()
        
        file_index = 0
        total_ips = 0
        ip_list = []  # Menyimpan IP sementara
        
        # Membuat folder hasil jika belum ada
        os.makedirs(output_folder, exist_ok=True)
        
        for ip_prefix in ip_prefixes:
            ip_prefix = ip_prefix.strip()
            if ip_prefix:
                print(f"{Fore.YELLOW}Processing IP prefix: {ip_prefix}")
                network = ipaddress.ip_network(ip_prefix)
                
                for ip in network.hosts():
                    ip_list.append(str(ip))
                    if len(ip_list) >= batch_size:
                        # Menyimpan batch ke file
                        filename = os.path.join(output_folder, f"{output_base_filename}{file_index}.txt")
                        with open(filename, 'w') as outfile:
                            outfile.write("\n".join(ip_list))
                        
                        total_ips += len(ip_list)
                        print(f"{Fore.GREEN}Saved {len(ip_list)} IP addresses to {filename}")
                        
                        ip_list = []  # Reset batch
                        file_index += 1
        
        # Menyimpan sisa IP jika ada
        if ip_list:
            filename = os.path.join(output_folder, f"{output_base_filename}{file_index}.txt")
            with open(filename, 'w') as outfile:
                outfile.write("\n".join(ip_list))
            
            total_ips += len(ip_list)
            print(f"{Fore.GREEN}Saved {len(ip_list)} IP addresses to {filename}")
        
        print(f"{Fore.CYAN}Total alamat IP yang dihasilkan: {total_ips}")

    except FileNotFoundError as e:
        print(f"{Fore.RED}File tidak ditemukan: {e}")
    except IOError as e:
        print(f"{Fore.RED}Kesalahan I/O: {e}")

def main():
    print(f"{Fore.MAGENTA}Selamat datang di program pemroses IP prefix!")
    
    # Meminta pengguna untuk memasukkan nama file input
    input_file = input(f"{Fore.CYAN}Silahkan masukkan nama file input (misalnya, ip_prefixes.txt): ").strip()
    
    # Meminta pengguna untuk memasukkan nama file output dasar
    output_base_filename = input(f"{Fore.CYAN}Silahkan masukkan nama file output dasar (misalnya, blabla): ").strip()
    
    # Meminta pengguna untuk memasukkan nama folder output
    output_folder = input(f"{Fore.CYAN}Silahkan masukkan nama folder output (misalnya, result): ").strip()
    
    # Memproses file input dan menghasilkan file output
    process_ip_prefix_file(input_file, output_base_filename, output_folder)

if __name__ == "__main__":
    main()
