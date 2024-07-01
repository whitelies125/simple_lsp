import warnings
warnings.simplefilter('ignore', FutureWarning)

from tree_sitter_languages import get_language, get_parser

language = get_language("python")
parser = get_parser("python")

example = """
def NoUseFunc():
    return 0
a = 1 # a is integer
b = False # b is bool
b = a # assign integer to bool
"""

# 创建抽象语法树
tree = parser.parse(example.encode())
root_node = tree.root_node
print(root_node.sexp())

print("--------")

var_condition = "(assignment left: (identifier) @var right: (_) @type)"
var_query = language.query(var_condition)
var_result = var_query.captures(root_node)
print(var_result)

dic = {}
var = ""
type = ""
for node, name in var_result:
    if (name == 'var'):
        var = node.text.decode('utf-8')
        print("var : ", var)
    if (name == 'type'):
        type = node.type
        if type == "identifier":
            type = dic[node.text.decode('utf-8')]
        print("type : ", type)
        if var in dic:
            if dic[var] != type:
                print("type does not match")
                print(node.start_point)
                print(node.end_point)
        else:
            dic[var] = type
print(dic)

# # 查询条件
# condition = "(assignment left: (identifier) @left_id right: (identifier) @right_id)"
# # 创建查询对象
# query = language.query(condition)
# # 执行查询
# result = query.captures(root_node)
# print(result)
#
# l_id = 'l_id'
# r_id = 'r_id'
# for node, name in result:
#     if (name == 'left_id'):
#         l_id = node.text.decode('utf-8')
#     if (name == 'right_id'):
#         r_id = node.text.decode('utf-8')
# print(l_id, r_id)

# points = set(
#     (node.start_point, node.end_point) for node, _ in result
# )
# print(points)
