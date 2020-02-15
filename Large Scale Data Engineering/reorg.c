#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>

#include "utils.h"

unsigned long person_length, knows_length, interest_length;
unsigned long person_new_length, knows_new_length, interest_new_length;

Person *person_map;
unsigned int *knows_map;
unsigned short *interest_map;

Person_new *person_map_new;
unsigned int *knows_map_new;

void update_knows (void) {
	unsigned int person_offset;
	unsigned long knows_offset, knows_offset2;
	Person *person, *knows;

	// Alloc new person array
	person_map_new = malloc(person_length * sizeof(Person_new));

	// Alloc new knows array
	unsigned int knows_map_new_count = 0, knows_map_new_set_size = 1000;
	knows_map_new = malloc(knows_length * sizeof(unsigned int));

	unsigned long person_knows_first = 0;

	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_length/sizeof(Person); person_offset++){
		person = &person_map[person_offset];
		
		unsigned int person_knows_count = 0;

		// Check for all their connections
		for(knows_offset = person->knows_first; knows_offset < person->knows_first + person->knows_n; knows_offset++){
			knows = &person_map[knows_map[knows_offset]];
			// If connection lives in same city, check for mutual friendship
			if(person->location == knows->location){
				person_knows_count++;
				knows_map_new[knows_map_new_count] = knows_map[knows_offset];
				knows_map_new_count++;
			}
		}
	
		Person_new *new_person = malloc(sizeof(Person_new));
		new_person->person_id = person->person_id;
		new_person->birthday =  person->birthday;
		new_person->interests_first = person->interests_first;
		new_person->interest_n = person->interest_n;

		new_person->knows_first = person_knows_first;
		new_person->knows_n = person_knows_count;

		person_map_new[person_offset] = *new_person;
		person_knows_first += person_knows_count;
	}

	// Shrink arrays to correct size
	person_map_new = realloc(person_map_new, person_offset * sizeof(Person_new));
	knows_map_new = realloc(knows_map_new, knows_map_new_count * sizeof(unsigned int));

	// Set to globals
	person_new_length = person_offset;
	knows_new_length = knows_map_new_count;
}

void print_stats(void){
	unsigned int person_offset;
	unsigned long knows_offset;

	Person_new *person, *knows;
	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_length/sizeof(Person_new); person_offset++) {
		person = &person_map_new[person_offset];
		for (knows_offset = person->knows_first; knows_offset < person->knows_first + person->knows_n; knows_offset++) {
			knows = &person_map_new[knows_map_new[knows_offset]];
			printf("%ld, %ld\n", person->person_id, knows->person_id);
		}
		printf("\n");
	}
}


FILE *knows_out;
FILE *person_out;

int main(int argc, char *argv[]) {
	unsigned offset = 0;

	person_map   = (Person *)         mmapr(makepath(argv[1], "person",   "bin"), &person_length);
	interest_map = (unsigned short *) mmapr(makepath(argv[1], "interest", "bin"), &interest_length);
	knows_map    = (unsigned int *)   mmapr(makepath(argv[1], "knows",    "bin"), &knows_length);

	update_knows();
	
	// print_stats();

	printf("Finished updating\n");

	char* person_output_file = makepath(argv[1], "person_reorg", "bin");
	person_out = fopen(person_output_file, "w");
	for(offset = 0; offset < person_new_length; offset++){
		fwrite(&person_map_new[offset], sizeof(Person_new), 1, person_out);
	}
	fclose(person_out);

	char* knows_output_file = makepath(argv[1], "knows_reorg", "bin");
	knows_out = fopen(knows_output_file, "w");
	for(offset = 0; offset < knows_new_length; offset++){
		fwrite(&knows_map_new[offset], sizeof(unsigned int), 1, person_out);
	}
	fclose(knows_out);
	
	return 0;
}

