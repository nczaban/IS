clear all;
clc;

[turnCount, txt, raw] = xlsread("gameSims3.xlsx");
aiModel = txt(:,1);
textHP = txt(:, 2:3);

for i=1:size(raw)
    for j=1:2
        s=textHP(i, j);
        s=cell2mat(s);
        s(regexp(s,'[\[\]]'))=[];
        x=str2num(s);
        finalHP(i,j)=x;
    end
end
clear s i j
