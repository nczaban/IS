clear all;
clc;

M = csvread("gameSims.csv");
turnCounter = M(:,3);
finalHealth = M(:,1:2);
[gameNums, gameLength] = size(M);
utility = zeros(gameNums,1);
for i=1:gameNums
    utility(i) = finalHealth(i,1)-finalHealth(i,2);
end
clearvars i

for i=1:gameNums
    