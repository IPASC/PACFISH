function ipasc_tool = read_ipasc(varargin)
%% manage the input file
if (nargin==0)
    path = '../';
    filename = 'demodata';
    file = [path filename];
else
    file = varargin{1};
end
[~, ~, ext] = fileparts(file);
if (isempty(ext))
    file = [file '.hdf5'];
end
fprintf('\n\n\n**********************\n\n\tTry to read %s file\n\n', file);

%% Extract one or more datasets 
% information
h5_info = h5info(file);

% read one or several dataset
for i=1:length(h5_info.Datasets)
    ipasc_tool.(h5_info.Datasets(i).Name) = h5read(file, ['/' h5_info.Datasets(i).Name]);
end


%% Extract the others dataset in the h5 file
ipasc_tool = extract_field(ipasc_tool, file, '/', h5_info);


% %% Try to display something...
% delete(gcf)
% for i=1:size(ipasc_tool.binary_time_series_data,1)
%      subplot(3,5,i); imagesc(rf2log(squeeze(ipasc_tool.binary_time_series_data(i,:,:)), 120)); 
% end



function S = extract_field(S, file, location, struc)
for i=1:length(struc.Groups)
    name = struc.Groups(i).Name;
    k=find(name=='/');
    name = name(k(end)+1:end);
    if (isempty(struc.Groups(i).Groups))
        % I create the current structure level
        S.(name) = struct();
        for j=1:length(struc.Groups(i).Datasets)
            % I read the dataset inside
            S.(name).(struc.Groups(i).Datasets(j).Name) = h5read(file, [location name '/' struc.Groups(i).Datasets(j).Name]);
        end
    else
        S.(name) = struct();
        S.(name) = extract_field(S.(name), file, [location name '/' ], struc.Groups(i));
    end
end
