from rich.markdown import HorizontalRule
import math


def show_stats(console, stats, minimal):
    if minimal:
        console.print(
            f"  Mean score: {stats['all']['mean']:.1f}/{stats['out_of']} " +
            f"({100*stats['all']['mean']/stats['out_of']:.1f}%)"
        )
        console.print(
            f"Median score: {stats['all']['median']:.1f}/{stats['out_of']} " +
            f"({100*stats['all']['median']/stats['out_of']:.1f}%)"
        )
        return

    console.print(HorizontalRule())

    console.print(f"   Total marked: {stats['total_marked']}")
    console.print(f"Compile success: {stats['compile_success']}")
    console.print(f" Compile failed: {stats['compile_failed']}")
    console.print(HorizontalRule())

    console.print(
        f"  Mean score [yellow]     (all)[/yellow]: " +
        f"{stats['all']['mean']:.2g}/{stats['out_of']} " +
        f"({100*stats['all']['mean']/stats['out_of']:.1f}%)"
    )
    console.print(
        f"Median score [yellow]     (all)[/yellow]: " +
        f"{stats['all']['median']:.2g}/{stats['out_of']} " +
        f"({100*stats['all']['median']/stats['out_of']:.1f}%)"
    )
    console.print(HorizontalRule())

    console.print(
        f"  Mean score [yellow] (compiled)[/yellow]: " +
        f"{stats['compiled']['mean']:.2g}/{stats['out_of']} " +
        f"({100*stats['compiled']['mean']/stats['out_of']:.1f}%)"
    )
    console.print(
        f"Median score [yellow] (compiled)[/yellow]: " +
        f"{stats['compiled']['median']:.2g}/{stats['out_of']} " +
        f"({100*stats['compiled']['median']/stats['out_of']:.1f}%)"
    )
    console.print(HorizontalRule())

    console.print("Mark distribution:")

    HIST_LINE_LEN = 20

    distribution = stats["distribution"]

    output_scale = HIST_LINE_LEN / max(k for _, k in distribution.items())
    for mark, count in distribution.items():
        line_count = math.ceil(count * output_scale)
        hist_line = 'x' * (line_count) + ' ' * (HIST_LINE_LEN - line_count)
        console.print(
            f" {mark:3d} : [green]{hist_line}[/green] | {count:3d} students"
        )

    console.print(HorizontalRule())