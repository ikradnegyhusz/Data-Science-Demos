//This small program aims to reformat a text file to a
//desireable format for the Page Rank script
#include "stdio.h"
#include "stdlib.h"

//get length of a string
int len(char* s)
{
	int i=0;
	while(s[i]!='\0')
		i++;
	return i;
}

//concatenate two strings
char* concat(char* s1, char* s2)
{
	int l1=len(s1);
	int l2=len(s2);
	char* ret=malloc(sizeof(char)*(l1+l2));
	int i;
	for(i=0;i<l1;i++)
		ret[i]=s1[i];
	for(int k=0;k<l2;k++,i++)
		ret[i]=s2[k];
	ret[i]='\0';
	return ret;
}

int main(int argc, char* argv[])
{
	if(argc<2)
	{ 
		printf("Give the filepath as a command line argument.");
		return 0;
	}
	
	FILE* fptr;
	FILE* out;
	
	//open files
	fptr=fopen(argv[1],"r");
	argv[1][len(argv[1])-4]='\0'; // place \0 before .txt in filepath
	out=fopen(concat( argv[1] ,"_formatted.txt"),"w+");
	
	//initialize variables for read
	char c;
	char read_space=0;
	int char_temp = 0;
	int values_read=0;
	
	//loop through input file and only write the two values separated by a space
	//into the output file (each line)
	while((c=fgetc(fptr)) != EOF)
	{
		if(c=='\n')
		{
			fputc(c,out);
			values_read=0;
			char_temp=0;
			read_space=0;
			continue;
		}
		if(c!=' ')
		{
			fputc(c,out);
			read_space=1;
			char_temp++;
		}
		else if (read_space && values_read<1)
		{
			fputc(c,out);
			read_space=0;
			if (char_temp>0) values_read++; 
		}
	}
	fclose(out);
	fclose(fptr);
	
	return 0;
}