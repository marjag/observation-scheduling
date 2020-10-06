% Problem encoding
%%GENERATE

% wybrac z mozliwych czas wykonywania zadan dla okna kazdej akcji, dla kazdego satelity
1 { sat_action_window(Action,Sat,Start,End) : satellite(Sat), time(Start), End = Start+Time-1, sat_action_time(Sat,Type,Time) } 1 :- action(Action,Type), satellite(Sat).

% czas wykonywania akcji musi miescic sie w dostepnych oknach czasowych
:- sat_action_window(Action,Sat,Start,End),
action_window(Action,WStart,WEnd),
Start < WStart.

:- sat_action_window(Action,Sat,Start,End),
action_window(Action,WStart,WEnd),
End > WEnd.


% przypisac satelite do wykonywanej akcji, dla kazdej akcji
% obserowanie - moze, ale nie musi byc wykonane, jezeli jest, to tylko 1 satelita
{ execute(Action,Sat) : satellite(Sat) } 1 :- action(Action,observe).
% downlink - moze, ale nie musi byc wykonane
{ execute(Action,Sat) : satellite(Sat) } :- action(Action,downlink).
% uplink - zawsze musi byc wykonane przez wszystkie satelity
1 { execute(Action,Sat) : satellite(Sat) } 1 :- satellite(Sat), action(Action,uplink).

% akcje nie moga sie na siebie nakladac
:- time(Time), satellite(Sat), #count { Action : execute(Action,Sat), sat_action_window(Action,Sat,Start,End), Time>=Start, Time<=End} > 1.

% praca satelity
% zuzycie pamieci satelit w danym czasie
sat_memory_busy(Sat,Action,Use) :- execute(Action,Sat), action(Action,observe),
Use = #sum { Mem,A : memory_use(S,Mem), execute(A,S), action(A,observe), A<=Action }.

% zuzycie energii
energy(Sat,Action,En) :- satellite(Sat),
En = #sum { Use,Task : do_task_using(Task,Sat), energy_use(Sat,Use) }.

% jakosc harmonogramowania zadan (suma priorytetow przipisanych zadan)
quality(X) :- X = #sum { Priority,Action : priority(Action,Priority), execute(Action,Sat) }.

%%TEST
% wykluczyc modele,gdzie zadanie (Task) wykonane jest na orbicie (Sat) na ktorej nie powinno (X) (optymalizowalne)
%:- do_task_using(Task,Sat),task(Task),satellite(Sat),task_satellite(Task,Sat,Execute),Execute = 0.

% wykluczyc modele z przekroczeniem pamieci
%:- memory_busy(Sat,_,Val),memory_storage(Sat,Max),Val > Max.

% wykluczyc modele z wyczerpaniem energii
%:- energy(Sat,Val),energy_storage(Sat,Max),Val > Max.


#maximize { X@4 : quality(X) }.
%#minimize { X@2 : memory_busy(Oid,GS,X) }.
%#minimize { X@1 : energy(Oid,X) }.


#show execute/2.
%#show sat_action_window/4.
%#show action_window/3.
%#show action/2.
%#show do_task_using/2.
%#show observe_task_during/3.
%#show downlink/3.
%#show uplink/3.
#show sat_memory_busy/3.
#show quality/1.
%#show busy/2.
