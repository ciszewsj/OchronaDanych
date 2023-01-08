#include <stdio.h>
#define N 8
/* quaz, quax sa odlozone ponizej sterty (heap) */
char quaz[N];
char quax[N];
int main(int argc, char *argv[]){
	/* foo, bar, baz sa odlozone na stos (stack) */
	char foo[N];
	char bar[N];
	char baz[N];
	/* spam, eggs sa odlozone na stercie (heap) */
	char *spam = calloc(N, sizeof(char));
	char *eggs = calloc(N, sizeof(char));
	if (argc < 3) {
		printf("usage: %s aaa bbb ccc\n", argv[0]);
		return 1;
	}
	strcpy(baz, argv[1]);
	strcpy(spam, argv[2]);
	strcpy(quaz, argv[3]);
	printf("%p foo: %s\n", foo, foo);
	printf("%p bar: %s\n", bar, bar);
	printf("%p baz: %s\n", baz, baz);
	printf("%p spam: %s\n", spam, spam);
	printf("%p eggs: %s\n", eggs, eggs);
	printf("%p quaz: %s\n", quaz, quaz);
	printf("%p quax: %s\n", quax, quax);
	return 0;
}

