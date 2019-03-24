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
b=1;
k=1;

for i=1:size(finalHP)
    if finalHP(i,1)>finalHP(i,2)
        finalHP(i,3)=0;
    else
        finalHP(i,3)=1;
    end
end

%% Create pie charts for each AI's win rate
for i=1:size(finalHP)
    if txt(i,1)=="Goblin"
        goblinWins(g,1)=finalHP(i, 3);
        g=g+1;
    end
    if txt(i, 1)=="Troll"
        trollWins(t,1)=finalHP(i, 3);
        t=t+1;
    end
    if txt(i, 1)=="Orc"
        orcWins(o,1)=finalHP(i, 3);
        o=o+1;
    end
    if txt(i, 1)=="Elf"
        elfWins(e,1)=finalHP(i, 3);
        e=e+1;
    end
    if txt(i, 1)=="Magician"
        magicianWins(m,1)=finalHP(i, 3);
        m=m+1;
    end
    if txt(i, 1)=="Beserker"
        beserkerWins(b, 1)=finalHP(i, 3);
        b=b+1;
    end
    if txt(i, 1)=="Knight"
        knightWins(k, 1)=finalHP(i, 3);
        k=k+1;
    end
end
clear g o t e m i b k

% counts = hist(goblinWins);
% pie(counts)
% pause
% counts = hist(trollWins);
% pie(counts)
% pause
% counts = hist(orcWins);
% pie(counts)
% pause
% counts = hist(elfWins);
% pie(counts)
% pause
% counts = hist(magicianWins);
% pie(counts)
% pause
% counts = hist(beserkerWins);
% pie(counts)
% pause
% counts = hist(knightWins);
% pie(counts)
% pause

%% Analyze the proportion of player actions per game
[x, y]=size(txt);
actionCounts = zeros(x, 4);
for i=1:x
    for j=5:y
        if mod(j,2)==1
            if txt(i,j)=="A"
                actionCounts(i,1)=actionCounts(i,1)+1;
        
            elseif txt(i,j)=="S"
                actionCounts(i,2)=actionCounts(i,2)+1;
        
            elseif txt(i,j)=="P"
                actionCounts(i,3)=actionCounts(i,3)+1;
        
            elseif txt(i,j)=="H"
                actionCounts(i,4)=actionCounts(i,4)+1;
            end
        end
    end
end

g=1;
t=1;
o=1;
e=1;
m=1;
b=1;
k=1;

for i=1:size(finalHP)
    if txt(i,1)=="Goblin"
        antiGoblinActions(g,:)=actionCounts(i,:);
        g=g+1;
    end
    if txt(i, 1)=="Troll"
        antiTrollActions(t,:)=actionCounts(i,:);
        t=t+1;
    end
    if txt(i, 1)=="Orc"
        antiOrcActions(o,:)=actionCounts(i,:);
        o=o+1;
    end
    if txt(i, 1)=="Elf"
        antiElfActions(e,:)=actionCounts(i,:);
        e=e+1;
    end
    if txt(i, 1)=="Magician"
        antiMagicianActions(m,:)=actionCounts(i,:);
        m=m+1;
    end
    if txt(i, 1)=="Beserker"
        antiBeserkerActions(b,:)=actionCounts(i,:);
        b=b+1;
    end
    if txt(i, 1)=="Knight"
        antiKnightActions(k,:)=actionCounts(i,:);
        k=k+1;
    end
end
clear g o t e m i j x y b k

% [x,y] = size(antiGoblinActions);
% for i=1:y
%     A(i) = sum(antiGoblinActions(:,i));
% end
% pie(A)
% pause
% 
% [x,y] = size(antiTrollActions);
% for i=1:y
%     A(i) = sum(antiTrollActions(:,i));
% end
% pie(A)
% 
% [x,y] = size(antiOrcActions);
% for i=1:y
%     A(i) = sum(antiOrcActions(:,i));
% end
% pie(A)
% 
% [x,y] = size(antiElfActions);
% for i=1:y
%     A(i) = sum(antiElfActions(:,i));
% end
% pie(A)
% pause
% 
% [x,y] = size(antiMagicianActions);
% for i=1:y
%     A(i) = sum(antiMagicianActions(:,i));
% end
% pie(A)
% 
% [x,y] = size(antiBeserkerActions);
% for i=1:y
%     A(i) = sum(antiBeserkerActions(:,i));
% end
% pie(A)
% pause
% 
% [x,y] = size(antiKnightActions);
% for i=1:y
%     A(i) = sum(antiKnightActions(:,i));
% end
% pie(A)

%% Analyze remaining HP for games where Player won
g=1;
t=1;
o=1;
e=1;
m=1;
b=1;
k=1;

for i=1:size(finalHP)
    if txt(i,1)=="Goblin"
        goblinHP(g,1:2)=finalHP(i, 1:2);
        g=g+1;
    end
    if txt(i, 1)=="Troll"
        trollHP(t,1:2)=finalHP(i, 1:2);
        t=t+1;
    end
    if txt(i, 1)=="Orc"
        orcHP(o,1:2)=finalHP(i, 1:2);
        o=o+1;
    end
    if txt(i, 1)=="Elf"
        elfHP(e,1:2)=finalHP(i, 1:2);
        e=e+1;
    end
    if txt(i, 1)=="Magician"
        magicianHP(m, 1:2)=finalHP(i, 1:2);
        m=m+1;
    end
    if txt(i, 1)=="Beserker"
        beserkerHP(b, 1:2)=finalHP(i, 1:2);
        b=b+1;
    end
    if txt(i, 1)=="Knight"
        knightHP(k, 1:2)=finalHP(i, 1:2);
        k=k+1;
    end
end

[x,y] = size(goblinHP);
avgGoblinHP = sum(goblinHP(:, 1)) / x;
[x,y] = size(trollHP);
avgTrollHP = sum(trollHP(:, 1)) / x;
[x,y] = size(orcHP);
avgOrcHP = sum(orcHP(:, 1)) / x;
[x,y] = size(elfHP);
avgElfHP = sum(elfHP(:, 1)) / x;
[x,y] = size(magicianHP);
avgMagicianHP = sum(magicianHP(:, 1)) / x;
[x,y] = size(beserkerHP);
avgBeserkerHP = sum(beserkerHP(:, 1)) / x;
[x,y] = size(knightHP);
avgKnightHP = sum(knightHP(:, 1)) / x;

clear g o t e m i b k