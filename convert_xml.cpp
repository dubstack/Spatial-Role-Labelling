#include<iostream>
#include<algorithm>
#include<stdio.h>
#include<cstdlib>
#include<sstream>
#include<string.h>
#include<set>
#include<map>
#include<assert.h>
#include<ctime>
#include<queue>
#include<vector>
#include<stack>
#include<list>
#include<math.h>
#include<fstream>
using namespace std;
typedef vector<int> vi;
typedef vector<string> vs;
typedef pair<int,int> pii;
typedef long long int lli;

#define MAXN 1000005
#define INF 2147483647
#define MOD 1000000007
#define pb push_back 
#define sz(a) int((a).size())
#define FOR(x,a,b) for(int (x) = (a);(x)<=(b);(x)++)
#define rep(x,n)   for(int (x)=0;(x)<(n);(x)++)
#define tr(c,it) for(typeof((c).begin()) it = (c).begin(); it != (c).end(); it++)
#define all(c) c.begin(),c.end()
#define mset(a,b) memset(a,b,sizeof(a))



int main(int num,char *args[])
{
	//freopen("input.txt","r",stdin);
	//freopen("output.xml","w",stdout);
	char line[MAXN];
	char x[MAXN/10];
	int c = 0;
	string temp = "<SENTENCE id=\"s";
	ifstream in;
	in.open(args[1],ifstream::in);
	ofstream out;
	out.open(args[2],ofstream::out);
	out<<"<DOC>\n";
	while(in.getline(line,MAXN-100))
	{ 
		c++;	
		stringstream ss(line);
		out<<temp<<c<<"\">";
		out<<"\n<CONTENT>";
		while(ss>>x)
			out<<x<<" ";
		out<<"</CONTENT>\n";
		out<<"</SENTENCE>\n";
	}
	 out<<"</DOC>\n";

	return 0;
}
