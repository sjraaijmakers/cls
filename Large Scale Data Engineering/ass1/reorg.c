#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>

#include "utils.h"

unsigned long person_length, knows_length, interest_length;
unsigned long person_new_length, knows_new_length, interest_new_length;
unsigned long person_new_2_length, knows_new_2_length, interest_new_2_length;

Person *person_map;
unsigned int *knows_map;
unsigned short *interest_map;

Person_new *person_map_new;
unsigned int *knows_map_new;

void update_location(void){
	unsigned int person_offset;
	unsigned long knows_offset, knows_offset2;
	Person *person, *knows;

	// Alloc new arrays with original size
	person_map_new = malloc(person_length / sizeof(Person) * sizeof(Person_new));
	unsigned int set_size = knows_length / 2;
	knows_map_new = malloc(set_size);

	unsigned long person_knows_first = 0;
	unsigned long knows_map_new_count = 0, person_knows_count;

	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_length/sizeof(Person); person_offset++){
		person_knows_count = 0;
		person = &person_map[person_offset];

		// Check for all their connections
		for(knows_offset = person->knows_first; knows_offset < person->knows_first + person->knows_n; knows_offset++){
			knows = &person_map[knows_map[knows_offset]];
			// If connection lives in same city
			if(person->location == knows->location){
				if (knows_map_new_count >= set_size) {
					set_size *= 2;
					knows_map_new = realloc(knows_map_new, set_size * sizeof(unsigned int));
				}
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

	// Shrink new arrays to correct size
	person_map_new = realloc(person_map_new, (person_offset+1) * sizeof(Person_new));
	knows_map_new = realloc(knows_map_new, (knows_map_new_count+1) * sizeof(unsigned int));

	// Set globals (for printing purposes)
	person_new_length = person_offset;
	knows_new_length = knows_map_new_count+1;
}

Person_new *person_map_new_2;
unsigned int *knows_map_new_2;

// Remove non-mutual friendship

void update_mutual(void){
	unsigned int person_offset;
	unsigned long knows_offset, knows_offset2;

	person_map_new_2 = malloc(person_new_length);
	knows_map_new_2 = malloc(knows_new_length*sizeof(unsigned int));

	Person_new *person, *knows;

	unsigned long person_knows_first = 0;
	unsigned int knows_map_new_count = 0, person_knows_count;

	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_new_length; person_offset++) {
		person_knows_count = 0;
		person = &person_map_new[person_offset];

		for (knows_offset = person->knows_first; knows_offset < person->knows_first + person->knows_n; knows_offset++) {
			knows = &person_map_new[knows_map_new[knows_offset]];

			// friendship must be mutual
			for (knows_offset2 = knows->knows_first; knows_offset2 < knows->knows_first + knows->knows_n; knows_offset2++){
				if (knows_map_new[knows_offset2] == person_offset) {
					knows_map_new_2[knows_map_new_count] = knows_map_new[knows_offset2];
					knows_map_new_count++;
					person_knows_count++;
					break;
				}
			}
		}

		Person_new *new_person = malloc(sizeof(Person_new));
		new_person->person_id = person->person_id;
		new_person->birthday =  person->birthday;
		new_person->interests_first = person->interests_first;
		new_person->interest_n = person->interest_n;

		new_person->knows_first = person_knows_first;
		new_person->knows_n = person_knows_count;

		person_map_new_2[person_offset] = *new_person;
		person_knows_first += person_knows_count;
	}
	
	printf("%d\n", knows_map_new_count);

	// Shrink new arrays to correct size
	person_map_new_2 = realloc(person_map_new_2, (person_offset+1) * sizeof(Person_new));
	knows_map_new_2 = realloc(knows_map_new_2, (knows_map_new_count+1) * sizeof(unsigned int));

	// Set globals (for printing purposes)
	person_new_2_length = person_offset;
	knows_new_2_length = knows_map_new_count+1;
}	

void print_stats(void){
	unsigned int person_offset;
	unsigned long knows_offset;

	Person_new *person, *knows;
	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_new_2_length/sizeof(Person_new); person_offset++) {
		person = &person_map_new_2[person_offset];
	}

	printf("old: %ld, new: %ld\n", knows_new_length, knows_new_2_length);
}


FILE *knows_out;
FILE *person_out;

int main(int argc, char *argv[]){
	char *person_output_file, *person_output_file_2, *knows_output_file, *knows_output_file_2;

	unsigned offset = 0;

	person_map   = (Person *)         mmapr(makepath(argv[1], "person",   "bin"), &person_length);
	interest_map = (unsigned short *) mmapr(makepath(argv[1], "interest", "bin"), &interest_length);
	knows_map    = (unsigned int *)   mmapr(makepath(argv[1], "knows",    "bin"), &knows_length);

	update_location();

	update_mutual();

	print_stats();

	printf("Finished updating\n");

	person_output_file = makepath(argv[1], "person_reorg", "bin");
	person_out = fopen(person_output_file, "w");
	for(offset = 0; offset < person_new_length; offset++){
		fwrite(&person_map_new[offset], sizeof(Person_new), 1, person_out);
	}
	fclose(person_out);

	printf("Finished writing persons\n");

	knows_output_file = makepath(argv[1], "knows_reorg", "bin");
	knows_out = fopen(knows_output_file, "w");
	for(offset = 0; offset < knows_new_length; offset++){
		fwrite(&knows_map_new[offset], sizeof(unsigned int), 1, knows_out);
	}
	fclose(knows_out);

	printf("Finished writing knows\n");

	person_output_file = makepath(argv[1], "person_reorg_2", "bin");
	person_out = fopen(person_output_file, "w");
	for(offset = 0; offset < person_new_2_length; offset++){
		fwrite(&person_map_new_2[offset], sizeof(Person_new), 1, person_out);
	}
	fclose(person_out);

	printf("Finished writing persons2\n");


	knows_output_file = makepath(argv[1], "knows_reorg_2", "bin");
	knows_out = fopen(knows_output_file, "w");
	for(offset = 0; offset < knows_new_2_length; offset++){
		fwrite(&knows_map_new_2[offset], sizeof(unsigned int), 1, knows_out);
	}
	fclose(knows_out);

	printf("Finished writing knows2\n");
	
	return 0;
}

