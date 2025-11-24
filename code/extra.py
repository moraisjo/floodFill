from collections import deque
from typing import List, Tuple
import random

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
except ImportError:
    plt = None  # type: ignore
    ListedColormap = None  # type: ignore


Grid = List[List[int]]


def generate_random_grid(rows: int, cols: int, obstacle_prob: float = 0.3) -> Grid:
    """
    Gera um grid aleatório com as dimensões especificadas.
    
    Args:
        rows: Número de linhas
        cols: Número de colunas
        obstacle_prob: Probabilidade de uma célula ser um obstáculo (0.0 a 1.0)
    
    Returns:
        Grid gerado aleatoriamente
    """
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            # Gera 0 (navegável) ou 1 (obstáculo) baseado na probabilidade
            if random.random() < obstacle_prob:
                row.append(1)  # Obstáculo
            else:
                row.append(0)  # Navegável
        grid.append(row)
    return grid


def find_random_start_position(grid: Grid) -> Tuple[int, int]:
    """
    Encontra uma posição inicial aleatória que seja navegável (valor 0).
    
    Returns:
        Tupla (x, y) com coordenadas válidas
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Coleta todas as posições navegáveis
    navigable_positions = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                navigable_positions.append((r, c))
    
    if not navigable_positions:
        raise ValueError("Não há posições navegáveis no grid")
    
    return random.choice(navigable_positions)


# Applies the Breadth-First Search (BFS) Flood Fill algorithm to fill a single connected region.
# It starts at the 'start' coordinate and replaces all contiguous zeros (empty cells) with the specified 'color'.
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


def flood_fill_animated(grid: Grid, start: Tuple[int, int], color: int, 
                       ax=None, cmap=None, max_value: int = 10) -> bool:
    """
    Versão animada do Flood Fill que mostra o preenchimento passo a passo.
    
    Args:
        grid: Grid a ser preenchido
        start: Posição inicial (x, y)
        color: Cor para preenchimento
        ax: Eixo do matplotlib para desenhar
        cmap: Mapa de cores
        max_value: Valor máximo para normalização
    
    Returns:
        True se o preenchimento foi realizado
    """
    n_rows = len(grid)
    if n_rows == 0:
        return False
    n_cols = len(grid[0])

    sr, sc = start

    if not (0 <= sr < n_rows and 0 <= sc < n_cols):
        return False
    if grid[sr][sc] != 0:
        return False

    queue = deque()
    queue.append((sr, sc))
    grid[sr][sc] = color
    
    # Atualiza a visualização
    if ax and cmap:
        ax.clear()
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=max_value)
        ax.set_title(f"Preenchendo região - Cor: {color}")
        ax.set_xlabel("Colunas")
        ax.set_ylabel("Linhas")
        ax.invert_yaxis()
        plt.pause(0.1)  # Pausa para animação

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n_rows and 0 <= nc < n_cols and grid[nr][nc] == 0:
                grid[nr][nc] = color
                queue.append((nr, nc))
                
                # Atualiza a visualização a cada 5 células para não ficar muito lento
                if len(queue) % 5 == 0 and ax and cmap:
                    ax.clear()
                    ax.imshow(grid, cmap=cmap, vmin=0, vmax=max_value)
                    ax.set_title(f"Preenchendo região - Cor: {color}")
                    ax.set_xlabel("Colunas")
                    ax.set_ylabel("Linhas")
                    ax.invert_yaxis()
                    plt.pause(0.05)  # Pausa mais curta durante o preenchimento

    return True


# Colors all connected regions (cells with value 0) in the grid, starting with the
# region containing the 'start' point, and then iterating through the rest of the grid.
# The coloring begins with color value 2.
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


def color_all_regions_animated(grid: Grid, start: Tuple[int, int]) -> Grid:
    """
    Versão animada que colore todas as regiões com visualização dinâmica.
    """
    if plt is None:
        print("Matplotlib não disponível. Usando versão normal.")
        return color_all_regions(grid, start)
    
    # Configura a visualização
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Determina o valor máximo para a escala de cores
    all_values = [v for row in grid for v in row]
    max_value = max(all_values) if all_values else 0
    max_value = max(max_value, 10)  # Garante espaço para novas cores
    
    cmap = build_colormap(max_value)
    
    # Mostra grid inicial
    ax1.imshow(grid, cmap=cmap, vmin=0, vmax=max_value)
    ax1.set_title("Grid Inicial")
    ax1.set_xlabel("Colunas")
    ax1.set_ylabel("Linhas")
    ax1.invert_yaxis()
    
    current_color = 2
    
    # Primeira região (com animação)
    if flood_fill_animated(grid, start, current_color, ax2, cmap, max_value):
        current_color += 1
        plt.pause(1)  # Pausa entre regiões

    n_rows = len(grid)
    n_cols = len(grid[0])

    # Demais regiões
    for r in range(n_rows):
        for c in range(n_cols):
            if grid[r][c] == 0:
                if flood_fill_animated(grid, (r, c), current_color, ax2, cmap, max_value):
                    current_color += 1
                    plt.pause(1)  # Pausa entre regiões
    
    ax2.set_title("Grid Final")
    plt.tight_layout()
    plt.show()
    
    return grid


# Reads the grid dimensions, the grid data (integers), and the starting coordinates from standard input.
# The format is expected to be: n m / <n lines of m integers> / x y.
def read_input() -> Tuple[Grid, Tuple[int, int]]:
    first_line = input().strip().split()
    if len(first_line) != 2:
        raise ValueError("Primeira linha deve conter n e m.")
    n, m = map(int, first_line)

    grid: Grid = []
    for _ in range(n):
        row_values = list(map(int, input().strip().split()))
        if len(row_values) != m:
            raise ValueError(
                "Cada linha do grid deve conter exatamente m valores.")
        grid.append(row_values)

    start_line = input().strip().split()
    if len(start_line) != 2:
        raise ValueError("Linha de coordenadas deve conter x e y.")
    x, y = map(int, start_line)

    return grid, (x, y)


# Prints the 2D grid contents to the console, with values separated by spaces.
def print_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(str(v) for v in row))


# Returns a fixed example grid and starting coordinate for quick testing purposes.
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


# Creates a Matplotlib ListedColormap object for visualization, mapping integer values
# (0, 1, 2, 3, 4, etc.) to specific colors for better contrast.
def build_colormap(max_value: int) -> ListedColormap:
    base_colors = [
        "#FFFFFF",  # 0 - branco (navegável)
        "#000000",  # 1 - preto (obstáculo)
        "#FF0000",  # 2 - vermelho
        "#FFA500",  # 3 - laranja
        "#FFFF00",  # 4 - amarelo
    ]

    extra_colors = [
        "#00FF00",  # 5 - verde
        "#0000FF",  # 6 - azul
        "#800080",  # 7 - roxo
        "#00FFFF",  # 8 - ciano
        "#FFC0CB",  # 9 - rosa
        "#A52A2A",  # 10 - marrom
        "#FFA500",  # 11 - laranja (novamente)
        "#800000",  # 12 - marrom escuro
        "#008000",  # 13 - verde escuro
    ]

    colors = list(base_colors)
    idx = 0
    while len(colors) <= max_value:
        colors.append(extra_colors[idx % len(extra_colors)])
        idx += 1

    return ListedColormap(colors)


# Displays a visualization of the initial grid and the final, colored grid side-by-side
# using Matplotlib, including a color bar for reference.
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


def test_random_grid():
    """Função de teste para grids aleatórios."""
    print("=== Teste de Geração de Grid Aleatório ===")
    
    # Gera um grid 8x12 com 25% de obstáculos
    grid = generate_random_grid(8, 12, 0.25)
    start = find_random_start_position(grid)
    
    print("Grid aleatório gerado (8x12, 25% obstáculos):")
    print_grid(grid)
    print(f"Posição inicial: {start}")
    
    initial_grid = [row[:] for row in grid]
    
    # Pergunta se quer usar animação
    use_animation = input("\nUsar animação? (s/n): ").strip().lower() == 's'
    
    if use_animation and plt is not None:
        colored_grid = color_all_regions_animated(grid, start)
    else:
        colored_grid = color_all_regions(grid, start)
        show_visualization(initial_grid, colored_grid)
    
    print("\nGrid preenchido:")
    print_grid(colored_grid)
    
    # Estatísticas
    regions = len(set(v for row in colored_grid for v in row if v >= 2))
    obstacles = sum(row.count(1) for row in colored_grid)
    navigable = sum(row.count(0) for row in initial_grid)
    
    print(f"\n--- Estatísticas ---")
    print(f"Regiões coloridas: {regions}")
    print(f"Células navegáveis: {navigable}")
    print(f"Obstáculos: {obstacles}")
    
    return initial_grid, colored_grid


def main() -> None:
    """Função principal com menu interativo."""
    print("=== Flood Fill - Colorindo Regiões ===")
    print("Escolha uma opção:")
    print("1. Usar exemplo pré-definido")
    print("2. Gerar grid aleatório")
    print("3. Entrada manual")
    print("4. Teste rápido com grid aleatório")
    
    choice = input("Digite sua opção (1-4): ").strip()
    
    if choice == "1":
        # Exemplo pré-definido
        grid, start = get_example_input()
        use_animation = input("Usar animação? (s/n): ").strip().lower() == 's'
        
    elif choice == "2":
        # Grid aleatório
        try:
            rows = int(input("Número de linhas: "))
            cols = int(input("Número de colunas: "))
            prob = float(input("Probabilidade de obstáculos (0.1-0.9): "))
            
            if not (0.1 <= prob <= 0.9):
                print("Probabilidade ajustada para 0.3 (valor padrão)")
                prob = 0.3
            
            grid = generate_random_grid(rows, cols, prob)
            start = find_random_start_position(grid)
            use_animation = True  # Sempre usar animação para grids aleatórios
            
            print(f"Grid gerado: {rows}x{cols}, obstáculos: {prob*100:.1f}%")
            print(f"Posição inicial: {start}")
            
        except ValueError as e:
            print(f"Erro na entrada: {e}")
            return
            
    elif choice == "3":
        # Entrada manual
        try:
            grid, start = read_input()
            use_animation = input("Usar animação? (s/n): ").strip().lower() == 's'
        except ValueError as e:
            print(f"Erro na entrada: {e}")
            return
    
    elif choice == "4":
        # Teste rápido
        test_random_grid()
        return
    
    else:
        print("Opção inválida!")
        return
    
    # Faz uma cópia do grid inicial
    initial_grid = [row[:] for row in grid]
    
    print("\nGrid inicial:")
    print_grid(initial_grid)
    print(f"Posição inicial: {start}")
    
    # Executa o algoritmo
    if use_animation and plt is not None:
        colored_grid = color_all_regions_animated(grid, start)
    else:
        colored_grid = color_all_regions(grid, start)
        if plt is not None:
            show_visualization(initial_grid, colored_grid)
    
    print("\nGrid preenchido:")
    print_grid(colored_grid)
    
    # Estatísticas
    regions = len(set(v for row in colored_grid for v in row if v >= 2))
    obstacles = sum(row.count(1) for row in colored_grid)
    navigable = sum(row.count(0) for row in initial_grid)
    
    print(f"\n--- Estatísticas ---")
    print(f"Regiões coloridas: {regions}")
    print(f"Células navegáveis: {navigable}")
    print(f"Obstáculos: {obstacles}")


if __name__ == "__main__":
    main()