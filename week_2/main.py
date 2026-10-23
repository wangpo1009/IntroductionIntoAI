import os
import sys
import argparse
from solve import Solution

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

arg = argparse.ArgumentParser()
arg.add_argument("-m", "--method", choices=["bfs", "dfs"], default="bfs",
                 help="Specify which method to use")
arg.add_argument("-l", "--legend", action="store_true",
                 help="Display legend on graph")

args = vars(arg.parse_args())

solve_method = args["method"]
legend_flag = args["legend"]


def main():
    s = Solution()

    if s.solve(solve_method):

        # Display Solution on console
        s.show_solution()

        output_file_name = f"{solve_method}"
        # Draw legend if legend_flag is set
        if legend_flag:
            output_file_name += "_legend.png"
            s.draw_legend()
        else:
            output_file_name += ".png"

        # Write State space tree to week_2 directory
        week_2_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(week_2_dir, output_file_name)
        s.write_image(output_path)
    else:
        raise Exception("No solution found")


if __name__ == "__main__":
    main()
