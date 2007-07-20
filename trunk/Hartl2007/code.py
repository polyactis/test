#2007-06-20 problems of chapter 5, page 253
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

#2007-06-26 chapter 7, problems, No 11
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
seq1 = Seq('CTGACCAAAATCGCCGCCGTAGCTGAAGACGGTGAACCATGCGTTACCTATATTGGTGCC', IUPAC.unambiguous_dna)
seq2 = Seq('CTGAAGCAGATCGCGGCGGTTGCTGAAGACGGTGAGCCGTGTGTGACTTATATAGGTGCC', IUPAC.unambiguous_dna)
from Bio import Translate
standard_translator = Translate.unambiguous_dna_by_id[1]
seq1_aa = standard_translator.translate(seq1)
seq2_aa = standard_translator.translate(seq2)

no_of_nts = len(seq1)
no_of_diff_nts = 0.0
for i in range(no_of_nts):
	if seq1[i]!=seq2[i]:
		no_of_diff_nts += 1

print "number of nt differences per nt site is", no_of_diff_nts/no_of_nts

no_of_aas = len(seq1_aa)
no_of_diff_aas = 0.0
for i in range(no_of_aas):
	if seq1_aa[i]!=seq2_aa[i]:
		no_of_diff_aas += 1

print "number of aa differences per aa site is", no_of_diff_aas/no_of_aas

aa2degeneracy = {} 
for codon, aa in standard_translator.table.forward_table.iteritems():
	if aa not in aa2degeneracy:
		aa2degeneracy[aa] = 0
	aa2degeneracy[aa] += 1


for aa, degeneracy in aa2degeneracy.iteritems():
	print standard_translator.table.back_table[aa], degeneracy


#the two loops above reveal that there're 3 AAs (Ser, Arg, Leu) with 6 triplets. so aa2degeneracy can't be used. This exposes a potential problem in synonymous and  non-synonymous calculations. (written down in the margin of page 341)

triplet2aa = standard_translator.table.forward_table
triplet2degeneracy = {}
nt_ls = ['A', 'C', 'G', 'T']
for a1 in nt_ls:
	for a2 in nt_ls:
		#1st, construct a local(for 4 triplets) degeneracy dictionary
		local_aa2degeneracy = {}
		triplet_ls = []
		for a3 in nt_ls:
			triplet = a1+a2+a3
			if triplet in triplet2aa:	#stop codons are not in triplet2aa
				triplet_ls.append(triplet)
				aa = triplet2aa[triplet]
				if aa not in local_aa2degeneracy:
					local_aa2degeneracy[aa] = 0
				local_aa2degeneracy[aa] += 1
		#2nd, write it to triplet2degeneracy
		for triplet in triplet_ls:
			aa = triplet2aa[triplet]
			triplet2degeneracy[triplet] = local_aa2degeneracy[aa]


no_of_syn_nts = 0.0
no_of_nonsyn_nts = 0.0
no_of_diff_syn_nts = 0.0
no_of_diff_nonsyn_nts = 0.0
for i in range(no_of_aas):
	triplet1 = seq1[3*i:3*(i+1)].tostring()
	triplet2 = seq2[3*i:3*(i+1)].tostring()
	degeneracy = triplet2degeneracy[triplet2]	#this is only based on sequence 1
	syn_coeff = (degeneracy-1.0)/3	#how to split the 3rd nucleotide between synonymous and non-synonymous
	nonsyn_coeff = (4.0-degeneracy)/3
	no_of_syn_nts += syn_coeff
	no_of_nonsyn_nts += (2+nonsyn_coeff)
	if triplet1[0]!=triplet2[0]:
		no_of_diff_nonsyn_nts += 1
	if triplet1[1]!=triplet2[1]:
		no_of_diff_nonsyn_nts += 1
	if triplet1[2]!=triplet2[2]:	#2007-06-27 some problem here. Yang2006a has a full explanation.
		if triplet2aa[triplet1]==triplet2aa[triplet2]:
			no_of_diff_syn_nts += 1
		else:
			no_of_diff_nonsyn_nts += 1


print "no of non-synonymous substitutions per non-synonymous site is", no_of_diff_nonsyn_nts/no_of_nonsyn_nts
print "no of synonymous substitutions per synonymous site is", no_of_diff_syn_nts/no_of_syn_nts


