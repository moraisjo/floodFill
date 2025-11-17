from collections import deque
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
except ImportError:
    plt = None  # type: ignore
    ListedColormap = None  # type: ignore


Grid = List[List[int]]


def flood_fill_region(grid: Grid, start: Tuple[int, int], color: int) -> bool:
    n_rows = len(grid)
    if n_rows == 0:
        return False
    n_cols = len(grid[0])

    sr, sc = start

    if not (0 <= sr < n_rows and 0 <= sc < n_cols):
        return False
    if grid[sr][sc] != 0:
        return False

    queue: deque[Tuple[int, int]] = deque()
    queue.append((sr, sc))
    grid[sr][sc] = color

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n_rows and 0 <= nc < n_cols and grid[nr][nc] == 0:
                grid[nr][nc] = color
                queue.append((nr, nc))

    return True


def color_all_regions(grid: Grid, start: Tuple[int, int]) -> Grid:
    current_color = 2

    if flood_fill_region(grid, start, current_color):
        current_color += 1

    n_rows = len(grid)
    if n_rows == 0:
        return grid
    n_cols = len(grid[0])

    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 0:
                if flood_fill_region(grid, (r, c), current_color):
                    current_color += 1

    return grid


def read_input() -> Tuple[Grid, Tuple[int, int]]:
    """
    Formato de entrada (texto), compatível com o enunciado:

    n m
    <n linhas com m inteiros>
    x y

    Exemplo:
    4 5
    0 0 1 0 0
    0 1 1 0 0
    0 0 1 1 1
    1 1 0 0 0
    0 0
    """
    first_line = input().strip().split()
    if len(first_line) != 2:
        raise ValueError("Primeira linha deve conter n e m.")
    n, m = map(int, first_line)

    grid: Grid = []
    for _ in range(n):
        row_values = list(map(int, input().strip().split()))
        if len(row_values) != m:
            raise ValueError("Cada linha do grid deve conter exatamente m valores.")
        grid.append(row_values)

    start_line = input().strip().split()
    if len(start_line) != 2:
        raise ValueError("Linha de coordenadas deve conter x e y.")
    x, y = map(int, start_line)

    return grid, (x, y)


def print_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(str(v) for v in row))


def get_example_input() -> Tuple[Grid, Tuple[int, int]]:
    """Retorna o exemplo do enunciado, para testes rápidos."""
    grid = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0],
    ]
    start = (0, 0)
    return grid, start


def build_colormap(max_value: int) -> ListedColormap:
    base_colors = [
        "#FFFFFF",  # 0 - branco (navegável)
        "#000000",  # 1 - preto (obstáculo)
        "#FF0000",  # 2 - vermelho
        "#FFA500",  # 3 - laranja
        "#FFFF00",  # 4 - amarelo
    ]

    extra_colors = [
        "#00FF00",
        "#0000FF",
        "#800080",
        "#00FFFF",
        "#FFC0CB",
        "#A52A2A",
    ]

    colors = list(base_colors)
    idx = 0
    while len(colors) <= max_value:
        colors.append(extra_colors[idx % len(extra_colors)])
        idx += 1

    return ListedColormap(colors)


def show_visualization(initial_grid: Grid, final_grid: Grid) -> None:
    if plt is None or ListedColormap is None:
        print("Aviso: matplotlib não está disponível; visualização desativada.")
        return

    all_values = [v for row in initial_grid for v in row] + [
        v for row in final_grid for v in row
    ]
    max_value = max(all_values) if all_values else 0
    cmap = build_colormap(max_value)

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    im0 = axes[0].imshow(initial_grid, cmap=cmap, vmin=0, vmax=max_value)
    axes[0].set_title("Entrada")
    axes[0].set_xlabel("Colunas")
    axes[0].set_ylabel("Linhas")
    axes[0].invert_yaxis()

    im1 = axes[1].imshow(final_grid, cmap=cmap, vmin=0, vmax=max_value)
    axes[1].set_title("Saída")
    axes[1].set_xlabel("Colunas")
    axes[1].set_ylabel("Linhas")
    axes[1].invert_yaxis()

    fig.colorbar(im1, ax=axes.ravel().tolist(), shrink=0.8)
    fig.tight_layout()
    plt.show()


def main() -> None:
    # Usa um exemplo pré-configurado, sem entrada do usuário.
    grid, start = get_example_input()

    initial_grid = [row[:] for row in grid]
    colored_grid = color_all_regions(grid, start)

    print("Saída:")
    print("Grid preenchido:")
    print_grid(colored_grid)

    print()
    print("Legenda:")
    print("0 - Branco (Terreno navegável)")
    print("1 - Preto (Obstáculo)")
    print("2 - Vermelho")
    print("3 - Laranja")
    print("4 - Amarelo")

    show_visualization(initial_grid, colored_grid)


if __name__ == "__main__":
    main()
