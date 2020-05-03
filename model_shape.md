Założenia:

1. Koszt pamięciowy każdego zadania jest jednakowy, zatem dostępna pamięć jest liczona w jednostce zadań.
2. Dostarczanie danych dotyczących zadań odbywa się, gdy satelita znajduje się nad stacją naziemną. Okno czasowe dostarczenia obejmuje całe okno czasowe widoczności stacji.
3. Odbieranie harmonogramu odbywa się, gdy satelita znajduje się nad stacją kontrolną. Okno czasowe odbioru obejmuje całe okno czasowe widoczności stacji.
Ograniczenia: 
- satelita może zajmować w danym czasie jedną orbitę
- orbitę może zajmować w danym czasie tylko jeden satelita
- każde zadanie może być wykonane maksymalnie 1 raz
- każde okno czasowe widoczności stacji kontrolnej musi być wykorzystane na wykonanie odbierania danych przez satelite
- każde okno czasowe widoczności stacji naziemniej musi być wykorzystane na wykonanie wysyłania danych przez satelite
- żadne okno czasowe nie może nakładać się na drugie
- wykonywanie zadania musi odbyć się w jego dostępnym oknie czasowym widoczności
- każdy satelita może pomieścić maksymalnie tyle danych z zadań ile wynosi jego pamięć
- pomiędzy stacjami naziemnymi można wykonac maksymalna ilość zadan związana z pamięcią satelity

Model:
- orbita z satelitą

o(OId).

- zadania do wykonania

t(TId).

- wagi zadan

zadanie | waga

p(TId,N).

- zadania na orbitach - czy nalezy wykonac na orbicie j

zadanie i | orbita j | 1 - TAK : 0 - NIE

x(TId,OId,Do).

- kolejnosc wykonywania zadan

zadanie i | zadanie k | 1 - TAK (i poprzedza j) : 0 - NIE (nie sa w kolejnosci)

y(TId,TId,After).

- okna czasowe

Okno zadania | zadanie i | start zadania | koniec zadania

tw(TId,Start,End).

Okno st. kontr. | start okna dla stacji kontrolnej | koniec okna

cw(CId,Start,End).

Okno st. naziemn. | start okna dla stacji naziemnej | koniec okna

gw(GId,Start,End).

- pamiec satelity na orbicie

orbita | pamiec

w(OId,Memory).

- zuzycie pamieci satelity na orbicie

orbita | zuzycie per zadanie

w_use(OId,WUse).

- energia satelity na orbicie

orbita | energia

e(Oid,Energy).

- zuzycie energii satelity na orbicie (w jednostce zadania)

orbita | zuzycie per zadanie

e_use(Oid,EUse).


