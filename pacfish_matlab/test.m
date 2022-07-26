% % test perso
clear
% [a1, b1, c1] = load_data('test_input2.hdf5');
% pa = pa_data(a1, b1, c1);
% 
% % tenter de convertir tous les char en uint8 ?
% 
% write_data('test_output.hdf5', pa, 1);
% 
% [a2, b2, c2] = load_data('test_output.hdf5');
% 
% 
%% test egality
% out1 = check_egality(b1, b2);
% out2 = check_egality(c1, c2);
% fprintf("\n\n\nResultat de la comparaison : %d %d\n", out1, out2);
% 

% p1=c1.illuminators.deleteme0000000000.illuminator_geometry_type;
% p2=c2.illuminators.deleteme0000000000.illuminator_geometry_type;
% whos p1 p2
% p1-p2


%%
pa1 = pa_data('test_input.hdf5');
pa1.save_data('test_output.hdf5', 1);
pa2 = pa_data('test_output.hdf5');

%% check if the data contain the same values
out1 = check_egality(pa1.meta_data,         pa2.meta_data);
out2 = check_egality(pa1.meta_data_device,  pa2.meta_data_device);
fprintf("\n\n\nResult of the conversion (with string converts to char): %d %d\n", out1, out2);
