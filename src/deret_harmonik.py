def hitung_deret_harmonik(n):
    
    if n <= 0:
        return 0, ""

    hasil = 0.0
    penjabaran = []

    for i in range(1, n + 1):
        hasil += 1 / i
        if i == 1:
            penjabaran.append("1")
        else:
            penjabaran.append(f"(1/{i})")

    penjabaran_str = " + ".join(penjabaran)
    return hasil, penjabaran_str


def validasi_input(input_str):
    
    if not input_str.strip():
        return False, 0, "Input tidak boleh kosong!"
    
    try:
        n = int(input_str)
        if n <= 0:
            return False, 0, "Masukkan harus bilangan bulat positif!"
        elif n > 1000000:  # Batas atas untuk mencegah perhitungan terlalu lama
            return False, 0, "Nilai terlalu besar! Maksimal 1.000.000"
        return True, n, "Valid"
    except ValueError:
        return False, 0, "Masukkan harus berupa bilangan bulat!"