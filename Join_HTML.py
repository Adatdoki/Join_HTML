########### 2024.11.19 16:05:58 ################################## ADATDOKI ####
# ZIP fájlban töltsd fel a HTML fájlokat, kicsomagolja a HTML mappába.
# HTML mappában található összes HTML fájl keletkezési dátum alapján sorrendbe rendezése
# és tartalmuk összefűzése. A végső fájlnév az első fájlnév elejétől a megadott
# szó végéig tartó rész alapján generálódik, és a fájl automatikusan letöltésre kerül.
#########1#########2#########3#########4#########5#########6#########7#########8

import os
import zipfile
from google.colab import files

# Kicsomagolási célmappa
html_folder_path = '/content/HTML'

# ZIP fájl kicsomagolása a célmappába
zip_file_path = '/content/html_files.zip'  # A feltöltött ZIP fájl elérési útvonala
if not os.path.exists(html_folder_path):
    os.makedirs(html_folder_path)  # HTML mappa létrehozása, ha nem létezik

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(html_folder_path)

print(f"A ZIP fájl kicsomagolva a következő mappába: {html_folder_path}")

# Összes HTML fájl listázása és keletkezési dátum alapján rendezése (fordított sorrend)
html_files = [
    (os.path.join(html_folder_path, f), os.path.getctime(os.path.join(html_folder_path, f)))
    for f in os.listdir(html_folder_path) if f.endswith('.html')
]
sorted_html_files = sorted(html_files, key=lambda x: x[1], reverse=True)  # Korábbi->Későbbi  

# Az első fájl <body> előtti tartalmának kivonása
with open(sorted_html_files[0][0], 'r', encoding='utf-8') as first_file:
    first_content = first_file.read()
    pre_body_content_end = first_content.find('<body')
    pre_body_content = first_content[:pre_body_content_end].strip()

# Az összes fájl <body> és </body> közötti tartalmának egyesítése
merged_body_content = "<body>\n"
for file_path, _ in sorted_html_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        body_start = content.find('<body') + len('<body')
        body_end = content.find('</body>')
        if body_start > -1 and body_end > -1:
            body_content = content[body_start:body_end].strip('>').strip()
            merged_body_content += body_content + "\n"
merged_body_content += "</body>"

# Teljes fájlnév kiírása az első fájlból
original_filename = os.path.basename(sorted_html_files[0][0])
print(f"Eredeti fájlnév: {original_filename}")

# Felhasználótól kérjük a szót, amelyig tart a fájlnév
target_word = input("Add meg a fájlnévben szereplő szót, ameddig tartson a fájlnév: ").strip()

# Végső fájl név generálása az elejétől a megadott szó végéig
final_filename = original_filename.split(target_word)[0] + target_word + '.html'

# Végső fájl létrehozása és mentése
final_content = pre_body_content + "\n" + merged_body_content
final_file_path = f'/content/{final_filename}'

with open(final_file_path, 'w', encoding='utf-8') as final_file:
    final_file.write(final_content)

# Fájl letöltése
files.download(final_file_path)
