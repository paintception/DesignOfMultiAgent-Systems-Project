#!/bin/sh

PARAMS="-f-1 -g7 -a147 -s30 -m10"
NUM_SIMS=100

rm results/results.json

echo "Running $NUM_SIMS simulations with parameters: $PARAMS"
for i in `seq 1 $NUM_SIMS`; do
	echo ">>>>>>>>>>>>>>>>>>>>> Simulation $i"
	# run the simulation with random routes and with memory
	./main.py $PARAMS -i $i -w
	[ $? -eq 0 ] || exit

	# run it again, reusing the routes and without memory
	./main.py $PARAMS -p results/parameters.json -i $i
	[ $? -eq 0 ] || exit
done
