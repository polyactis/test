#problems of chapter 5, page 253
#no 5, 6
def cal_next_freq(p,w_vector):
	q = 1-p
	w_avg = w_vector[0]*p*p+2*p*q*w_vector[1]+q*q*w_vector[2]
	new_p = (w_vector[0]*p*p + w_vector[1]*p*q)/w_avg	
	return new_p, new_p-p

w_vector = [1,0.9,0.6]
def draw_new_p_vs_p(w_vector):
	import pylab
	p_ls = pylab.arange(0,1,0.01)
	new_p_ls = []
	for old_p in p_ls:
		new_p_ls.append(cal_next_freq(old_p, w_vector)[0])
	pylab.clf()
	pylab.plot(p_ls, p_ls, 'r')
	pylab.plot(p_ls, new_p_ls)
	pylab.show()


draw_new_p_vs_p(w_vector)


def draw_delta_p_vs_p(w_vector):
	import pylab
	delta_p_ls = []
	for old_p in p_ls:
		delta_p_ls.append(cal_next_freq(old_p, w_vector)[1])
	pylab.clf()
	pylab.plot(p_ls, delta_p_ls)
	pylab.show()


draw_delta_p_vs_p(w_vector)


w_vector = [0.300, 1, 0.7]
draw_new_p_vs_p(w_vector)

