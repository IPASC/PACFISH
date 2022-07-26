function out = check_egality(a, b)
out = 0;
f = fieldnames(a);
if (length(f)~=length(fieldnames(b)))
    out = 1;
    disp('the number of fields are not the same in the two structures');
    return
end

for i=1:length(f)
    t1 = getfield(a, f{i});
    t2 = getfield(b, f{i});
    if (isstruct(t1))
        out = out + check_egality(t1, t2);
    else
        out = out + compare_field(t1, t2);
    end
end


return


function out = compare_field(a, b)
    if (isstring(a))
        a = char(a);
    end
    if (isstring(b))
        b = char(b);
    end
    out = max(max(max(abs(a-b))));
return