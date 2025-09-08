function [E_R, ER2] = N_opaque(q,N,c,cycle)
level = c./10;
R = zeros(level,cycle);

%number = zeros(N,1);%  number of customers that choose product i

% number of customers in the cycle
% r number of replenishments

for r = 1:cycle
    
    n = 0; 
    inv_level = 1;
    number = zeros(N,1);
    while(inv_level<=level)
        [max_inv,max_0] = min(number);
        % opaque policy
        U = rand;
        if (U>=1-q)
            i = max_0;
        else
            i = randi(N);
        end
        number(i) = number(i)+1;
        
        max_number = max(number);
        n = n+1;
        % check replenishment
        if(max_number == inv_level.*10)
            %ordering = ordering + K;
            R(inv_level,r) = n;
            inv_level= inv_level+1;
        end
    end

end

E_R = mean(R');
R2 = R.^2;
ER2 = mean(R2');
end