Tests the increase of output with more orbits

- 10 research cases
- each case is 20 tasks
- measurement: execute time, schedule quality (priority sum) with 2 orbits, execute time and quality increase with 4 orbits
- research cases the same as in b&b comparation (21-30)
- expanded each problem instance content using Extension with_3_4_orbits.lp which comprises orbit and satellite-related facts:



orbit(3).
satellite(3,sat_3).
sat_action_time(3, observe, 10).
sat_action_time(3, downlink, 7).
sat_action_time(3, uplink, 8).
sat_memory(3,0,0).
memory_storage(3,200).
memory_use(3,50).
sat_energy(3,0,300).
energy_storage(3,400).
energy_use(3,15).
energy_gen(3,5).

visible(1,3,1).
visible(2,3,0).
visible(3,3,1).
visible(4,3,0).
visible(5,3,1).
visible(6,3,0).
visible(7,3,1).
visible(8,3,0).
visible(9,3,1).
visible(10,3,0).
visible(11,3,1).
visible(12,3,0).
visible(13,3,1).
visible(14,3,0).
visible(15,3,1).
visible(16,3,0).
visible(17,3,1).
visible(18,3,0).
visible(19,3,1).
visible(20,3,0).


orbit(4).
satellite(4,sat_4).
sat_action_time(4, observe, 9).
sat_action_time(4, downlink, 8).
sat_action_time(4, uplink, 7).
sat_memory(4,0,0).
memory_storage(4,400).
memory_use(4,100).
sat_energy(4,0,600).
energy_storage(4,700).
energy_use(4,30).
energy_gen(4,10).

visible(1,3,0).
visible(2,3,1).
visible(3,3,0).
visible(4,3,1).
visible(5,3,0).
visible(6,3,1).
visible(7,3,0).
visible(8,3,1).
visible(9,3,0).
visible(10,3,1).
visible(11,3,0).
visible(12,3,1).
visible(13,3,0).
visible(14,3,1).
visible(15,3,0).
visible(16,3,1).
visible(17,3,0).
visible(18,3,1).
visible(19,3,0).
visible(20,3,1).

