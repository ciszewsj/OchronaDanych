#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
	int zalogowany;
	char haslo[8];
	zalogowany = 0;
	strcpy(haslo, argv[1]);
	if (strcmp(haslo, "Tajne") == 0)
		zalogowany = 1;
	if (zalogowany == 1)
		printf("TAK\n");
	else
		printf("NIE\n");
	return 0;
}
