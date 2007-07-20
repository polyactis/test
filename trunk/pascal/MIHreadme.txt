/enj

This directory contains a very basic and user non-friendly
program to perform MIH estimates of the two last outcrossing rates
of a population. (Jerome Enjalbert and Jacques L.david, Genetics dec. 2000)
Other programs used to perform population simulations and lod score
will be soon integrated.

\exemple : file giving the format of the input data file:
             
	0.06         : a priori last outcrossing rate t0-test
	0.06         : a priori mean previous outcrossing rate tp-test -> likelihood test calculated  
	3  10        : number of populations and number of locus
	pop1         : name of first pop.
	77	     : individual numb. in first pop
	pop2
        78
	pop3
        78
	ba381 3	     : name of the first locus, and its max. allele number
	65B 2        : name of the second locus, and its max. allele number...
	...
	bb178 2
	UCB82 2
	1  1  2  2  0  0  1  1  2  2  1  1  1  1  1  1  1  1  1  1 
	2  2  1  1  1  1  2  2  2  2  1  1  1  1  1  1  1  1  1  1  
        Genotype coding, one individual per line, all loci beeing ordered 
        as in the locus definition, missing values => [0]


\MIHdeep2.exe : turbopascal executable performing the MIH estimate of T0+Tp,
                and produce two output files: 
                    - #input#.ph where are reported the ML estimates and their likelihood
                    - #input#.fr containing the allelic frequencies of populations


\MIHdeep2.pas : souce of previous executable 
		
