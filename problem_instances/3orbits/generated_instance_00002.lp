% Instancja wygenerowana automatycznie
orbit(1). orbit(2). orbit(3).

satellite(orbit(1),kosmos). satellite(orbit(2),sentinel). satellite(orbit(3),landsat).

energy_gen(satellite(1),8). energy_gen(satellite(2),8). energy_gen(satellite(3),8). 

energy_storage(satellite(1),500). energy_storage(satellite(2),800). energy_storage(satellite(3),800).

energy_use(satellite(1),40). energy_use(satellite(2),20). energy_use(satellite(3),20).

memory_storage(satellite(1),800). memory_storage(satellite(2),900). memory_storage(satellite(3),900).

memory_use(satellite(1),50). memory_use(satellite(2),40). memory_use(satellite(3),40).

sat_action_time(satellite(1),downlink,12). sat_action_time(satellite(1),observe,12). sat_action_time(satellite(1),uplink,8).
sat_action_time(satellite(2),downlink,12). sat_action_time(satellite(2),observe,10). sat_action_time(satellite(2),uplink,9).
sat_action_time(satellite(3),downlink,9). sat_action_time(satellite(3),observe,8). sat_action_time(satellite(3),uplink,9).

sat_energy(1,0,500). sat_energy(2,0,800). sat_energy(3,0,800).

sat_memory(1,0,0). sat_memory(2,0,0). sat_memory(3,0,0).

action_type(downlink). action_type(observe). action_type(uplink).
action(1,downlink).
action(2,observe).
action(3,observe).
action(4,observe).
action(5,observe).
action(6,observe).
action(7,observe).
action(8,observe).
action(9,observe).
action(10,observe).
action(11,observe).
action(12,uplink).
action(13,observe).
action(14,observe).
action(15,observe).
action(16,observe).
action(17,observe).
action(18,uplink).
action(19,observe).
action(20,observe).
action(20,observe).
action(21,observe).
action(22,observe).
action(23,observe).
action(24,observe).
action(25,observe).

action_window(1,6,14).
action_window(2,63,72).
action_window(3,99,110).
action_window(4,126,135).
action_window(5,166,176).
action_window(6,280,292).
action_window(7,242,251).
action_window(8,284,295).
action_window(9,402,410).
action_window(10,452,460).
action_window(11,502,513).
action_window(12,498,506).
action_window(13,727,737).
action_window(14,721,732).
action_window(15,568,578).
action_window(16,831,841).
action_window(17,964,976).
action_window(18,1023,1032).
action_window(19,993,1003).
action_window(20,769,779).
action_window(20,1145,1157).
action_window(21,1204,1213).
action_window(22,1265,1277).
action_window(23,1102,1111).
action_window(24,1273,1282).
action_window(25,1327,1336).

visible(1,1,1). visible(2,1,1). visible(3,1,1). visible(4,1,1).
visible(5,1,1). visible(6,1,1). visible(7,1,0). visible(8,1,1).
visible(9,1,1). visible(10,1,1). visible(11,1,1). visible(12,1,1).
visible(13,1,1). visible(14,1,1). visible(15,1,0). visible(16,1,1).
visible(17,1,1). visible(18,1,1). visible(19,1,1). visible(20,1,1).

visible(1,2,0). visible(2,2,1). visible(3,2,1). visible(4,2,1).
visible(5,2,1). visible(6,2,1). visible(7,2,1). visible(8,2,1).
visible(9,2,1). visible(10,2,1). visible(11,2,1). visible(12,2,1).
visible(13,2,1). visible(14,2,1). visible(15,2,1). visible(16,2,1).
visible(17,2,0). visible(18,2,1). visible(19,2,0). visible(20,2,0).

visible(1,3,1). visible(2,3,0). visible(3,3,1). visible(4,3,1).
visible(5,3,1). visible(6,3,1). visible(7,3,0). visible(8,3,1).
visible(9,3,1). visible(10,3,1). visible(11,3,1). visible(12,3,0).
visible(13,3,1). visible(14,3,1). visible(15,3,1). visible(16,3,0).
visible(17,3,0). visible(18,3,1). visible(19,3,0). visible(20,3,0).

visible(21,1,1).
visible(21,2,0).
visible(21,3,1).
visible(22,1,0).
visible(22,2,1).
visible(22,3,1).
visible(23,1,1).
visible(23,2,0).
visible(23,3,1).
visible(24,1,1).
visible(24,2,1).
visible(24,3,1).
visible(25,1,1).
visible(25,2,1).
visible(25,3,0).

emergency_task(2). emergency_task(8). emergency_task(16). emergency_task(20). emergency_task(21). emergency_task(25).

priority(2,35).  priority(3,38).
priority(4,36). priority(5,40).
priority(6,43). priority(7,6).
priority(8,21). priority(9,26).
priority(10,25). priority(11,28).
priority(13,3). priority(14,23).
priority(15,35). priority(16,3).
priority(17,6). priority(19,38).
priority(20,17).
priority(21,30).
priority(22,39).
priority(23,47).
priority(24,28).
priority(25,9).






