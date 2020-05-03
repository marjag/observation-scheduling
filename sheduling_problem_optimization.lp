% Problem encoding

%%GENERATE
% wybrac przypisanie satelity na orbicie (Orbit) do zadania (Task), kazde zadanie wykonac max raz, po zadaniu poprzednim
{ link(Task, Orbit) : o(Orbit) } 1 :- doable(Task).

% poczatek obserwacji od zadania 1
doable(1).
% zadanie (Task) musi byc wykonane w kolejnosci (Order), czyli po zadaniu porzedzajacym (TaskPrev)
doable(Task) :- t(Task), t(TaskPrev), y(TaskPrev, Task, Order), Order = 1, doable(TaskPrev).

% praca satelity - obserwacje i transfer danych nie moga sie na siebie nakladac
work(Time) :- link(Task, _), tw(Task,Start,End), Time=Start..End.
work(Time) :- cw(_, Start, End), Time=Start..End.
work(Time) :- gw(_, Start, End), Time=Start..End.

% zuzycie pamieci
memory(Orbit,Val) :- o(Orbit), Val = #sum { Use,Task : link(Task, Orbit), w_use(Orbit,Use) }.

% zuzycie energii
energy(Orbit,Val) :- o(Orbit), Val = #sum { Use,Task : link(Task, Orbit), e_use(Orbit,Use) }.

%%TEST
% wykluczyc modele, gdzie zadanie (Task) wykonane jest na orbicie (Orbit) na ktorej nie powinno (X) (optymalizowalne)
:- link(Task, Orbit), t(Task), o(Orbit), x(Task, Orbit, Execute), Execute = 0.

% wykluczyc modele z nakladajacymi sie procesami (optymalizowalne)


% wykluczyc modele z przekroczeniem pamieci
:- memory(Orbit,Val), w(Orbit,Max), Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- energy(Orbit,Val), e(Orbit,Max), Val > Max.


% jakosc harmonogramowania zadan (suma priorytetow polaczonych zadan)
quality(X) :- X = #sum { Priority,Task : p(Task,Priority), link(Task,Orbit) }.

#maximize { X@3 : quality(X) }.
#minimize { X@2 : energy(Oid, X) }.
#minimize { X@1 : memory(Oid, X) }.

#show link/2.
#show memory/2.
#show energy/2.
#show quality/1.
#show work/1.


