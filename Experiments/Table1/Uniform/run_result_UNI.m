std = 10;

%load('new_q_2.mat')
%load('new_q.mat')
%load('new_p0_2.mat')
%load('new_p0.mat')
%load('new_ERK.mat')
%load('new_ER2K.mat')
%load('new_ER2.mat')
%load('new_ER.mat')
load('ER_K.mat')
load('ER2_K.mat')
load('ER2.mat')
load('ER.mat')


new_ER = ER;
new_ER2 = ER2;
new_ER2K = ER2K;
new_ERK = ERK;

c=100;

%c_index = (c-10)./2+1;
c_index = c./10;

h = 1;
lambda = 50;
ave = 100;
pur_cost = 50;
N = 5;
a = ave - sqrt(3).*std;
b = ave + sqrt(3).*std;
%delta = 1:0.1:9;
%m = length(delta);
%p =103:0.1:105;
%n = length(p);
delta = 0:0.1:8;
m = length(delta);
price = 102:0.1:105;
n = length(price);
p0 = zeros(n,m);
q = zeros(n,m);
p0_2 = zeros(n,m);
q_2 = zeros(n,m);



fprintf('Progress:\n');
fprintf(['\n' repmat('\b|\n',1,n) '\n\n']);
for i = 1:n
    p = price(i);
    [p0(i,:),q(i,:)] = find_q(a,b,N,p,delta,N);
    [p0_2(i,:),q_2(i,:)] = find_q(a,b,N,p,delta,2);
    fprintf('\b|\n');
end




q_value = 0:0.01:0.5;

k = [1000,5000,10000]; %%%%%%%%%%%%%%%%%

nn = length(k);
p_star = zeros(1,nn);
c_star = zeros(1,nn);
delta_star_N = zeros(1,nn);
delta_star_2 = zeros(1,nn);
Pi_star = zeros(1,nn);
Pi_star_N = zeros(1,nn);
Pi_star_2 = zeros(1,nn);
q_star_N = zeros(1,nn);
q_star_2 = zeros(1,nn);
total_cost_star = zeros(1,nn);
total_cost_star_N = zeros(1,nn);
total_cost_star_2 = zeros(1,nn);
revenue = zeros(1,nn);
revenue_N = zeros(1,nn);
revenue_2 = zeros(1,nn);
lambda_star_N = zeros(1,nn);
lambda_star_2 = zeros(1,nn);
lambda_star_trad = zeros(1,nn);


% for traditional strategy
p0_trad = ((price-a).^N./(b-a).^N)';% delta = 0
%p0_trad = 1./(1 + exp())
ER_trad = new_ER(1,c_index); % q = 0
ER2_trad = new_ER2(1,c_index); % q = 0

lambda_trad = (1-p0_trad).*lambda;
hold_trad = ((2.*N.*c+1).*ER_trad-ER2_trad).*h./(2.*ER_trad); % holding cost per time unit for traditional strategy
holding_trad = mtimes(ones(length(lambda_trad),1) ,hold_trad);

for i = 1:nn
K = k(i);
%K = (i-1)*100+500;
% find p*
% find c* for every p
cost_trad = mtimes(lambda_trad,K./ER_trad)+holding_trad; % matrix
%[cost_trad_star,I] = min(cost_trad,[],2);
%c_trad = (I-1).*2+10;
c_trad = c;

Pi_trad = (price-pur_cost)'.*lambda_trad-cost_trad;
[Pi_star(i),J]=max(Pi_trad);

%find best price
p_star(i) = price(J);
c_star(i) = c;
lambda_star_trad(i) = lambda_trad(J);
total_cost_star(i) = cost_trad(J);
revenue(i) = (p_star(i))*lambda_trad(J);

% compute revenue for N and 2-opaque using p_star and c_star for K fixed
% find the best delta and corresponding q
lambda_N = lambda.*(1-p0(J,:));
q_value_N =  q(J,:);

lambda_2 = lambda.*(1-p0_2(J,:));
q_value_2 =  q_2(J,:);

% find q index
% index of c is I(J)
index_q = round(q_value_N.*100)+1;
index_q = index_q.*(index_q<=51)+51.*(index_q>51);

index_q2 = round(q_value_2.*100)+1;
index_q2 = index_q2.*(index_q2<=51)+51.*(index_q2>51);

er_N = new_ER(index_q,c_index);
er2_N =new_ER2(index_q,c_index);
er_2 = new_ERK(index_q2,c_index);
er2_2 =new_ER2K(index_q2,c_index);

