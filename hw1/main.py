import ast
import networkx as nx
import matplotlib.pyplot as plt

fibonacci_code = \
"""
def fibonacci(n: int) -> list:
    numbers = [0, 1]

    if n < 0:
        return []
    
    if n == 0:
        return [0]

    for i in range(2, n + 1):
        numbers.append(numbers[-1] + numbers[-2])

    return numbers
"""


def parse_if(if_ast, parent_name, graph, if_name, op='<'):
    graph.add_edges_from([(parent_name, f'If{if_name}')])
    graph.add_edges_from([(f'If{if_name}', f'Compare{if_name}')])
    graph.add_edges_from([(f'If{if_name}', f'Statement{if_name}')])
    graph.add_edges_from([(f'Compare{if_name}', f'{if_name}: left = {if_ast.test.left.id}')])
    graph.add_edges_from([(f'Compare{if_name}', f'{if_name}: right = {if_ast.test.comparators[0].value}')])
    graph.add_edges_from([(f'Compare{if_name}', f'op {op}')])

    graph.add_edges_from([(f'Statement{if_name}', f'Return{if_name}')])
    graph.add_edges_from([(f'Return{if_name}', f'List{if_name}')])
    for value in if_ast.body[0].value.elts:
        graph.add_edges_from([(f'List{if_name}', f'{if_name}: {value.value}')])


def parse_assign(assign_ast, parent_name, graph, assign_name):
    graph.add_edges_from([(parent_name, f'Assign{assign_name}')])
    name = assign_ast.targets[0].id
    graph.add_edges_from([(f'Assign{assign_name}', f'{assign_name}: {name}')])
    graph.add_edges_from([(f'Assign{assign_name}', f'List{assign_name}')])
    for value in assign_ast.value.elts:
        graph.add_edges_from([(f'List{assign_name}', f'{assign_name}: {value.value}')])


def parse_for(for_ast, parent_name, graph, for_name):
    graph.add_edges_from([(parent_name, f'For{for_name}')])
    graph.add_edges_from([(f'For{for_name}', f'Call{for_name}')])
    graph.add_edges_from([(f'Call{for_name}', f'Append{for_name}')])
    graph.add_edges_from([(f'Append{for_name}', f'{for_name}: {for_ast.body[0].value.func.value.id}')])
    graph.add_edges_from([(f'Append{for_name}', f'BinOp{for_name}')])
    graph.add_edges_from([(f'BinOp{for_name}', f'op +')])
    graph.add_edges_from([(f'BinOp{for_name}', f'left: Subscript')])
    graph.add_edges_from([(f'BinOp{for_name}', f'right: Subscript')])

    bin_op_left = for_ast.body[0].value.args[0].left
    bin_op_right = for_ast.body[0].value.args[0].right
    graph.add_edges_from([(f'left: Subscript', f'left: {bin_op_left.value.id}')])
    graph.add_edges_from([(f'right: Subscript', f'right: {bin_op_right.value.id}')])

    graph.add_edges_from([(f'left: Subscript', f'left: Slice')])
    graph.add_edges_from([(f'right: Subscript', f'right: Slice')])

    graph.add_edges_from([(f'left: Slice', f'left: Unary')])
    graph.add_edges_from([(f'right: Slice', f'right: Unary')])

    graph.add_edges_from([(f'left: Unary', f'left: -')])
    graph.add_edges_from([(f'right: Unary', f'right: -')])

    graph.add_edges_from([(f'left: Unary', f'{for_name}: {bin_op_left.slice.operand.value}')])
    graph.add_edges_from([(f'right: Unary', f'{for_name}: {bin_op_right.slice.operand.value}')])


def build_graph():
    ast_object = ast.parse(fibonacci_code).body[0]
    graph = nx.DiGraph()
    parse_assign(ast_object.body[0], ast_object.name, graph, '0')
    parse_if(ast_object.body[1], ast_object.name, graph, '1')
    parse_if(ast_object.body[2], ast_object.name, graph, '2', '==')
    parse_for(ast_object.body[3], ast_object.name, graph, '3')

    graph.add_edges_from([(ast_object.name, f'Return4')])
    graph.add_edges_from([(f'Return4', f'4: {ast_object.body[4].value.id}')])

    nx.draw(graph, with_labels=True)
    plt.show()


if __name__ == '__main__':
    build_graph()

