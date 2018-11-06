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

for i=1:gameNums
    for j=1:gameLength
        if(M(i,j)==-100)
            p2DataStart(i,1) = j+1;
        end
    end
end

testData = M(:,3:end);
T = fitctree(testData(1:4000,:), p1Wins(1:4000));

PrunedT = prune(T, 'level', 35);
view(PrunedT, 'Mode', 'Graph')
P=predict(PrunedT, testData(4001:4500, :));
mse=sum((p1Wins(4001:4500)-P).^2)/length(P)

pause

j=1;
for i=1:gameNums
    if(testData(i, 96) > 20.5)
        trainingTurnNums(j,1) = testData(i,1);
        trainingTurnNumsSolutions(j,1) = p1Wins(i,1);
        trainingTurnNums(j,2) = 96 - p2DataStart(i,1);
        j=j+1;
    end
end

for

TwoColumnT = fitctree(trainingTurnNums(1:400,:), trainingTurnNumsSolutions(1:400));
view(TwoColumnT, 'Mode', 'Graph')
P=predict(TwoColumnT, trainingTurnNums(401:488, :));
mse=sum((trainingTurnNumsSolutions(401:488,1)-P).^2)/length(P)