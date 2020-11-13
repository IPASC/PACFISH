% read with a given file in Matlab
path = '../';
filename = 'demodata';
file = [path filename];

% Create an instance of the class
inst = ipasc_tool(file);

% test of a given function
inst.visualize_device