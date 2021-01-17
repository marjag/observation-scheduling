% Problem encoding
%% GENERATE
% okres harmonogramowania [s]
time(1..1800). % 30 minut

% przypisac satelite do wykonywanej akcji, dla kazdej akcji
% obserwacja - moze byc wykonana na jednej z orbit z ktorej widac dany obszar
{ execute(Action,Sat) : orbit(Sat), visible(Action,Sat,1) } 1 :- action(Action,observe).
% downlink - moze, ale nie musi byc wykonane
{ execute(Action,Sat) : orbit(Sat), visible(Action,Sat,1) } :- action(Action,downlink).
% uplink - musi byc wykonane przez wszystkie satelity majace mozliwosc wykonania
execute(Action,Sat) :- orbit(Sat), visible(Action,Sat,1), action(Action,uplink).

% wybrac z mozliwych czas wykonywania zadan dla okna kazdej akcji, dla kazdego satelity
% czas wykonywania akcji musi miescic sie w dostepnych oknach czasowych
1 { action_scheduled(Action,Sat,Start,End) : action_window(Action,WStart,WEnd),
time(Start),
End = Start+Duration-1,
Start >= WStart,
End <= WEnd
 } 1 :- execute(Action,Sat), orbit(Sat), action(Action,Type), sat_action_time(Sat,Type,Duration), action_type(Type).

% parametry satelity
% zuzycie pamieci satelit w danym czasie
% downlink zwalnia zuzyta pamiec
sat_memory(Sat,Action,0) :- execute(Action,Sat), action(Action,downlink), orbit(Sat).
% obserwacje zajmuja pamiec
sat_memory(Sat,Action,Use) :- execute(Action,Sat), action(Action,observe), orbit(Sat),
LastDownlink = #max {A: execute(A,S), action(A,downlink), S=Sat, A < Action },
Use = #sum {Units,A,D,S: execute(A,S), action(A,observe), memory_use(S,Units), A <= Action, A > D, S=Sat, D=LastDownlink }.

% zuzycie energii
sat_energy(Sat,Action,Amount) :- execute(Action,Sat), orbit(Sat),
sat_energy(Sat,0,Initial), energy_gen(Sat,Units), action_scheduled(Action,Sat,Start,End),
Cost = #sum { U,A : execute(A,S), A <= Action, energy_use(S,U), S=Sat },
Gen = Units * Start,
Amount = Initial+Gen-Cost,
Amount <= Initial.

% statystyki dot. ilosci akcji wykonywanych przez satelity
executed(Sat,Cnt) :- orbit(Sat), Cnt = #count {A: execute(A,S), S=Sat }.
observed(Sat,Cnt) :- orbit(Sat), Cnt = #count {A: execute(A,S), action(A,observe), S=Sat }.
downlinked(Sat,Cnt) :- orbit(Sat), Cnt = #count {A: execute(A,S), action(A,downlink), S=Sat }.

%% TEST

% akcje nie moga sie na siebie nakladac
:- time(Time), orbit(Sat), #count { Action : execute(Action,Sat), action_scheduled(Action,Sat,Start,End), Time>=Start, Time<=End} > 1.

% wykluczyc modele z przekroczeniem pamieci
:- sat_memory(Sat,Action,Val), memory_storage(Sat,Max), action(Action,Type), orbit(Sat), Val > Max.

% wykluczyc modele z wyczerpaniem energii
:- sat_energy(Sat,Action,Val), action(Action,Type), orbit(Sat), Val < 1.

% wykluczyc modele, w ktorych nie wykonano istniejacych zadan awaryjnych
:- not execute(Action,_), action(Action,observe), emergency_task(Action).

%% OPTIMISE
% jakosc harmonogramowania zadan (suma priorytetow przipisanych zadan)
quality(X) :- X = #sum { Priority,Action : priority(Action,Priority), execute(Action,Sat) }.

% maksymalizacja jakosci harmonogramowania
#maximize { X@5 : quality(X) }.

% inne mozliwosci...
%*
memory_used(X) :- 
X = #sum { U,Sat: observed(Sat,Cnt), memory_use(Sat,Use), U=Use*Cnt }.
energy_used(X) :- 
X = #sum { U,Sat: executed(Sat,Cnt), energy_use(Sat,Use), U=Use*Cnt }.
% minimalizacja sumy zuzycia energii
#minimize { X@1 : energy_used(X) }.
% minimalizacja sumy zuzycia pamieci
#minimize { X@1 : memory_used(X) }.
#show memory_used/1.
#show energy_used/1.
*%

#show action_scheduled/4.
#show executed/2.
#show observed/2.
#show downlinked/2.
#show quality/1.
#show sat_memory/3.
%*
#show execute/2.
#show sat_energy/3.
*%