ordering =lambda_N'.*K./er_N;
holding = ((2.*N.*c_star(i)+1).*er_N-er2_N).*h./(2.*er_N);
total_cost_N = ordering + holding;
Pi_N = (1-q_value_N).*lambda_N.*(p_star(i)-pur_cost)+q_value_N.*lambda_N.*(p_star(i)-delta-pur_cost)-total_cost_N';
[Pi_star_N(i),index] = max(Pi_N);
delta_star_N(i) = delta(index);
q_star_N(i) = q_value_N(index);
lambda_star_N(i) = lambda_N(index);
total_cost_star_N(i) = total_cost_N(index);
revenue_N(i) = (1-q_value_N(index)).*lambda_N(index).*(p_star(i))+q_value_N(index).*lambda_N(index).*(p_star(i)-delta(index));

ordering =lambda_2'.*K./er_2;
holding = ((2.*N.*c_star(i)+1).*er_2-er2_2).*h./(2.*er_2);
total_cost_2 = ordering + holding;
Pi_2 = (1-q_value_2).*lambda_2.*(p_star(i)-pur_cost)+q_value_2.*lambda_2.*(p_star(i)-delta-pur_cost)-total_cost_2';
[Pi_star_2(i),index] = max(Pi_2);
delta_star_2(i) = delta(index);
q_star_2(i) = q_value_2(index);
lambda_star_2(i) = lambda_2(index);
total_cost_star_2(i) = total_cost_2(index);
revenue_2(i) = (1-q_value_2(index)).*lambda_2(index).*(p_star(i))+q_value_2(index).*lambda_2(index).*(p_star(i)-delta(index));
end

cost_unit_trad = total_cost_star./lambda_star_trad;
cost_unit_N = total_cost_star_N./lambda_star_N;
cost_unit_2 = total_cost_star_2./lambda_star_2;

cost_saving_N = 100.*cost_unit_N./cost_unit_trad -100;
cost_saving_2 = 100.*cost_unit_2./cost_unit_trad -100;

Profit_trad = Pi_star./lambda_star_trad;
Profit_N = Pi_star_N./lambda_star_N;
Profit_2 = Pi_star_2./lambda_star_2;

profit_increase_N =  100.*Profit_N./Profit_trad - 100;
profit_increase_2 =  100.*Profit_2./Profit_trad - 100;

figure(1)
subplot(2,2,1)
plot(k,100.*Pi_star_N./Pi_star-100,'r-','linewidth',2)
hold on
plot(k,100.*Pi_star_2./Pi_star-100,'b-','linewidth',2)
ylabel('% Change in Profit')
xlabel('Ordeing Cost')
legend('N-opaque', '2-opaque')


subplot(2,2,2)
plot(k,q_star_N.*100,'r-','linewidth',2)
hold on
plot(k,q_star_2.*100,'b-','linewidth',2)
ylabel('% Opaque Customers')
xlabel('Ordeing Cost')

subplot(2,2,3)
hold on
yyaxis left
plot(k,100.*total_cost_star_N./total_cost_star-100,'r-','linewidth',2)
ylabel('% Change in Cost')
xlabel('Ordeing Cost')
plot(k,100.*total_cost_star_2./total_cost_star-100,'b-','linewidth',2)
yyaxis right
plot(k,100.*revenue_N./revenue-100,'r--','linewidth',2)

plot(k,100.*revenue_2./revenue-100,'b--','linewidth',2)
ylabel('% Change in Revenue')


hold off
% %subplot(4,2,6)
% 
% %plot(k,c_star,'r-','linewidth',2)
% %ylabel('c^*')
% %xlabel('K')
% 
% %subplot(4,2,8)
% %plot(k,p_star,'r-','linewidth',2)
% %ylabel('p^*')
% %xlabel('K')
% 
subplot(2,2,4)
plot(k,100.*delta_star_N./p_star,'r-','linewidth',2)
hold on
plot(k,100.*delta_star_2./p_star,'b-','linewidth',2)
ylabel('% of Discount')
xlabel('Ordeing Cost')


%subplot(4,2,5)
%plot(k,100.*revenue_N./revenue-100,'r-','linewidth',2)
%hold on
%plot(k,100.*revenue_2./revenue-100,'b-','linewidth',2)
%ylabel('% Change in Revenue')
%xlabel('K')

Result_table = zeros(nn,12);
Result_table(:,1) = (100.*delta_star_N./p_star)';
Result_table(:,2) = (100.*delta_star_2./p_star)';
Result_table(:,3) = (q_star_N.*100)';
Result_table(:,4) = (q_star_2.*100)';
Result_table(:,5) = (cost_saving_N)';
Result_table(:,6) = (cost_saving_2)';
Result_table(:,7) = (lambda_star_N./lambda_star_trad*100-100)';
Result_table(:,8) = (lambda_star_2./lambda_star_trad*100-100)';
Result_table(:,9) = (100.*revenue_N./revenue-100)'
Result_table(:,10) = (100.*revenue_2./revenue-100)'
Result_table(:,11) = (100.*Pi_star_N./Pi_star-100)'
Result_table(:,12) = (100.*Pi_star_2./Pi_star-100)'
Result_table