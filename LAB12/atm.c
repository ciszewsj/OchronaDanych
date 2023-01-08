#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, char** argv) {
	unsigned int pin;
	unsigned int amount;
	int balance = 100;

	if (isdigit(argv[2][0]) == 0) {
		printf("Attach mitigated\n");
		exit(1);
	}

	sscanf(argv[1], "%u", &pin);
	sscanf(argv[2], "%u", &amount);

	if (pin != 1234) {
		printf("\033[31;1mPIN Invalid\033[0m\n");
		exit(2);
	} else {
		printf("\033[32;1mPIN Accepted\033[0m\n");
	}

	printf("Deposit:\n");
	printf("%dBTC - %dBTC = %dBTC\n", balance, amount, balance - amount);
	return 0;
}
