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
clear s i j x

g=1;
t=1;
o=1;
e=1;
m=1;

for i=1:size(finalHP)
    if finalHP(i,1)>finalHP(i,2)
        finalHP(i,4)=0;
    else
        finalHP(i,4)=1;
    end
end

for i=1:size(finalHP)
    if txt(i,1)=="Goblin"
        goblinWins(g,1)=finalHP(i, 4);
        g=g+1;
    end
    if txt(i, 1)=="Troll"
        trollWins(t,1)=finalHP(i, 4);
        t=t+1;
    end
    if txt(i, 1)=="Orc"
        orcWins(o,1)=finalHP(i, 4);
        o=o+1;
    end
    if txt(i, 1)=="Elf"
        elfWins(e,1)=finalHP(i, 4);
        e=e+1;
    end
    if txt(i, 1)=="Magician"
        magicianWins(m,1)=finalHP(i, 4);
        m=m+1;
    end
end
clear g o t e m

counts = hist(goblinWins);
pie(counts)
pause
counts = hist(trollWins);
pie(counts)
pause
counts = hist(orcWins);
pie(counts)
pause
counts = hist(elfWins);
pie(counts)
pause
counts = hist(magicianWins);
pie(counts)
