function [value]=KK2011SpringProjectFunction(epsilon, max_n, max_m)

% 2011-4-12 function to calculate values of a fomula

disp(epsilon);
disp(max_n);
disp(max_m);

epsilon = str2num(epsilon);
max_n = str2num(max_n);
max_m = str2num(max_m);

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

