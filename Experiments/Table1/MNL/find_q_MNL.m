function [p0,q] = find_q_MNL(ave,s,N,p,delta,k)
% po = fraction of no purchase
% p1 = fraction of buying opaque product
% q = p1/(1-p0)
% [a,b] the interval of valuation
% N products with price p, discount for k-opaque product is delta

%beta= std *sqrt(6)/pi;
%mu =  0.5772 * beta;
%mu =0;

p0 = zeros(1,length(delta));
p1 = zeros(1,length(delta));
step = 100000;
%step = 10;
%Gumbel =  -evrnd(0,beta,N,step);
valuation = random('logistic', ave,s,[N,step]);
for i = 1:step
%v = a+(b-a).*rand(N,1) ;% valuation 
%v = ave + evrnd(mu,beta, N,1);
v = valuation(:,i);

v = sort(v,'descend');
V = v(1:k);

temp1 = v(1)-p;
temp2 = mean(V)-p+delta;  % risk_neutral
p0 = p0+1.*(temp1<=0).*(temp2<=0);
p1 = p1+1.*(temp2>temp1).*(temp2>0);

end
p0 = p0./step;
p1= p1./step;
q = p1./(1-p0);
end