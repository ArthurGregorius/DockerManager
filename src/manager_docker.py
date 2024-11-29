import docker
import pytest
from docker.errors import NotFound, APIError

# Inisialisasi klien Docker
client = docker.from_env()

# Fungsi untuk melihat container yang sedang berjalan
def list_containers():
    """Menampilkan daftar container yang aktif."""
    print("\nDaftar Container yang Aktif:\n")
    try:
        containers = client.containers.list()
        if not containers:
            print("Tidak ada container yang aktif.")
        else:
            for container in containers:
                print(f"ID: {container.id}, Nama: {container.name}, Status: {container.status}")
    except APIError as e:
        print(f"Terjadi kesalahan saat mengambil daftar container: {e}")

# Fungsi untuk menjalankan container
def start_container(container_name):
    """Memulai container berdasarkan nama atau ID."""
    print("\nMemulai container...\n")
    try:
        container = client.containers.get(container_name)
        container.start()
        print(f"Container {container_name} telah dimulai.")
    except NotFound:
        print(f"Container {container_name} tidak ditemukan.")
    except APIError as e:
        print(f"Terjadi kesalahan saat memulai container: {e}")

# Fungsi untuk menghentikan container yang sedang berjalan
def stop_container(container_name):
    """Menghentikan container berdasarkan nama atau ID."""
    print("\nMenghentikan container...\n")
    try:
        container = client.containers.get(container_name)
        container.stop()
        print(f"Container {container_name} telah dihentikan.")
    except NotFound:
        print(f"Container {container_name} tidak ditemukan.")
    except APIError as e:
        print(f"Terjadi kesalahan saat menghentikan container: {e}")

# FUngsi untuk menghapus container
def remove_container(container_name):
    """Menghapus container berdasarkan nama atau ID."""
    print("\nMenghapus container...\n")
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
        print(f"Container {container_name} telah dihapus.")
    except NotFound:
        print(f"Container {container_name} tidak ditemukan.")
    except APIError as e:
        print(f"Terjadi kesalahan saat menghapus container: {e}")

# Fungsi untuk membuat container baru
def create_container(image, name, ports=None, volumes=None):
    """Membuat container baru dari image tertentu."""
    print("\nMembuat container baru...\n")
    try:
        container = client.containers.run(
            image, detach=True, name=name, ports=ports, volumes=volumes
        )
        print(f"Container baru telah dibuat: {container.name}")
    except APIError as e:
        print(f"Terjadi kesalahan saat membuat container: {e}")

# Menu utama untuk pengelolaan container
def main_menu():
    while True:
        print("\n=== Pengelolaan Docker Container ===\n")
        print("1. Lihat daftar container")
        print("2. Membuat container baru")
        print("3. Menjalankan container")
        print("4. Hentikan container")
        print("5. Hapus container")
        print("6. Keluar\n")
        
        choice = input("Pilih opsi: ")
        if choice == "1":
            list_containers()
        elif choice == "2":
            image = input("\nMasukkan nama image: ")
            name = input("Masukkan nama container: ")
            port = input("Port mapping (format: host_port:container_port): ")
            ports = {port.split(":")[1]: port.split(":")[0]} if port else None
            create_container(image, name, ports)
        elif choice == "3":
            name = input("\nMasukkan nama container untuk dimulai: ")
            start_container(name)
        elif choice == "4":
            name = input("\nMasukkan nama container untuk dihentikan: ")
            stop_container(name)
        elif choice == "5":
            name = input("\nMasukkan nama container untuk dihapus: ")
            remove_container(name)
        elif choice == "6":
            print("\nKeluar dari program.\n")
            break
        else:
            print("\nPilihan tidak valid.\n")
            
if __name__ == "__main__":
    main_menu()

# Fitur Utama
# 1 Melihat Daftar Container yang Berjalan: Skrip akan menampilkan semua container aktif beserta statusnya (ID, nama, status, port mapping).
# 2 Menjalankan Container Baru: Menjalankan container dengan image tertentu, menambahkan pengaturan seperti nama container, port, dan volume.
# 3 Menghentikan Container: Menghentikan container tertentu berdasarkan ID atau nama.
# 4 Restart Container: Melakukan restart container untuk memperbarui atau memulihkan aplikasi.
# 5 Menghapus Container: Menghapus container yang telah berhenti atau tidak digunakan.
