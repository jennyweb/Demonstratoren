with open('DivingComputer\divingprofile.txt', 'w') as fout:
    fout.write('Zeit\tTiefe\n')
    aktuelleTiefe = 0
    for i in range(200):
        aktuelleZeit = i * 10
        if aktuelleTiefe < 18:
            if aktuelleZeit % 4 == 0:
                aktuelleTiefe = aktuelleTiefe
            else:
                aktuelleTiefe = i * 0.3
            fout.write(f'{aktuelleZeit}\t{aktuelleTiefe}\n')
        else: 
            aktuelleTiefe = 18
            fout.write(f'{aktuelleZeit}\t{aktuelleTiefe}\n')

