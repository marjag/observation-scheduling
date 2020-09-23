% Problem encoding
%%GENERATE

% wybrac przypisanie satelity na orbicie (Sat) do zadania (Task),kazde zadanie wykonac max raz,po zadaniu poprzednim
{ link(Task,Sat) : satellite(Sat) } 1 :- doable(Task).

% poczatek obserwacji od zadania 1
doable(1).

% zadanie (Task) musi byc wykonane w kolejnosci (Order),czyli po zadaniu porzedzajacym (TaskPrev)
% doable(Task) :- task(Task),task(TaskPrev),task_order(TaskPrev,Task,Order),Order = 1,doable(TaskPrev).

% praca satelity
downlink(Sat,Start,End) :- ground_window(Sat,Station,WStart,WEnd), Start >= WStart, End <= WEnd, End-Start = Duration, sat_downlink(Sat,Duration).

uplink(Sat,Start,End) :- control_window(Sat,Station,WStart,WEnd), sat_uplink(Sat,Duration), Start>=WStart, End<=WEnd, End-Start=Duration.

observe(Sat,Start,End) :- link(Task,Sat),task_window(Task,WStart,WEnd),sat_observe(Sat,Duration),Start>=WStart,End <= WEnd,End-Start=Duration.

% zuzycie pamieci satelit pomiedzy stacjami naziemnymi
% satelita | od stacji nr... do nastepnej | zuzycie
memory_busy(Sat,Gs,Mem) :- satellite(Sat),ground_window(Gs,GStart,GEnd),ground_window(Gs+1,NextStart,NextEnd),
Mem = #sum { Use,Task : link(Task,Sat),memory_use(Sat,Use),task_window(Task,TStart,TEnd),TEnd >= GEnd,TEnd <= NextStart  }. 

% zuzycie energii
energy(Sat,Val) :- satellite(Sat),Val = #sum { Use,Task : link(Task,Sat),energy_use(Sat,Use) }.

% jakosc harmonogramowania zadan (suma priorytetow polaczonych zadan)
quality(X) :- X = #sum { Priority,Task : priority(Task,Priority),link(Task,Sat) }.



%%TEST
% wykluczyc modele,gdzie zadanie (Task) wykonane jest na orbicie (Sat) na ktorej nie powinno (X) (optymalizowalne)
:- link(Task,Sat),task(Task),satellite(Sat),task_satellite(Task,Sat,Execute),Execute = 0.

% wykluczyc modele z przekroczeniem pamieci
:- memory_busy(Sat,_,Val),memory_storage(Sat,Max),Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- energy(Sat,Val),energy_storage(Sat,Max),Val > Max.

#maximize { X@3 : quality(X) }.
#minimize { X@2 : memory_busy(Oid,GS,X) }.
#minimize { X@1 : energy(Oid,X) }.

#show link/2.
#show energy/2.
#show quality/1.
#show observe/1.
#show memory_busy/3.


