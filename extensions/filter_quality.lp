%% Extension
%*
 * Returns stable models schedules with
 * at least X percent quality reached
*%
% target quality. To control, use clingo option --const quality=n
#const quality = 50.
target(X*quality/100) :- X = #sum { Priority,Action : priority(Action,Priority) }.
:- quality(X), target(Y), X < Y.
