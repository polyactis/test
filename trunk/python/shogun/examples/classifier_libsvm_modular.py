#!/usr/bin/env python

"""
# In this example a two-class support vector machine classifier is trained on a
# toy data set and the trained classifier is used to predict labels of test
# examples. As training algorithm the LIBSVM solver is used with SVM
# regularization parameter C=1 and a Gaussian kernel of width 2.1 and the
# precision parameter epsilon=1e-5. The example also shows how to retrieve the
# support vectors from the train SVM model.
# 
# For more details on LIBSVM solver see http://www.csie.ntu.edu.tw/~cjlin/libsvm/
"""
def libsvm ():
	print 'LibSVM'

	from shogun.Features import RealFeatures, Labels
	from shogun.Kernel import GaussianKernel
	from shogun.Classifier import LibSVM

	feats_train=RealFeatures(fm_train_real)
	feats_test=RealFeatures(fm_test_real)
	width=2.1
	kernel=GaussianKernel(feats_train, feats_train, width)

	C=1
	epsilon=1e-5
	labels=Labels(label_train_twoclass)

	svm=LibSVM(C, kernel, labels)
	svm.set_epsilon(epsilon)
	svm.train()
	print "True labels:"
	print label_train_twoclass
	print label_train_twoclass>0
	
	print "Labels predicted for the training data"
	kernel.init(feats_train, feats_train)
	labels = svm.classify().get_labels()
	print labels>0
	
	
	print "Labels predicted for the testing data"
	kernel.init(feats_train, feats_test)
	labels = svm.classify().get_labels()
	print labels>0
	
	sv_idx=svm.get_support_vectors()
	alphas=svm.get_alphas()

if __name__=='__main__':
	from tools.load import LoadMatrix
	lm=LoadMatrix()
	fm_train_real=lm.load_numbers('../data/fm_train_real.dat')
	fm_test_real=lm.load_numbers('../data/fm_test_real.dat')
	label_train_twoclass=lm.load_labels('../data/label_train_twoclass.dat')
	libsvm()
