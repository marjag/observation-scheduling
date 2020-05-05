% Problem encoding
%%GENERATE
% wybrac przypisanie satelity na orbicie (Orbit) do zadania (Task), kazde zadanie wykonac max raz, po zadaniu poprzednim
{ link(Task, Orbit) : o(Orbit) } 1 :- doable(Task).

% poczatek obserwacji od zadania 1
doable(1).
% zadanie (Task) musi byc wykonane w kolejnosci (Order), czyli po zadaniu porzedzajacym (TaskPrev)
doable(Task) :- t(Task), t(TaskPrev), y(TaskPrev, Task, Order), Order = 1, doable(TaskPrev).

% praca satelity - obserwacje nie moga sie na siebie nakladac (optymalizowalne)
upload(Time) :- cw(_, Start, End), Time=Start..End.
download(Time) :- gw(_, Start, End), Time=Start..End.
observe(Time) :- link(Task, _), tw(Task,Start,End), Time=Start..End.

% zuzycie pamieci satelit pomiedzy stacjami naziemnymi
% satelita | od stacji nr... do nastepnej | zuzycie
busy(Orbit, GS, Mem) :- o(Orbit), gw(GS, GStart, GEnd), gw(GS+1, NextStart, NextEnd), 
Mem = #sum { Use,Task : link(Task, Orbit), w_use(Orbit, Use), tw(Task, TStart, TEnd), TEnd >= GEnd, TEnd <= NextStart  }. 

% zuzycie energii
energy(Orbit,Val) :- o(Orbit), Val = #sum { Use,Task : link(Task, Orbit), e_use(Orbit,Use) }.

% jakosc harmonogramowania zadan (suma priorytetow polaczonych zadan)
quality(X) :- X = #sum { Priority,Task : p(Task,Priority), link(Task,Orbit) }.

%%TEST
% wykluczyc modele, gdzie zadanie (Task) wykonane jest na orbicie (Orbit) na ktorej nie powinno (X) (optymalizowalne)
:- link(Task, Orbit), t(Task), o(Orbit), x(Task, Orbit, Execute), Execute = 0.

% wykluczyc modele z przekroczeniem pamieci
:- busy(Orbit, _, Val), w(Orbit,Max), Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- energy(Orbit,Val), e(Orbit,Max), Val > Max.

#maximize { X@3 : quality(X) }.
#minimize { X@2 : busy(Oid, GS, X) }.
#minimize { X@1 : energy(Oid, X) }.

#show link/2.
#show energy/2.
#show quality/1.
#show observe/1.
#show busy/3.


