% Problem encoding
%%GENERATE
% wybrac przypisanie satelity na orbicie (Orbit) do zadania (Task), kazde zadanie wykonac max raz, po zadaniu poprzednim
{ link(Task, Orbit) : orbit(Orbit) } 1 :- doable(Task).

% poczatek obserwacji od zadania 1
doable(1).
% zadanie (Task) musi byc wykonane w kolejnosci (Order), czyli po zadaniu porzedzajacym (TaskPrev)
doable(Task) :- task(Task), task(TaskPrev), task_order(TaskPrev, Task, Order), Order = 1, doable(TaskPrev).

% praca satelity - obserwacje nie moga sie na siebie nakladac (optymalizowalne)
upload(Time) :- control_window(_, Start, End), Time=Start..End.
download(Time) :- ground_window(_, Start, End), Time=Start..End.
observe(Time) :- link(Task, _), task_window(Task,Start,End), Time=Start..End.

% zuzycie pamieci satelit pomiedzy stacjami naziemnymi
% satelita | od stacji nr... do nastepnej | zuzycie
memory_busy(Orbit, GS, Mem) :- orbit(Orbit), ground_window(GS, GStart, GEnd), ground_window(GS+1, NextStart, NextEnd), 
Mem = #sum { Use,Task : link(Task, Orbit), memory_use(Orbit, Use), task_window(Task, TStart, TEnd), TEnd >= GEnd, TEnd <= NextStart  }. 

% zuzycie energii
energy(Orbit,Val) :- orbit(Orbit), Val = #sum { Use,Task : link(Task, Orbit), energy_use(Orbit,Use) }.

% jakosc harmonogramowania zadan (suma priorytetow polaczonych zadan)
quality(X) :- X = #sum { Priority,Task : priority(Task,Priority), link(Task,Orbit) }.

%%TEST
% wykluczyc modele, gdzie zadanie (Task) wykonane jest na orbicie (Orbit) na ktorej nie powinno (X) (optymalizowalne)
:- link(Task, Orbit), task(Task), orbit(Orbit), task_orbit(Task, Orbit, Execute), Execute = 0.

% wykluczyc modele z przekroczeniem pamieci
:- memory_busy(Orbit, _, Val), memory_storage(Orbit,Max), Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- energy(Orbit,Val), energy_storage(Orbit,Max), Val > Max.

#maximize { X@3 : quality(X) }.
#minimize { X@2 : memory_busy(Oid, GS, X) }.
#minimize { X@1 : energy(Oid, X) }.

#show link/2.
#show energy/2.
#show quality/1.
#show observe/1.
#show memory_busy/3.


