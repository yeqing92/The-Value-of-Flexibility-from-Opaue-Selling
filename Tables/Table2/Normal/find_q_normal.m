function [p0,q] = find_q_normal(ave,std,N,p,delta,k)
% po = fraction of no purchase
% p1 = fraction of buying opaque product
% q = p1/(1-p0)
% [a,b] the interval of valuation
% N products with price p, discount for k-opaque product is delta
p0 = zeros(1,length(delta));
p1 = zeros(1,length(delta));

step = 20000;
for i = 1:step
v = ave+ std.*randn(N,1) ;% valuation 
v = sort(v,'descend');
V = v(1:k);
temp1 = v(1)-p;
temp2 = mean(V)-p+delta; % normal-AVE

%if (temp1<0)&&(temp2<0)
    p0 = p0+1.*(temp1<=0).*(temp2<=0);
%elseif (temp2>=temp1)
    p1 = p1+1.*(temp2>=temp1).*(temp2>0);
%end
end
p0 = p0./step;
p1= p1./step;
q = p1./(1-p0);
end