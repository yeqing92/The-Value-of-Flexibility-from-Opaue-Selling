load('ER_K.mat')
load('ER2_K.mat')
load('ER2.mat')
load('ER.mat')


new_ER = ER;
new_ER2 = ER2;
new_ER2K = ER2K;
new_ERK = ERK;

std = 10;
c=100;
c_index = c./10;

h = 1;
lambda = 50;
ave = 100;
pur_cost = 50;
N = 5;
delta = 0:0.1:11;
m = length(delta);
price =95:0.1:110;
n = length(price);

p0 = zeros(n,m);
q = zeros(n,m);

p0_2 = zeros(n,m);
q_2 = zeros(n,m);

beta= std *sqrt(3)/pi;

fprintf('Progress:\n');
fprintf(['\n' repmat('\b|\n',1,n) '\n\n']);

step = 100000;
valuation = random('logistic', ave,beta,[N,step]);
k = N; % generate price and q table for n opaque product
for i = 1:n
    p = price(i);
    p_0 = zeros(1,length(delta));
    p_1 = zeros(1,length(delta));

    for j = 1:step
        v = valuation(:,j);
        v = sort(v,'descend');
        V = v(1:k);

        temp1 = v(1)-p;
        temp2 = mean(V)-p+delta;  % risk_neutral
        p_0 = p_0+1.*(temp1<=0).*(temp2<=0);
        p_1 = p_1+1.*(temp2>temp1).*(temp2>0);
    end
    p_0 = p_0./step;
    p0(i,:) = p_0;
    p_1= p_1./step;
    q(i,:)= p_1./(1-p_0);
    
    fprintf('\b|\n');
end

k = 2; % generate price and q table for 2 opaque product
for i = 1:n
    p = price(i);
    p_0 = zeros(1,length(delta));
    p_1 = zeros(1,length(delta));

    for j = 1:step
        v = valuation(:,j);
        v = sort(v,'descend');
        V = v(1:k);

        temp1 = v(1)-p;
        temp2 = mean(V)-p+delta;  % risk_neutral
        p_0 = p_0+1.*(temp1<=0).*(temp2<=0);
        p_1 = p_1+1.*(temp2>temp1).*(temp2>0);
    end
    p_0 = p_0./step;
    p0_2(i,:) = p_0;
    p_1= p_1./step;
    q_2(i,:)= p_1./(1-p_0);
    
    fprintf('\b|\n');
end
