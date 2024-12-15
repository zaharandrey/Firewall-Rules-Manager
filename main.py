import subprocess

# Конфігурація брандмауера
def add_block_ip_rule(ip_address):
    """Заборонити трафік з певної IP-адреси."""
    try:
        subprocess.run([
            "sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"
        ], check=True)
        print(f"Блокування трафіку з IP {ip_address} додано.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка додавання правила для IP {ip_address}: {e}")


def add_block_port_rule(port):
    """Заборонити доступ до певного порту."""
    try:
        subprocess.run([
            "sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "DROP"
        ], check=True)
        print(f"Блокування порту {port} додано.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка додавання правила для порту {port}: {e}")


def allow_ip_only(ip_address):
    """Дозволити трафік лише з певної IP-адреси."""
    try:
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], check=True)
        subprocess.run([
            "sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "ACCEPT"
        ], check=True)
        print(f"Дозвіл трафіку тільки з IP {ip_address} активовано.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка налаштування дозволу для IP {ip_address}: {e}")


def list_iptables_rules():
    """Переглянути всі правила iptables."""
    try:
        result = subprocess.run(["sudo", "iptables", "-L", "-n", "-v"], check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Помилка перегляду правил: {e}")


def main():
    while True:
        print("\n--- Меню керування брандмауером ---")
        print("1. Заборонити трафік з IP")
        print("2. Заборонити доступ до порту")
        print("3. Дозволити трафік лише з певної IP-адреси")
        print("4. Переглянути всі правила")
        print("5. Вийти")

        choice = input("Оберіть дію: ")

        if choice == "1":
            ip = input("Введіть IP-адресу для блокування: ")
            add_block_ip_rule(ip)
        elif choice == "2":
            port = input("Введіть номер порту для блокування: ")
            if port.isdigit():
                add_block_port_rule(int(port))
            else:
                print("Некоректний номер порту.")
        elif choice == "3":
            ip = input("Введіть IP-адресу для дозволу: ")
            allow_ip_only(ip)
        elif choice == "4":
            list_iptables_rules()
        elif choice == "5":
            print("Вихід з програми.")
            break
        else:
            print("Некоректний вибір, спробуйте знову.")

if __name__ == "__main__":
    main()

