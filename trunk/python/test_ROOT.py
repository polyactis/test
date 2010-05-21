"""
2010-5-21
    example copied from http://root.cern.ch/viewvc/trunk/tutorials/pyroot/.\
    Run it as 'python -i test_ROOT.py'. Have to run fillrandom.py to generate data first.
"""
from ROOT import TCanvas, TFile, TPaveText
from ROOT import gROOT, gBenchmark

gROOT.Reset()
c1 = TCanvas( 'c1', 'The Fit Canvas', 200, 10, 700, 500 )
c1.SetGridx()
c1.SetGridy()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderMode(-1 )
c1.GetFrame().SetBorderSize( 5 )

gBenchmark.Start( 'fit1' )
#
# We connect the ROOT file generated in a previous tutorial
# (see begin_html <a href="fillrandom.C.html">Filling histograms with random numbers from a function</a>) end_html
#
fill = TFile( 'fillrandom.root' )

#
# The function "ls()" lists the directory contents of this file
#
fill.ls()

#
# Get object "sqroot" from the file.
#

sqroot = gROOT.FindObject( 'sqroot' )
sqroot.Print()

#
# Now fit histogram h1f with the function sqroot
#
h1f = gROOT.FindObject( 'h1f' )
h1f.SetFillColor( 45 )
h1f.Fit( 'sqroot' )

f1 = h1f.GetFunction('sqroot')
print f1.Eval(4.5)  #get the prediction at x=4.5
print f1.GetChisquare();
f1.GetParameter(0);
f1.GetParError(1);

# We now annotate the picture by creating a PaveText object
# and displaying the list of commands in this macro
#
fitlabel = TPaveText( 0.6, 0.3, 0.9, 0.80, 'NDC' )
fitlabel.SetTextAlign( 12 )
fitlabel.SetFillColor( 42 )
fitlabel.ReadFile( 'fit1_py.py' )
fitlabel.Draw()
c1.Update()
gBenchmark.Show( 'fit1' )
