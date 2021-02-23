time(1..1800).
orbit(1).
action_type(observe).
action(1,observe).
sat_action_time(1,observe,4).
execute(1,1).
action_window(1,1,14).


1 { action_scheduled(Action,O,Start,End) : time(Start),
action_window(Action,Start,WEnd),
time(End),
End = Start+Duration-1,
End <= WEnd,
sat_action_time(O,Type,Duration)
} 1 :- 
execute(Action,O)
.