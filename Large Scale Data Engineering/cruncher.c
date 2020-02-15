#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>

#include "utils.h"

#define QUERY_FIELD_QID 0
#define QUERY_FIELD_A1 1
#define QUERY_FIELD_A2 2
#define QUERY_FIELD_A3 3
#define QUERY_FIELD_A4 4
#define QUERY_FIELD_BS 5
#define QUERY_FIELD_BE 6

Person_new *person_map;
unsigned int *knows_map;
unsigned short *interest_map;

unsigned long person_length, knows_length, interest_length;

FILE *outfile;

int result_comparator(const void *v1, const void *v2) {
    Result *r1 = (Result *) v1;
    Result *r2 = (Result *) v2;
    if (r1->score > r2->score)
        return -1;
    else if (r1->score < r2->score)
        return +1;
    else if (r1->person_id < r2->person_id)
        return -1;
    else if (r1->person_id > r2->person_id)
        return +1;
     else if (r1->knows_id < r2->knows_id)
        return -1;
    else if (r1->knows_id > r2->knows_id)
        return +1;
    else
        return 0;
}

unsigned char get_score(Person_new *person, unsigned short areltd[]) {
	long interest_offset;
	unsigned short interest;
	unsigned char score = 0;
	for (interest_offset = person->interests_first; 
		interest_offset < person->interests_first + person->interest_n; 
		interest_offset++) {

		interest = interest_map[interest_offset];
		if (areltd[0] == interest) score++;
		if (areltd[1] == interest) score++;
		if (areltd[2] == interest) score++;
		// early exit
		if (score > 2) {
			break;
		}
	}
	return score;
}

char likes_artist(Person_new *person, unsigned short artist) {
	long interest_offset;
	unsigned short interest;
	unsigned short likesartist = 0;

	for (interest_offset = person->interests_first; 
		interest_offset < person->interests_first + person->interest_n; 
		interest_offset++) {

		interest = interest_map[interest_offset];
		if (interest == artist) {
			likesartist = 1;
			break;
		}
	}
	return likesartist;
}

typedef struct {
	unsigned char score;
	unsigned char likes;
	unsigned int in_range;
} Result_struct;

void query(unsigned short qid, unsigned short artist, unsigned short areltd[], unsigned short bdstart, unsigned short bdend) {
	unsigned int person_offset;
	unsigned long knows_offset, knows_offset2;

	Person_new *person, *knows;
	unsigned char score;

	unsigned int result_length = 0, result_idx, result_set_size = 1000;
	Result* results = malloc(result_set_size * sizeof (Result));
	printf("Running query %d\n", qid);

	Result_struct *arr_results = malloc(person_length / sizeof(Person_new) * sizeof(Result_struct));

	for (person_offset = 0; person_offset < person_length/sizeof(Person_new); person_offset++) {
		person = &person_map[person_offset];

		unsigned char tmp_score;
		unsigned int tmp_in_range;
		
		if (person->birthday < bdstart || person->birthday > bdend) {
			tmp_score = 0;
			tmp_in_range = 0;
		}
		else {
			tmp_score = get_score(person, areltd);	
			tmp_in_range = 1;
		}

		arr_results[person_offset].score = tmp_score;
		arr_results[person_offset].likes = likes_artist(person, artist);
		arr_results[person_offset].in_range = tmp_in_range;

	}


	unsigned int loc_not = 0;

	for (person_offset = 0; person_offset < person_length/sizeof(Person_new); person_offset++) {
		person = &person_map[person_offset];

		if (person_offset > 0 && person_offset % REPORTING_N == 0) {
			printf("%.2f%%\n", 100 * (person_offset * 1.0/(person_length/sizeof(Person_new))));
		}

		// filter by birthday
		if (!arr_results[person_offset].in_range) continue; 

		// person must not like artist yet
		if (arr_results[person_offset].likes) continue;

		// person must like some of these other guys
		score = arr_results[person_offset].score;
		if (score < 1) continue;

		// check if friend lives in same city and likes artist 
		for (knows_offset = person->knows_first; knows_offset < person->knows_first + person->knows_n; knows_offset++) {
			
			knows = &person_map[knows_map[knows_offset]];

			// friend must already like the artist
			if (!arr_results[knows_map[knows_offset]].likes) continue;

			// friendship must be mutual
			for (knows_offset2 = knows->knows_first;
				knows_offset2 < knows->knows_first + knows->knows_n;
				knows_offset2++) {
			
				if (knows_map[knows_offset2] == person_offset) {

					// realloc result array if we run out of space
					if (result_length >= result_set_size) {
						result_set_size *= 2;
						results = realloc(results, result_set_size * sizeof (Result));
					}

					results[result_length].person_id = person->person_id;
					results[result_length].knows_id = knows->person_id;
					results[result_length].score = score;
					result_length++;

					break;
				}
			}
		}
	}

	// sort result
	qsort(results, result_length, sizeof(Result), &result_comparator);

	// output
	for (result_idx = 0; result_idx < result_length; result_idx++) {
		fprintf(outfile, "%d|%d|%lu|%lu\n", qid, results[result_idx].score, 
			results[result_idx].person_id, results[result_idx].knows_id);
	}

	free(arr_results);
}

void query_line_handler(unsigned char nfields, char** tokens) {
	unsigned short q_id, q_artist, q_bdaystart, q_bdayend;
	unsigned short q_relartists[3];

	q_id            = atoi(tokens[QUERY_FIELD_QID]);
	q_artist        = atoi(tokens[QUERY_FIELD_A1]);
	q_relartists[0] = atoi(tokens[QUERY_FIELD_A2]);
	q_relartists[1] = atoi(tokens[QUERY_FIELD_A3]);
	q_relartists[2] = atoi(tokens[QUERY_FIELD_A4]);
	q_bdaystart     = birthday_to_short(tokens[QUERY_FIELD_BS]);
	q_bdayend       = birthday_to_short(tokens[QUERY_FIELD_BE]);
	
	query(q_id, q_artist, q_relartists, q_bdaystart, q_bdayend);
}

void test(){
	unsigned int person_offset, knows_offset;
	Person_new *person, *knows;
	//  Loop over all existing persons
	for(person_offset = 0; person_offset < person_length/sizeof(Person_new); person_offset++) {
		person = &person_map[person_offset];
		printf("%ld\n", person->person_id);
	}
}

int main(int argc, char *argv[]) {
	if (argc < 4) {
		fprintf(stderr, "Usage: [datadir] [query file] [results file]\n");
		exit(1);
	}

	clock_t before = clock();
	
	/* memory-map files created by loader */
	person_map   = (Person_new *)         mmapr(makepath(argv[1], "person_reorg",   "bin"), &person_length);
	interest_map = (unsigned short *) mmapr(makepath(argv[1], "interest", "bin"), &interest_length);
	knows_map    = (unsigned int *)   mmapr(makepath(argv[1], "knows_reorg",    "bin"), &knows_length);

	// test();

  	outfile = fopen(argv[3], "w");  
  	if (outfile == NULL) {
  		fprintf(stderr, "Can't write to output file at %s\n", argv[3]);
		exit(-1);
  	}
  	/* run through queries */
	parse_csv(argv[2], &query_line_handler);

	clock_t difference = clock() - before;
	int msec = difference * 1000 / CLOCKS_PER_SEC;
	printf("Time taken %d seconds %d milliseconds \n", msec/1000, msec%1000);

	return 0;
}
