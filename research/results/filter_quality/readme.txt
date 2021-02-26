Tests some more complex instance against Extension filter_qulity.lp

Demo of finding the first solution to reach a valid schedule
- with a condition of solution quality 55% having 100 tasks to schedule
run:
$ clingo scheduler.lp quality55.lp extensions/filter_quality.lp --const quality=55 1

- with a condition of solution quality 70% having 50 tasks to schedule and 4 orbits (multiple extension use)
run:
$ clingo scheduler.lp 4_orbits.lp extensions/with_orbits_3_4.lp extensions/filter_quality.lp --const quality=70 1

