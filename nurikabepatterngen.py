import itertools
from typing import List

class PatternGeneration:
    def __init__(self, size: int):
        self.matrix_size = size
        self.generated_rows = []
        self.matrix_list = []
        self.pattern = [' '] * self.matrix_size
        self.pool_check_array = []
        self.pattern_check = False
        self.area = 0

    def generate_rows(self, index: int):
        if index < self.matrix_size:
            self.pattern[index] = '1'
            self.generate_rows(index + 1)

            self.pattern[index] = '0'
            self.generate_rows(index + 1)
        else:
            final_pattern = ''.join(self.pattern)
            self.generated_rows.append(final_pattern)

    def create_report(self):
        with open("pattern.txt", "w") as sw:
            index = 1
            margin = "     "

            for matrix in self.matrix_list:
                sw.write(f"{index}.  \n")

                for i in range(self.matrix_size):
                    sw.write(margin)
                    for j in range(self.matrix_size):
                        sw.write(f"{matrix[i][j]} ")
                    sw.write("\n")
                sw.write("\n")
                index += 1

    def pool_check(self, matrix: List[str]) -> bool:
        self.pattern_check = True
        test_matrix = [[0] * self.matrix_size for _ in range(2)]
        array_one = list(matrix[0])
        array_two = list(matrix[1])

        for j in range(self.matrix_size - 1):
            test_matrix[0][0] = int(array_one[j])
            test_matrix[0][1] = int(array_one[j + 1])
            test_matrix[1][0] = int(array_two[j])
            test_matrix[1][1] = int(array_two[j + 1])

            if test_matrix[0][0] == 1 and test_matrix[0][1] == 1 and test_matrix[1][0] == 1 and test_matrix[1][1] == 1:
                self.pattern_check = False

        return self.pattern_check

    def area_for_matrix(self, matrix: List[List[int]], row: int, col: int) -> int:
        if matrix[row][col] == 1:
            matrix[row][col] = 3
            self.area = 1

            if col + 1 <= self.matrix_size - 1:
                self.area += self.area_for_matrix(matrix, row, col + 1)
            if row + 1 <= self.matrix_size - 1:
                self.area += self.area_for_matrix(matrix, row + 1, col)
            if col - 1 >= 0:
                self.area += self.area_for_matrix(matrix, row, col - 1)
            if row - 1 >= 0:
                self.area += self.area_for_matrix(matrix, row - 1, col)
        else:
            self.area = 0
        return self.area

    def continuity_check_matrix(self, matrix: List[List[int]]) -> bool:
        water_count = self.water_count_for_matrix(matrix)
        stream_count = 0

        row, col = 0, 0

        if water_count > 1:
            for i in range(self.matrix_size):
                for j in range(self.matrix_size):
                    if matrix[i][j] == 1:
                        row, col = i, j
                        break
                else:
                    continue
                break

            stream_count = self.area_for_matrix(matrix, row, col)
        else:
            if water_count == 1:
                stream_count = 1

        self.pattern_check = stream_count == water_count
        return self.pattern_check

    def water_count_for_matrix(self, matrix: List[List[int]]) -> int:
        count = 0
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if matrix[i][j] == 1:
                    count += 1
        return count

    def copy_matrix(self, pattern: List[str]) -> List[List[int]]:
        new_matrix = [[0] * self.matrix_size for _ in range(self.matrix_size)]
        for k in range(self.matrix_size):
            if pattern[k]:
                copy_array = list(pattern[k])
                for j in range(self.matrix_size):
                    new_matrix[k][j] = int(copy_array[j])
        return new_matrix

    def report_progress(self, progress: int):
        print(self.matrix_list)

    def generate_pattern(self, index: int, pattern: List[str], pattern_count: int, recursive_calls: int):
        if recursive_calls % 1000 == 0:
            self.report_progress(0)

        self.pool_check_array = [""] * 2

        print(self.generated_rows)

        if index < self.matrix_size:
            for row in self.generated_rows:
                pattern[index] = row

                if index != 0:
                    self.pool_check_array[0] = pattern[index - 1]
                    self.pool_check_array[1] = pattern[index]
                    if self.pool_check(self.pool_check_array):
                        if self.continuity_check_matrix(self.copy_matrix(pattern)):
                            pass
                        else:
                            if index < (self.matrix_size - 1):
                                for row_index in self.generated_rows:
                                    pattern[index + 1] = row_index
                                    if self.continuity_check_matrix(self.copy_matrix(pattern)):
                                        break

                if self.pattern_check or index == 0:
                    self.generate_pattern(index + 1, pattern, pattern_count, recursive_calls)
                    recursive_calls += 1
        elif self.pattern_check:
            pattern_count += 1
            self.matrix_list.append(self.copy_matrix(pattern))


patternCount = 0
recursiveCalls = 0
pattern = []
size = 3
#sizey = 5
for i in range(size):
    pattern.append("");

patternGeneration = PatternGeneration(size)
patternGeneration.generate_rows(0)
patternGeneration.generate_pattern(0, pattern, patternCount, recursiveCalls)

for matrix in patternGeneration.matrix_list:
    print(matrix)