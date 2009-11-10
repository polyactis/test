/*
 * sort_vardata.cpp
 *
 *  Created on: Oct 18, 2009
 *      Author: dzmagus
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int get_pos(string line)
{
	int chrend, posend;
	string chr, pos;
	int chri, posi; //chr*100,000,000 + pos
    chrend = line.find(",");
    posend = line.find(",",chrend+1);
    chr = line.substr(0,chrend);
    pos = line.substr(chrend+1, posend-chrend-1);
    stringstream sschr(chr);
    stringstream sspos(pos);
    sschr >> chri;	// cast string chr into integer "chri"
    sspos >> posi;
    return chri*100000000+posi; // adding one more 0 will prevent segmentation error but why...
}

bool compare_lines(string i, string j)
{
	//cout << ""; // Somehow this line prevents a segmentation error... which I do not understand at all!
	return (get_pos(i)<get_pos(j));
}

int main(int argc, char *argv[]) {
	string line;
	string filename;
	bool header;
	string headerline;
	vector<string> lines;
	vector<string>::iterator it;

	// Reading parameters
	if (argc != 3)
	{
		cerr << "Incorrect number of arguments: " << argc << endl << "Usage: ./sort_vardata [filename] [0 for no header line] [> outputfile]" << endl;
		return 0;
	}
	filename = argv[1];
	if (!strcmp(argv[2],"0")) header = false;
	else header = true;

	// Opening file and reading entries
	ifstream finput(filename.c_str());
	if (finput.is_open())
	{
		if (header == true) getline(finput,headerline);
	    while (! finput.eof() )
	    {
	      getline (finput,line);
	      if (!line.empty()) lines.push_back(line);
	    }
	    finput.close();
	}
	else cerr << "Unable to open file";

	// Sorting
	sort(lines.begin(),lines.end(),compare_lines);

	// Outputing
	if (header == true) cout << headerline << endl;
	for (it=lines.begin(); it!=lines.end(); ++it) cout << *it << endl;
}
