#include <stdio.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_eigen.h>
#include <iostream>

int
main (void)
{
	double data[] = { 0 , 1, 1, 0,
					  1, 0, 1, 1,
					  1, 1, 0, 1,
					  0, 1, 1, 0 };

	gsl_matrix_view m
	= gsl_matrix_view_array (data, 4, 4);

	gsl_vector *eval = gsl_vector_alloc (4);
	gsl_matrix *evec = gsl_matrix_alloc (4, 4);

	gsl_eigen_symmv_workspace * w =
		gsl_eigen_symmv_alloc (4);
	//02-23-05 access the dimension of the matrix of a matrixview
	std::cout<<"dimension of matrix : "<<m.matrix.size1 <<std::endl;
	gsl_eigen_symmv (&m.matrix, eval, evec, w);
	//02-23-05 access the dimension of a matrix pointer.
	std::cout<<"dimension of matrix evec: "<<evec->size1 <<std::endl;

	gsl_eigen_symmv_free (w);

	gsl_eigen_symmv_sort (eval, evec,
						  GSL_EIGEN_SORT_VAL_ASC);

	{
		int i;

		for (i = 0; i < 4; i++)
		{
			double eval_i
			= gsl_vector_get (eval, i);
			gsl_vector_view evec_i
			= gsl_matrix_column (evec, i);

			printf ("eigenvalue = %g\n", eval_i);
			printf ("eigenvector = \n");
			gsl_vector_fprintf (stdout,
								&evec_i.vector, "%g");
		}
	}

	return 0;
}
