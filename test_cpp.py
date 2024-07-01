import warnings
warnings.simplefilter('ignore', FutureWarning)

from tree_sitter_languages import get_language, get_parser

language = get_language("cpp")
parser = get_parser("cpp")

example = """
int foo() {
    return 1;
}

int func() {
    return false;
}

int func(int a, int b) {
    return a != b;
}
"""

# 创建抽象语法树
tree = parser.parse(example.encode())
root_node = tree.root_node
print(root_node.sexp())

print("--------")
condition = """
(function_definition
    type: (_) @func_ret_type
    body: (compound_statement (return_statement (_) @ret_type)))
"""
query = language.query(condition)
result = query.captures(root_node)
print(result)

func_ret_type = ""
ret_type = ""
for node, name in result:
    print("node.type : ", node.type)
    if (name == 'func_ret_type'):
        func_ret_type = node.text.decode('utf-8')
        print("func_ret_type : ", func_ret_type)
    if (name == 'ret_type'):
        if node.type == "primitive_type":
            ret_type = node.text.decode('utf-8')
        if node.type == "binary_expression" or node.type == "false" or node.type == "true":
            ret_type = "bool"
        if node.type == "number_literal" :
            ret_type = "int"
        print("ret_type : ", ret_type)
        if (ret_type != func_ret_type):
            print("type does not match")
