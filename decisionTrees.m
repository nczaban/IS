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

p1Wins = zeros(gameNums, 1);
for i=1:gameNums
    if(utility(i,1) > 0)
        p1Wins(i) = 1;
    else
        p1Wins(i) = 0;
    end
end
testData = M(:,3:end);
T = fitctree(testData(1:4000,:), p1Wins(1:4000));
view(T, 'Mode', 'Graph')

P=predict(T, testData(4001:4500, :));
mse=sum((p1Wins(4001:4500)-P).^2)/length(p1Wins(4001:4500))
