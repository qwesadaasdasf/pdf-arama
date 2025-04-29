import rarfile
import pdfplumber
import os
import shutil
from pathlib import Path

# WinRAR yolunu belirt (Windows için tipik kurulum yolu)
rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\UnRAR.exe"
# veya
# rarfile.UNRAR_TOOL = "C:\\Program Files (x86)\\WinRAR\\UnRAR.exe"

def pdf_ara(rar_dosyasi, aranacak_kelime):
    # Geçici klasör oluştur
    temp_klasor = "gecici_pdf"
    os.makedirs(temp_klasor, exist_ok=True)
    
    try:
        # RAR dosyasını aç ve PDF'leri çıkar
        with rarfile.RarFile(rar_dosyasi) as rf:
            pdf_dosyalari = [f for f in rf.namelist() if f.lower().endswith('.pdf')]
            if not pdf_dosyalari:
                print("RAR dosyasında PDF bulunamadı!")
                return
            
            print(f"{len(pdf_dosyalari)} adet PDF dosyası bulundu. İşleniyor...")
            rf.extractall(temp_klasor)
        
        # Her PDF'de arama yap
        for pdf_dosya in pdf_dosyalari:
            pdf_yolu = os.path.join(temp_klasor, pdf_dosya)
            print(f"\nDosya inceleniyor: {pdf_dosya}")
            
            try:
                with pdfplumber.open(pdf_yolu) as pdf:
                    for sayfa_no, sayfa in enumerate(pdf.pages, 1):
                        metin = sayfa.extract_text()
                        if metin and aranacak_kelime.lower() in metin.lower():
                            print(f"\nSayfa {sayfa_no}'de bulundu!")
                            # Metni paragraflara böl
                            paragraflar = metin.split('\n')
                            for paragraf in paragraflar:
                                if aranacak_kelime.lower() in paragraf.lower():
                                    print("-" * 50)
                                    print(f"Paragraf: {paragraf.strip()}")
                                    print("-" * 50)
            
            except Exception as e:
                print(f"Hata: {pdf_dosya} dosyası işlenirken bir sorun oluştu - {str(e)}")
                continue
    
    finally:
        # Geçici dosyaları temizle
        try:
            shutil.rmtree(temp_klasor)
        except:
            pass

def main():
    print("PDF Arama Programı")
    print("-" * 20)
    
    while True:
        # Kullanıcıdan dosya yolu al
        rar_yolu = input("\nRAR dosyasının yolunu girin (çıkmak için 'q'): ")
        if rar_yolu.lower() == 'q':
            break
            
        if not os.path.exists(rar_yolu):
            print("Dosya bulunamadı! Lütfen doğru dosya yolunu girin.")
            continue
            
        # Aranacak kelimeyi al
        kelime = input("Aranacak kelimeyi girin: ")
        
        # Aramayı başlat
        try:
            pdf_ara(rar_yolu, kelime)
        except Exception as e:
            print(f"Bir hata oluştu: {str(e)}")
            # Hata detayını göster
            import traceback
            print("Hata detayı:")
            print(traceback.format_exc())
        
        print("\nArama tamamlandı!")

if __name__ == "__main__":
    main()
        
        print("\nArama tamamlandı!")

if __name__ == "__main__":
    main()
