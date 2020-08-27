Model dla problemu łączenia zadań z satelitami powinien zawierać:
- podstawową wersje problemu (zbiór zadań, zbiór satelitów oraz okna czasowe),
- skończoną pamięć satelitów,
- stacje naziemne,
- skończoną energię satelitów,
- zadania awaryjne,
- stacje kontrolne.














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


Modele

MODEL I

1. Zadanie

T - identyfikator zadania
{t1..tn}
n - ilość zadań

X - wykonywanie zadań
{x11..xij}
i - identyfikator zadania
j - identyfikator orbity

xij = 0 || xij = 1
1 - zadanie i ma być wykonane na orbicie j
0 - zadanie i NIE ma być wykonane na orbicie j

p - waga zadania (priorytet)
{p1..pn}

y - kolejność zadań
{y11..yih}
i, h - identyfikator zadania

yih = 0 || yih = 1
1 - zadanie h ma być wykonane po zadaniu i
0 - zadanie h NIE ma być wykonane po zadaniu i


2. Orbity
O - orbita j zajęta przez satelitę wykonującego zadania
{o1..oj}

3. Pamięć
W - pojemność pamięciowa satelity na orbicie j
{W1..Wj}

w - zużycie pamięci na zadanie dla satelity na orbicie j
{w1..wj}

4. Energia
E - pojemność energetyczna energii satelity na orbicie j
{E1..Ej}

w - zużycie pamięci na zadanie dla satelity na orbicie j
{e1..ej}


5. Okno czasowe
TW - okno czasowe dla zadania
{TW1..TWn}
TWi = [ tsi , tei ]
tsi - (time start i) - czas rozpoczęcia zadania i w oknie czasowym
tsi - (time end i) - czas zakończenia zadania i w oknie czasowym



MODEL II

1. Zadanie
t, tv, d, ar, dl

t - identyfikator zadania
tv - wartosc zadania
d - czas trwania (okno czasowe wykonywania zadania)
ar - czas rozpoczecia zadania
dl - limit czasowy
- ogólne
- awaryjne:
zadania o wyższym priorytecie i wymaganym krótkim (limitowanym) czasie wykonania, nieznane podczas poprzedniego harmonogramowania

2. Satelita
S - identyfikator satelity
{s1..sn}

3. Stacja kontrolna
C - identyfikator stacji kontrolnej
{c1..cn}

4. Stacja naziemna
G - identyfikator stacji naziamnej
{g1..gn}

5. Okno czasowe
CW - okno czasowe widoczności stacji kontrolnej c
GW - okno czasowe widoczności stacji naziemnej g
TW - okno czasowe widoczności zadania t

