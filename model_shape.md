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

o(OId).

- zadania do wykonania

t(TId).

- wagi zadan

zadanie i | waga

p(TId,N).

- zadanie na orbitach - (czy nalezy wykonac na orbicie j)

zadanie i | orbita j | 1 - TAK : 0 - NIE

x(TId,OId,Do).

- kolejnosc wykonywania zadan

zadanie i | zadanie j | 1 - TAK (i poprzedza j) : 0 - NIE (nie sa w kolejnosci)

y(TId,TId,After).

- okna czasowe

Zadania:

zadanie i | start okna | koniec okna

tw(TId,Start,End).

Stacji kontrolnej

stacja kontrolna i | start okna | koniec okna

cw(CId,Start,End).

Stacji naziemnej

stacja naziemna i | start okna | koniec okna

gw(GId,Start,End).

- pamięć satelity na orbicie

orbita i | pamiec

w(OId,Memory).

- zużycie pamięci satelity na orbicie

orbita i | zużycie (w jednostce zadań)

w_use(OId,WUse).

- energia satelity na orbicie

orbita i | energia

e(Oid,Energy).

- zużycie energii satelity na orbicie

orbita i | zużycie (w jednostce zadań)

e_use(Oid,EUse).


