import requests
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Membuat folder untuk menyimpan gambar
folder_name = "downloaded_images"
os.makedirs(folder_name, exist_ok=True)

# Membaca file PNG.txt
with open('PNG.txt', 'r') as file:
    urls = file.readlines()

total_urls = len(urls)
downloaded_count = 0
start_time = time.time()

def download_image(url):
    url = url.strip()
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Memastikan tidak ada kesalahan dalam permintaan
            
            # Membuat nama file acak dengan awalan BUATSITUS
            random_number = random.randint(10000000, 99999999)
            file_name = os.path.join(folder_name, f"BUATSITUS{random_number}.png")

            # Menyimpan gambar ke file lokal
            with open(file_name, 'wb') as img_file:
                img_file.write(response.content)
                
            return True
        except requests.exceptions.RequestException:
            return False

# Menggunakan ThreadPoolExecutor untuk unduhan paralel
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(download_image, url): url for url in urls}
    for future in as_completed(future_to_url):
        if future.result():
            downloaded_count += 1
            elapsed_time = time.time() - start_time
            estimated_total_time = (elapsed_time / downloaded_count) * total_urls
            remaining_time = estimated_total_time - elapsed_time
            minutes_remaining = remaining_time / 60
            
            print(f"Progres | List {total_urls} | Downloaded {downloaded_count} | Estimasi {int(minutes_remaining)} menit", end='\r')
        else:
            print(f"Gagal mengunduh {future_to_url[future]}")

print("\nProses pengunduhan selesai.")
