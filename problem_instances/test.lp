time(1..18).
orbit(1).
action_type(observe).
action(1,observe).
sat_action_time(1,observe,2).
execute(1,1).
action_window(1,1,4).

%not action_scheduled(_,O,Start..Start+Duration,_)

1 { action_scheduled(Action,O,Start,Start+Duration-1) : time(Start),
Start >= WStart,
Start+Duration-1 <= WEnd,
sat_action_time(O,observe,Duration),
action_window(Action,WStart,WEnd),
execute(Action,O),
 } 1.



%*
1 { action_scheduled(Action,O,Start,End) : action_window(Action,WStart,WEnd),
time(Start),
End = Start+Duration-1,
Start >= WStart,
End <= WEnd
} 1 :- 
execute(Action,O),
orbit(O),
action(Action,Type),
sat_action_time(O,Type,Duration),
action_type(Type),time(Start).
*%

#show action_scheduled/4.