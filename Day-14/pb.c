#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <assert.h>

// gcc --std=c2x pb.c -o run_c

/*
 * ......\n
 * ......\n
 * 
*/

char **transpose(char **matrix, int width, int height) {
	char *data = (char *)malloc((height + 1) * width);
	assert(data != NULL);

	char **transposed = (char **)malloc((width + 1) * sizeof(char *));
	assert(transposed != NULL);

	for (int x = 0; x < width; x++) {
		transposed[x] = &data[x * (width+1)];
		for (int y = 0; y < height; y++) {
			transposed[x][y] = matrix[y][x];
		}
		transposed[x][height] = '\0';
	}
	transposed[width] = NULL;

	return transposed;
}

char **make_2d(char *text, int length, int *width, int *height) {
	int n_cols = 0; // find out row length by looking for '\n'
	for (int i = 0; text[i]; i++) {
		if (text[i] == '\n') {
			n_cols = i;
			break;
		}
	}

	int n_rows = length / n_cols;

	char *data = (char *)malloc((n_rows + 1) * n_cols);
	assert(data != NULL);

	char **matrix = (char **)malloc((n_rows + 1) * sizeof(char *));
	assert(matrix != NULL);

	for (int y = 0; y < n_rows; y++) {
		matrix[y] = &data[y * (n_cols+1)];
		memcpy(matrix[y], &data[y * (n_cols+1)], n_cols);
		// for (int x = 0; x < n_cols; x++) {
		// 	matrix[y][x] = text[(y * (n_cols+1)) + x];
		// }
		matrix[y][n_cols] = '\0';
	}
	matrix[n_rows] = NULL;

	*width = n_cols;
	*height = n_rows;
	return matrix;
}

size_t file_size(const char *file_name) {
	struct stat buf;

	if (lstat(file_name, &buf) >= 0) {
		return buf.st_size;
	}

	return -1;
}

char *load_file(const char *file_name, int *file_size) {
	struct stat buf;
	int success = lstat(file_name, &buf);
	assert(success >= 0);

	FILE *f = fopen(file_name, "r");
	assert(f != NULL);

	char *file_data = (char *)malloc(buf.st_size + 1);
	*file_size = fread(file_data, 1, buf.st_size, f);
	file_data[buf.st_size] = '\0';
	assert(*file_size == buf.st_size);

	fclose(f);
	return file_data;
}

void print_matrix(char **matrix, int width, int height) {
	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			printf("%c", matrix[y][x]);
		}
		printf("\n");
	}
}

int main() {
	int size;
	char *data = load_file("test.txt", &size);
	assert(data != NULL);

	int width, height;
	char **matrix = make_2d(data, size, &width, &height);
	assert(matrix != NULL);

	printf("matrix\n");
	print_matrix(matrix, width, height);

	char **t = transpose(matrix, width, height);

	printf("\ntransposed\n");
	print_matrix(t, height, width);


	// printf(fd);
	return 0;
}