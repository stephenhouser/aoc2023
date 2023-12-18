#include <stdio.h>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include <chrono>

// g++  -std=c++20 pb.cpp -o run_c++

static std::chrono::time_point<std::chrono::steady_clock> s_start_time;
static std::chrono::time_point<std::chrono::steady_clock> s_end_time;
static bool s_timer_active = false;

void start()
{
	s_start_time = std::chrono::steady_clock::now();
	s_timer_active = true;
}

double get_elapsed_seconds()
{
	const std::chrono::time_point<std::chrono::steady_clock> elapsed_time = s_timer_active ? std::chrono::steady_clock::now() : s_end_time;
	const auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed_time - s_start_time).count();
	return elapsed / 1000000000.0;

}

void stop()
{
	s_end_time = std::chrono::steady_clock::now();
	s_timer_active = false;
}

void print_map(std::vector<std::string> map) {
	for (auto row : map) {
		printf("%s\n", row.c_str());
	}
	
	printf("\n");
}

std::vector<std::string> load_map(const std::string& input_file) {
	std::vector<std::string> map;
	std::ifstream file_input;

	file_input.open(input_file);
	if (file_input.is_open()) {
		for (std::string line; std::getline(file_input, line); ) {
			if ( line.length() > 0 ) {
				map.push_back(line);
			}
		}

		file_input.close();
	}

	return map;
}


int main() {
	start();
	std::vector<std::string> map = load_map("test.txt");
	print_map(map);
	stop();

	printf("%g\n", get_elapsed_seconds());
}
