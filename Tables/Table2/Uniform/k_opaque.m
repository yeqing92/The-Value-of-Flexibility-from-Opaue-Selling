function [E_R,ER2] = k_opaque( q,N,c,cycle,k)
% 2-opaque, k=2
level = c./10;
R = zeros(level,cycle);
% r number of replenishments

for r = 1:cycle
    n = 0;
    inv_level = 1;
    number = zeros(N,1);
    while(inv_level<=level)
        %[max_inv,max_0] = min(number);
        % opaque policy
        U = rand;
        if (U>=1-q)
            k_choice = randperm(N,k);
            k_number = number(k_choice);
            [max_inv,max_0] = min(k_number);
            i = k_choice(max_0);
        else
            i = randi(N);
        end
        number(i) = number(i)+1;
        
        max_number = max(number);
        n = n+1;
        % check replenishment
        if(max_number == inv_level*10)
            R(inv_level,r) = n;
            inv_level= inv_level+1;
        end
    end
end

E_R = mean(R');
R2 = R.^2;
ER2 = mean(R2');
end