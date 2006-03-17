#03-13-06 R codes to use randomForest on function annotation data

library(randomForest)

#use 'correct' and 'wrong'(not 1 and 0) to denote the respone
#1 and 0 will not be regarded as factor type and randomForest does not have that option
data = read.table('/tmp/hs_fim_92m5x25bfsdfl10q0_7gf1.known', header=TRUE)
data_unknown = read.table('/tmp/hs_fim_92m5x25bfsdfl10q0_7gf1.unknown', header=TRUE)

#create two indices, one for training (2/3), one for testing (1/3)

data_1_index = c()
data_2_index = c()
for (i in seq(30484))
{
	m = runif(1)
	if  (m<=0.66)
	{
		data_1_index = c(data_1_index, i)
	}
	else
	{
		data_2_index = c(data_2_index, i)
	}
}

data.rf = randomForest(is_correct~p_value+recurrence+connectivity+cluster_size+gradient, data=data[data_1_index,],  xtest=data[data_2_index,c(1,2,3,4,5)], ytest=data[data_2_index,8])

data.rf

#another way to partition data into training and testing

ind <- sample(2, nrow(data), replace = TRUE, prob=c(0.8, 0.2))

data_ind_1.rf = randomForest(is_correct~p_value+recurrence+connectivity+cluster_size+gradient, data=data[ind==1,])
data_ind_2.pred = predict(data_ind_1.rf, data[ind==2,])
table(observed = data[ind==2, "is_correct"], predicted = data_ind_2.pred)

data.rf = randomForest(is_correct~p_value+recurrence+connectivity+cluster_size+gradient, data=data)
data_unknown.pred = predict(data.rf, data_unknown)

