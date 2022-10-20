addpath ../pacfish_matlab

file = dir('*.hdf5');
for i=1:length(file)
    pa = pa_data(file(i).name);
    pa_matlab = struct;
    
    % first one
    pa_matlab.binary_time_series_data = pa.binary_time_series_data;
    
    % seconde one
    f = fieldnames(pa.meta_data);
    for j=1:length(f)
        pa_matlab.(f{j}) = pa.meta_data.(f{j});
    end
    
    % third one
    f = fieldnames(pa.meta_data_device.general);
    for j=1:length(f)
        pa_matlab.general.(f{j}) = pa.meta_data_device.general.(f{j});
    end
    
    % illuminators and detectors manage differently...
    ids_dete = fieldnames(pa.meta_data_device.detectors);
    for j=1:length(ids_dete)
        s = pa.meta_data_device.detectors.(ids_dete{i});
        f = fieldnames(s);
        for k=1:length(f)
            pa_matlab.detector.(f{k}){j} = s.(f{k});        
            if (j==length(ids_dete) && isnumeric(pa_matlab.detector.(f{k}){1}))
                pa_matlab.detector.(f{k}) = squeeze(reshape(cell2mat(pa_matlab.detector.(f{k})), [size(pa_matlab.detector.(f{k}){1}) length(ids_dete)]));
            end
        end
    end
    
    ids_illu = fieldnames(pa.meta_data_device.illuminators);
    for j=1:length(ids_illu)
        s = pa.meta_data_device.illuminators.(ids_illu{i});
        f = fieldnames(s);
        for k=1:length(f)
            pa_matlab.illuminators.(f{k}){j} = s.(f{k});        
            if (j==length(ids_illu) && isnumeric(pa_matlab.illuminators.(f{k}){1}))
                pa_matlab.illuminators.(f{k}) = squeeze(reshape(cell2mat(pa_matlab.illuminators.(f{k})), [size(pa_matlab.illuminators.(f{k}){1}) length(ids_illu)]));
            end
        end
    end
    
    % save the structure with 26 field
    save([file(i).name(1:end-5) '.mat'], 'pa_matlab');
end

