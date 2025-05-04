% Daftar jenis cuaca
cuaca(cerah).
cuaca(mendung).
cuaca(hujan).
cuaca(badai).

% Gejala untuk masing-masing cuaca
gejala(langit_cerah, cerah).
gejala(suhu_panas, cerah).

gejala(awan_gelap, mendung).
gejala(angin_sepoi, mendung).

gejala(awan_tebal, hujan).
gejala(rintik_air, hujan).
gejala(langit_gelap, hujan).

gejala(angin_kencang, badai).
gejala(kilat, badai).
gejala(guntur, badai).

% Pertanyaan untuk masing-masing gejala
pertanyaan(langit_cerah, "Apakah langit tampak cerah?").
pertanyaan(suhu_panas, "Apakah suhu terasa panas?").
pertanyaan(awan_gelap, "Apakah langit dipenuhi awan gelap?").
pertanyaan(angin_sepoi, "Apakah ada angin sepoi-sepoi?").
pertanyaan(awan_tebal, "Apakah langit tampak berawan tebal?").
pertanyaan(rintik_air, "Apakah ada rintik-rintik air hujan?").
pertanyaan(langit_gelap, "Apakah langit tampak gelap?").
pertanyaan(angin_kencang, "Apakah angin bertiup kencang?").
pertanyaan(kilat, "Apakah terlihat kilatan petir?").
pertanyaan(guntur, "Apakah terdengar suara guntur?").

% Diagnosa cuaca
diagnosa(Cuaca) :-
    cuaca(Cuaca),
    cocok(Cuaca).

% Cocokkan gejala positif
cocok(Cuaca) :-
    forall(gejala(G, Cuaca), gejala_pos(G)).
