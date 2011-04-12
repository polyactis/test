function [value]=KK2011SpringProjectFunction(epsilon, max_n, max_m)

% comp_Estep_SBL Implements the E_step of the SBL algorithm
% It can be used either in the multiple sample or the single sample
% approach.

value = calculateFirstTerm(epsilon, max_n);

value = value + calculateFirstTerm(epsilon, max_m);

for n=1:max_n
	for m=1:max_m
		x = 2*sqrt(pi)*n*epsilon;
		y = 2*sqrt(pi)*m*epsilon;
		z = sqrt(x*x + y*y);
		value = value + 8*sin(z)*Besselj(1, z)/((m*m+n*n)*pi*pi*z);
	end
end
disp(value);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [value] =calculateFirstTerm(epsilon, max_n)

value = 0;
for n=1:max_n
  x = 2*sqrt(pi)*n*epsilon;
  value = value + 4*sin(x)*Besselj(1, x)/(n*n*pi*pi*x);
end

