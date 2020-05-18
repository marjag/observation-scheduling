Założenia:

1. Koszt pamięciowy każdego zadania jest jednakowy, zatem dostępna pamięć jest liczona w jednostce zadań.
2. Dostarczanie danych dotyczących zadań odbywa się, gdy satelita znajduje się nad stacją naziemną. Okno czasowe dostarczenia obejmuje całe okno czasowe widoczności stacji.
3. Odbieranie harmonogramu odbywa się, gdy satelita znajduje się nad stacją kontrolną. Okno czasowe odbioru obejmuje całe okno czasowe widoczności stacji.
4. Ograniczenia: 
- satelita może zajmować w danym czasie jedną orbitę
- orbitę może zajmować w danym czasie tylko jeden satelita
- każde zadanie może być wykonane maksymalnie 1 raz
- każde okno czasowe widoczności stacji kontrolnej musi być wykorzystane na wykonanie odbierania danych przez satelite
- każde okno czasowe widoczności stacji naziemniej musi być wykorzystane na wykonanie wysyłania danych przez satelite
- żadne wykorzystywane okno czasowe nie może nakładać się na drugie (tylko jedna czynność wykonywana jest w danym czasie)
- wykonywanie zadania musi odbyć się w jego dostępnym oknie czasowym widoczności
- pomiędzy stacjami naziemnymi można wykonać maksymalną ilość zadan związaną z pamięcią satelity i ilością tych zadań

Model:
- orbita z satelitą

orbit(OId).

- zadania do wykonania

task(TId).

- wagi zadan

zadanie i | waga

priority(TId,N).

- zadanie na orbitach - (czy nalezy wykonac na orbicie j)

zadanie i | orbita j | 1 - TAK : 0 - NIE

task_orbit(TId,OId,Do).

- kolejnosc wykonywania zadan

zadanie i | zadanie j | 1 - TAK (i poprzedza j) : 0 - NIE (nie sa w kolejnosci)

task_order(TId,TId,After).

- okna czasowe

Zadania:

zadanie i | start okna | koniec okna

task_window(TId,Start,End).

Stacji kontrolnej

stacja kontrolna i | start okna | koniec okna

control_window(CId,Start,End).

Stacji naziemnej

stacja naziemna i | start okna | koniec okna

ground_window(GId,Start,End).

- pamięć satelity na orbicie

orbita i | pamiec

memory_storage(OId,Memory).

- zużycie pamięci satelity na orbicie

orbita i | zużycie (w jednostce zadań)

memory_use(OId,WUse).

- energia satelity na orbicie

orbita i | energia

energy_storage(Oid,Energy).

- zużycie energii satelity na orbicie

orbita i | zużycie (w jednostce zadań)

energy_use(Oid,EUse).

- generowanie energii satelity na orbicie

orbita i | wartość generowana (na minutę)

energy_gen(Oid,EGen)