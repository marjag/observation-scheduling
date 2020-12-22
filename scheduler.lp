% Problem encoding
%% GENERATE

% przypisac satelite do wykonywanej akcji, dla kazdej akcji
% obserowanie - moze, ale nie musi byc wykonane, jezeli jest, to tylko 1 satelita
{ execute(Action,Sat) : satellite(Sat) } 1 :- action(Action,observe).
% downlink - moze, ale nie musi byc wykonane
{ execute(Action,Sat) : satellite(Sat) } :- action(Action,downlink).
% uplink - zawsze musi byc wykonane przez wszystkie satelity
1 { execute(Action,Sat) : satellite(Sat) } 1 :- satellite(Sat), action(Action,uplink).

% wybrac z mozliwych czas wykonywania zadan dla okna kazdej akcji, dla kazdego satelity
% czas wykonywania akcji musi miescic sie w dostepnych oknach czasowych
1 { sat_action_window(Action,Sat,Start,End) : action_window(Action,WStart,WEnd),
satellite(Sat),
action(Action,Type),
sat_action_time(Sat,Type,Duration),
time(Start),
Start >= WStart,
End = Start+Duration-1,
End <= WEnd
 } 1 :- execute(Action,Sat).


% akcje nie moga sie na siebie nakladac
:- time(Time), satellite(Sat), #count { Action : execute(Action,Sat), sat_action_window(Action,Sat,Start,End), Time>=Start, Time<=End} > 1.

% parametry satelity
% zuzycie pamieci satelit w danym czasie
% downlink zwalnia zuzyta pamiec
sat_memory(Sat,Action,0) :- execute(Action,Sat), action(Action,downlink).
% obserwacje zajmuja pamiec
sat_memory(Sat,Action,Use) :- execute(Action,Sat), action(Action,observe),
LastDownlink = #max {A: execute(A,S), action(A,downlink), S=Sat, A < Action },
Use = #sum {Units,A,D,S: execute(A,S), action(A,observe), memory_use(S,Units), A <= Action, A > D, S=Sat, D=LastDownlink }.

% zuzycie energii
sat_energy(Sat,Action,Amount) :- execute(Action,Sat),
sat_energy(Sat,0,Initial), energy_gen(Sat,Units), sat_action_window(Action,Sat,Start,End),
Cost = #sum { U,A : execute(A,S), A <= Action, energy_use(S,U), S=Sat },
Gen = Units * Start,
Amount = Initial+Gen-Cost.

% statystyki dot. ilosci akcji wykonywanych przez satelity
executed(Sat,Cnt) :- satellite(Sat), Cnt = #count {A: execute(A,S), S=Sat }.
observed(Sat,Cnt) :- satellite(Sat), Cnt = #count {A: execute(A,S), action(A,observe), S=Sat }.
downlinked(Sat,Cnt) :- satellite(Sat), Cnt = #count {A: execute(A,S), action(A,downlink), S=Sat }.


%% TEST
% wykluczyc modele z przekroczeniem pamieci
:- sat_memory(Sat,Action,Val), memory_storage(Sat,Max),Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- sat_energy(Sat,Action,Val), Val < 1.

% wykluczyc modele, w ktorych nie wykonano zadan awaryjnych
:- not execute(Action,_), emergency_task(Action).


%% OPTIMISE
% jakosc harmonogramowania zadan (suma priorytetow przipisanych zadan)
quality(X) :- X = #sum { Priority,Action : priority(Action,Priority), execute(Action,Sat) }.

% maksymalizuj jakosc harmonogramowania
#maximize { X@4 : quality(X) }.
% minimalizuj ilosc akcji wykonanych
#minimize { X@1 : executed(Sat,X) }.

#show emergency_task/1.
#show execute/2.
#show executed/2.
#show observed/2.
#show downlinked/2.
#show sat_action_window/4.
#show sat_memory/3.
#show sat_energy/3.
#show quality/1.
