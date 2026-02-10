## Return
Penjelasan:
Saat Python bertemu kata return, fungsi langsung selesai dan keluar. Baris kedua tidak akan dieksekusi.
Akibatnya, fungsi main() hanya mengembalikan 1 data (list coords), padahal di bawah Anda memanggilnya dengan 2 variabel (coords, vehicle_start = main()). Ini menyebabkan error: ValueError: not enough values to unpack.
Solusi:
Gabungkan menjadi satu baris:
code
Python
return coords, vehicle_start

## PROBLEM 2 nonlocal scope 
Kesalahan Scope Variabel (Logic Error)
Variabel vehicle_start didefinisikan di dalam main, tetapi Anda mencoba mengubah isinya di dalam fungsi anak addtostart.
Dalam Python, jika Anda melakukan vehicle_start = (lon2, lat2) di dalam fungsi anak, Python menganggap Anda membuat variabel baru lokal di fungsi itu, bukan mengubah variabel vehicle_start milik main. Akibatnya, saat program selesai, vehicle_start akan tetap bernilai None.
Solusi:
Gunakan kata kunci nonlocal di dalam fungsi addtostart.