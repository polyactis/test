/*
*02-23-05
*After two days, the prototype of the clustering algorithm is done. Use gsl and Boost.Graph.
*Idea is simple, get the second minimum eigen vector. Parition the vertices based on the sign
*of the each value in the vector.
*
*/

#include <boost/config.hpp>
#include <iostream>                      // for std::cout
#include <utility>                       // for std::pair
#include <boost/utility.hpp>             // for boost::tie
#include <boost/graph/subgraph.hpp>	//for boost::subgraph
#include <boost/graph/graph_traits.hpp>  // for boost::graph_traits
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/connected_components.hpp>	//for connected_components

//for parsing input file
#include <fstream>
#include <string>
#include <boost/tokenizer.hpp>
#include <boost/tuple/tuple.hpp>

#include <gsl/gsl_math.h>		//for gsl_matrix, gsl_vector stuff
#include <gsl/gsl_eigen.h>		//for gsl_eigen stuff

using namespace boost;

typedef subgraph<adjacency_list<vecS, vecS, undirectedS,
	property<vertex_name_t, int>, property<edge_index_t, int> > > Graph;
//typedef adjacency_list_traits<vecS, vecS, directedS> Traits;
typedef std::pair<int, int> Edge;
enum {A, B, C, D, E, N};
typedef graph_traits < Graph >::vertex_descriptor Vertex;
typedef property_map<Graph, vertex_name_t>::type vertex_name_type;
typedef boost::property_map<Graph, boost::edge_index_t>::type EdgeIndexMap;

class test
{
	public:
		test(double connectivity, int which_eigen_vector, int cluster_size);
		~test();
		void self_init_graph(Graph &graph);
		void init_graph_from_file(std::ifstream &datafile, Graph &graph);
		void walk_vertices(Graph &graph);
		void walk_edges(Graph &subgraph, Graph &graph);
		gsl_matrix *graph2gsl_matrix(Graph &graph);
		gsl_vector *return_eigen_vector(gsl_matrix* graph_matrix, int which_eigen_vector);
		double connectivity_of_graph(Graph &graph);
		std::vector<Graph> subgraph_components(Graph &subgraph, Graph &graph, std::vector<int> component, int no_of_components);
		void clustering(Graph &graph);
		void output();
		void run();
		
		Graph g;
		std::vector<int> vertex_name_array;
		std::map<std::string, Vertex> VertexNameMap;
		//property_map of the vertex names
		vertex_name_type vertex2name;
		int min_cluster_size;
		int eigen_vector_no;
		double connectivity_cutoff;
		//store the final results
		std::vector<Graph> good_clusters;

};

test::test(double connectivity, int which_eigen_vector, int cluster_size)
{
	//parameter initialization
	eigen_vector_no = which_eigen_vector;		//second minimum
	connectivity_cutoff = connectivity;	
	min_cluster_size = cluster_size;
}

test::~test()
{
	//do nothing
	std::cout<<"End"<<std::endl;
}

void test::self_init_graph(Graph &graph)
{
	vertex_name_array.push_back(1);
	vertex_name_array.push_back(2);
	vertex_name_array.push_back(3);
	vertex_name_array.push_back(4);
	vertex_name_array.push_back(5);
	std::vector <int>::iterator vi_iter;
	Vertex u;
	vertex2name = get(vertex_name, graph);
	for (vi_iter=vertex_name_array.begin();vi_iter!=vertex_name_array.end(); vi_iter++)
	{
		u = add_vertex(graph);
		vertex2name[u] = *vi_iter;
		std::cout<<*vi_iter;
		//VertexNameMap.insert(std::make_pair(*vi_iter, u));
	}
	std::cout<<std::endl;
	Edge edge_array[] = {Edge(A,B), Edge(A,D), Edge(C,A), Edge(D,C),  Edge(C,E), Edge(B,D), Edge(D,E),Edge(B,C)};
	const int num_edges = sizeof(edge_array)/sizeof(edge_array[0]);
	int weight_array[] = {6,7,6,8,9,10,6,7,9,10,11,2,3,};
	//add one by one
	for (std::size_t j = 0; j < num_edges; ++j) {
		graph_traits<Graph>::edge_descriptor e; bool inserted;
		tie(e, inserted) = add_edge(edge_array[j].first, edge_array[j].second, graph);
	}
	//setup an exterior property_map for edge weights
	EdgeIndexMap edge_id = boost::get(boost::edge_index, graph);
	boost::iterator_property_map<int*, EdgeIndexMap, int, int&>
	weight_pa(weight_array, edge_id);
	
	#if defined(DEBUG)
	//print the edge weights
	std::cout<<"weights of the edges:"<<std::endl;
	boost::graph_traits<Graph>::edge_iterator ei, ei_end;
	for (tie(ei,ei_end)=edges(graph);ei!=ei_end;++ei)
		std::cout<<get(edge_id,*ei)<<":"<<get(weight_pa, *ei)<<"\t";
	std::cout<<std::endl;
	#endif
	//add in a whole
	//g = Graph(edge_array, edge_array+num_edges, weight_array, num_vertices);
}

