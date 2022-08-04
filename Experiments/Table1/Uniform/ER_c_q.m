cycle = 100000;
col = 50;
r = 50;
k=2;
N = 5;   
c=500; % compute ER ER2 for all c = 10: 500
% c is the order up to level S in the paper
ER = zeros(r+1,col);
ER2 = zeros(r+1,col);
ERK = zeros(r+1,col);
ER2K = zeros(r+1,col);

fprintf('Progress:\n');
fprintf(['\n' repmat('.',1,r+1) '\n\n']);

for i = 1:(r+1)
        [ER(i,:),ER2(i,:)] = N_opaque((i-1)./100,N,c,cycle);
        [ERK(i,:),ER2K(i,:)] = k_opaque((i-1)./100,N,c,cycle,k);
        fprintf('\b|\n');
end
