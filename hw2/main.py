def fill_row(row):
    return " & ".join(list(map(str, row)))


def fill_values(table):
    return " \\\\ ".join(list(map(fill_row, table)))


def fill_head(n):
    return '\\begin{tabular}{' + " ".join(["c"] * n) + "}"


def fill_tail():
    return '\\end{tabular}'


def gen_tex_table(table):
    return " ".join([func(*arg) for func, arg in zip([fill_head, fill_values, fill_tail], [[len(table[0])], [table], []])])


if __name__ == '__main__':
    print(gen_tex_table([[0, 1, 2], [0, 1, 2], [0, 1, 2]]))