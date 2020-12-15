#!/bin/bash
switchA=$1
output_file="out.lp"

cd /home/marcin/Pulpit/magisterka/observation-scheduling;

if [[ $switchA == "sort" ]]; then
	clingo scheduling_problem_optimization.lp problem_instance.lp 0 > $output_file;
	python models_processor.py;
	rm $output_file;
else
	clingo scheduling_problem_optimization.lp problem_instance.lp 0;
fi