void test::init_graph_from_file(std::ifstream &datafile, Graph &graph)
{
	std::vector<int> weight_array;
	vertex2name = get(vertex_name, graph);
	for (std::string line; std::getline(datafile, line);) {
		char_delimiters_separator < char >sep(false, "", " ");
		tokenizer <> line_toks(line, sep);
		tokenizer <>::iterator i = line_toks.begin();
		*i++;	//skip 'e'
		std::string gene1 = *i++;
		std::map<std::string, Vertex>::iterator pos;
		bool inserted;
		Vertex u, v;
		tie(pos, inserted) = VertexNameMap.insert(std::make_pair(gene1, Vertex()));
		if (inserted) {
			u = add_vertex(graph);
			vertex2name[u] = atoi(gene1.c_str());
			pos->second = u;
		} else
			u = pos->second;

		std::string gene2 = *i++;

		tie(pos, inserted) = VertexNameMap.insert(std::make_pair(gene2, Vertex()));
		if (inserted) {
			v = add_vertex(graph);
			vertex2name[v] = atoi(gene2.c_str());
			pos->second = v;
		} else
			v = pos->second;

		graph_traits < Graph >::edge_descriptor e;
		tie(e, inserted) = add_edge(u, v, graph);
		std::string edge_weight = *i;
		if (inserted)
			weight_array.push_back(atoi(edge_weight.c_str()));
	}
}

gsl_matrix* test::graph2gsl_matrix(Graph &graph)
{
	int dimension = num_vertices(graph);
	#if defined(DEBUG)
		std::cout<<"Dimension of the graph is "<<dimension<<std::endl;
	#endif
	gsl_matrix* m = gsl_matrix_calloc(dimension, dimension);	//calloc sets all elements to 0, different from alloc
	boost::property_map<Graph, vertex_index_t>::type
	vertex_id = get(vertex_index, graph);
	
	int index1,index2;
	graph_traits<Graph>::edge_iterator ei, ei_end;
	for (tie(ei, ei_end) = edges(graph); ei!=ei_end; ++ei)
	{
		index1 = get(vertex_id, source(*ei, graph));
		index2 = get(vertex_id, target(*ei, graph));
		gsl_matrix_set(m, index1, index2, 1.0);
		gsl_matrix_set(m, index2, index1, 1.0);	//undirected, symmetric
	}
	return m;
}


gsl_vector* test::return_eigen_vector(gsl_matrix* graph_matrix, int which_eigen_vector)
{
	gsl_vector *eval = gsl_vector_alloc (graph_matrix->size1);
	gsl_matrix *evec = gsl_matrix_alloc (graph_matrix->size1, graph_matrix->size2);

	gsl_eigen_symmv_workspace * w =
		gsl_eigen_symmv_alloc(graph_matrix->size1);
	gsl_eigen_symmv (graph_matrix, eval, evec, w);
	gsl_eigen_symmv_free (w);
	gsl_eigen_symmv_sort (eval, evec,
						  GSL_EIGEN_SORT_VAL_ASC);
	gsl_vector* evec_i = gsl_vector_alloc(graph_matrix->size1);
	if(gsl_matrix_get_col(evec_i, evec, which_eigen_vector))
	{
		std::cerr<<"error occured when get the eigenvector"<<std::endl;
		return NULL;
	};
	gsl_vector_free(eval);
	gsl_matrix_free(evec);
	return evec_i;
}

double test::connectivity_of_graph(Graph &graph)
{

	int no_of_vertices = num_vertices(graph);
	int no_of_edges = num_edges(graph);
	if(no_of_vertices<=1)
		return 0;
		//only one vertex, cause floating point exception
	double connectivity = 2*no_of_edges/(no_of_vertices*(no_of_vertices-1));
	return connectivity;
}

std::vector<Graph> test::subgraph_components(Graph &subgraph, Graph &graph, std::vector<int> component, int no_of_components)
{
	//initialize the vector_subgraph with the number of components
	std::vector<Graph> vector_subgraph(no_of_components);
	for(int i=0;i<no_of_components;i++)
		vector_subgraph[i] = graph.create_subgraph();
	//two vertex_descriptor
	boost::graph_traits<Graph>::vertex_descriptor
	vertex_local, vertex_global;
	//the vertex_index_global map is used to translate the global descriptor to the global index.
	boost::property_map<Graph, vertex_index_t>::type
	vertex_index_global;
	vertex_index_global = get(vertex_index, graph);
	for(int i=0; i<component.size(); i++)
	{
		int component_no = component[i];
		//i is the local index, get a descriptor from it
		vertex_local = vertex(i, subgraph);
		//find the global descriptor
		vertex_global = subgraph.local_to_global(vertex_local);
		//get the global index and add it to the subgraph
		add_vertex(get(vertex_index_global, vertex_global), vector_subgraph[component_no]);
	}
	
	return vector_subgraph;
}


