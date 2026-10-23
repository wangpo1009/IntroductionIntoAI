import os
import shutil
import argparse
from collections import deque
import pydot

# Không sửa PATH cố định; dùng PATH hệ thống, biến môi trường GRAPHVIZ_BIN, hoặc tự động phát hiện đường dẫn Graphviz
graphviz_bin = os.environ.get("GRAPHVIZ_BIN")
if graphviz_bin:
    os.environ["PATH"] += os.pathsep + graphviz_bin
elif shutil.which("dot") is None:
    for candidate in [
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Graphviz\bin"),
    ]:
        if os.path.exists(os.path.join(candidate, "dot.exe")):
            os.environ["PATH"] += os.pathsep + candidate
            break

options = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]
Parent = dict()
graph = pydot.Dot(graph_type='graph', strict=False, bgcolor="#fff3af",
                  label="fig: Missionaries and Cannibal State Space Tree",
                  fontcolor="red", fontsize="24", overlap="true")
# To track node
i = 0

arg = argparse.ArgumentParser()
arg.add_argument("-d", "--depth", required=False, type=int,
                 help="MAximum depth upto which you want to generate Space State Tree")

args = vars(arg.parse_args())

depth_arg = args.get("depth")
max_depth = 20 if depth_arg is None else depth_arg
if max_depth < 0:
    raise SystemExit("--depth phải là số nguyên >= 0")


def is_valid_move(number_missionaries, number_cannnibals):
    """
    Checks if number constraints are satisfied
    """
    return (0 <= number_missionaries <= 3) and (0 <= number_cannnibals <= 3)


def write_image(file_name="state_space"):
    week_2_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(week_2_dir, f"{file_name}_{max_depth}.png")
    try:
        graph.write_png(target_path)
        print(f"File {target_path} successfully written.")
    except Exception as e:
        print("Error while writing file", e)
        raise


def draw_edge(number_missionaries, number_cannnibals, side, depth_level, node_num):
    u, v = None, None
    if Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)] is not None:
        u = pydot.Node(str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)]),
                       label=str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)][:3]))
        graph.add_node(u)

        v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)),
                       label=str((number_missionaries, number_cannnibals, side)))
        graph.add_node(v)

        edge = pydot.Edge(str(Parent[(number_missionaries, number_cannnibals, side, depth_level, node_num)]),
                          str((number_missionaries, number_cannnibals, side, depth_level, node_num)), dir='forward')
        graph.add_edge(edge)
    else:
        # For start node
        v = pydot.Node(str((number_missionaries, number_cannnibals, side, depth_level, node_num)),
                       label=str((number_missionaries, number_cannnibals, side)))
        graph.add_node(v)
    return u, v


def is_start_state(number_missionaries, number_cannnibals, side):
    return (number_missionaries, number_cannnibals, side) == (3, 3, 1)


def is_goal_state(number_missionaries, number_cannnibals, side):
    return (number_missionaries, number_cannnibals, side) == (0, 0, 0)


def number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
    number_missionaries_right = 3 - number_missionaries
    number_cannnibals_right = 3 - number_cannnibals
    return (number_missionaries > 0 and number_cannnibals > number_missionaries) \
        or (number_missionaries_right > 0 and number_cannnibals_right > number_missionaries_right)


def generate():
    global i
    q = deque()
    node_num = 0
    q.append((3, 3, 1, 0, node_num))

    Parent[(3, 3, 1, 0, node_num)] = None
    visited = {(3, 3, 1)}

    while q:
        number_missionaries, number_cannnibals, side, depth_level, node_num = q.popleft()

        u, v = draw_edge(number_missionaries, number_cannnibals, side, depth_level, node_num)

        if is_start_state(number_missionaries, number_cannnibals, side):
            v.set_style("filled")
            v.set_fillcolor("blue")
            v.set_fontcolor("white")
        elif is_goal_state(number_missionaries, number_cannnibals, side):
            v.set_style("filled")
            v.set_fillcolor("green")
            continue
        elif number_of_cannibals_exceeds(number_missionaries, number_cannnibals):
            v.set_style("filled")
            v.set_fillcolor("red")
            continue
        else:
            v.set_style("filled")
            v.set_fillcolor("orange")

        if depth_level == max_depth:
            continue

        op = -1 if side == 1 else 1

        can_be_expanded = False

        for x, y in options:
            next_m, next_c, next_s = number_missionaries + op * x, number_cannnibals + op * y, int(not side)

            if (next_m, next_c, next_s) not in visited and is_valid_move(next_m, next_c):
                visited.add((next_m, next_c, next_s))
                can_be_expanded = True
                i += 1
                q.append((next_m, next_c, next_s, depth_level + 1, i))
                # Keep track of parent
                Parent[(next_m, next_c, next_s, depth_level + 1, i)] = (
                    number_missionaries, number_cannnibals, side, depth_level, node_num
                )

        if not can_be_expanded:
            v.set_style("filled")
            v.set_fillcolor("gray")

    return True


if __name__ == "__main__":
    if generate():
        write_image()