void test::clustering(Graph &graph)
{
	gsl_matrix* m = graph2gsl_matrix(graph);
	#if defined(DEBUG)
		std::cout<<"The matrix is "<<std::endl;
		gsl_matrix_fprintf(stdout, m, "%g");		//check matrix
	#endif
	gsl_vector* evec_i = return_eigen_vector(m, eigen_vector_no);
	#if defined(DEBUG)
		gsl_vector_fprintf (stdout,evec_i, "%g");
	#endif
	int i;
	std::cout<<"Second minimum eigenvector: "<<std::endl;
	for(i=0;i<evec_i->size;++i)
		std::cout<<gsl_vector_get(evec_i, i)<<"\t";
	std::cout<<std::endl;
	//split the big graph based on eigenvector, >0 or <0
	std::vector<Graph> vector_subgraph(2);
	vector_subgraph[0] = graph.create_subgraph();
	vector_subgraph[1] = graph.create_subgraph();
	for(i=0;i<evec_i->size;++i)
	{
		if (gsl_vector_get(evec_i, i)<0)
			add_vertex(i, vector_subgraph[0]);
		else
			add_vertex(i, vector_subgraph[1]);
	}
	
	for(i=0; i<2; i++)
	{
		int num_vertices_of_subgraph = num_vertices(vector_subgraph[i]);
		if (num_vertices_of_subgraph < min_cluster_size)
			//stop here, too small, even it could be empty
			continue;
		//get all the components and check
		std::vector<int> component(num_vertices_of_subgraph);
		int no_of_components = connected_components(vector_subgraph[i], &component[0]);
		std::vector<Graph> vector_sub_subgraph = subgraph_components(vector_subgraph[i], graph, component, no_of_components);
		
		std::vector<Graph>::iterator g_iterator;
		std::cout<<"No of components of "<<i<<" is: "<<no_of_components<<std::endl;
		for(g_iterator=vector_sub_subgraph.begin();g_iterator!=vector_sub_subgraph.end();++g_iterator)
		{
			if(num_vertices(*g_iterator)>=min_cluster_size)
			{
				double connectivity = connectivity_of_graph(*g_iterator);
				if (connectivity>=connectivity_cutoff)
					good_clusters.push_back(*g_iterator);
				else
					clustering(*g_iterator);
			}
		}
	}
}

void test::run()
{
	std::ifstream datafile("./sample_graph.dat");
	if (datafile)
	{
		init_graph_from_file(datafile, g);
		datafile.close();
	}
	else
	{
		std::cerr << "No ./sample_graph.dat file" << std::endl;
		self_init_graph(g);
	}
	walk_vertices(g);
	clustering(g);
	output();
}


void test::walk_vertices(Graph &graph)
{
	boost::graph_traits<Graph>::vertex_descriptor 
	s = vertex(0, graph);
	vertex_name_type vertexname=get(vertex_name, graph);
	std::cout<<"the out edges for vertex "<<get(vertexname, s)<<": ";
	boost::graph_traits<Graph>::out_edge_iterator e, e_end;
	for(tie(e, e_end) = out_edges(s,graph); e!=e_end; ++e)
		std::cout<<"("<<source(*e, graph)<<target(*e,graph)<<")";
	std::cout<<std::endl;
	std::cout<<"Number of vertices: "<<num_vertices(graph)<<std::endl;
	
	boost::property_map<Graph, vertex_index_t>::type
	vertex_id = get(vertex_index, graph);
	
	std::cout << "vertices(g) = ";
	typedef graph_traits<Graph>::vertex_iterator vertex_iter;
	std::pair<vertex_iter, vertex_iter> vp;
	for (vp = vertices(graph); vp.first != vp.second; ++vp.first)
		std::cout << get(vertexname, *vp.first) <<  " ";
	std::cout << std::endl;

	std::cout << "vertices(g) = ";
	for (vp = vertices(graph); vp.first != vp.second; ++vp.first)
		std::cout << vertexname[*vp.first] <<  " ";
	std::cout << std::endl;
}

void test::walk_edges(Graph &subgraph, Graph &graph)
{
	
	boost::property_map<Graph, vertex_index_t>::type
	vertex_id = get(vertex_index, graph);
	boost::graph_traits<Graph>::vertex_descriptor
	vertex_local, vertex_local1, vertex_global, vertex_global1;
	std::cout << "edges(g) = ";
	graph_traits<Graph>::edge_iterator ei, ei_end;
	for (tie(ei,ei_end) = edges(subgraph); ei != ei_end; ++ei)
	{
		vertex_local = source(*ei, subgraph);
		vertex_local1 = target(*ei, subgraph);
		vertex_global = subgraph.local_to_global(vertex_local);
		vertex_global1 = subgraph.local_to_global(vertex_local1);
		std::cout << "(" << get(vertex_id, vertex_global)
		<< "," << get(vertex_id, vertex_global1) << ") ";
		std::cout << "[" << get(vertex2name, vertex_global)
		<< "," << get(vertex2name, vertex_global1) << "] ";
	}
	std::cout << std::endl;
	
}

void test::output()
{
	std::vector<Graph>::iterator g_iterator;
	for(g_iterator=good_clusters.begin();g_iterator!=good_clusters.end();++g_iterator)
		walk_edges(*g_iterator, g);
}

int main(int argc, char* argv[])
{
	test instance(atof(argv[1]), atoi(argv[2]), atoi(argv[3]));
	instance.run();
}
