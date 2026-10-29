import csv
from pathlib import Path


def create_plot(csv_path):
    with csv_path.open(encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    generations = [int(row["generation"]) for row in rows]
    values = [int(row["best_objective"]) for row in rows]

    if not values:
        raise ValueError(f"Plik jest pusty: {csv_path}")

    problem = csv_path.stem.split("_")[0].upper()

    x_max = max(generations) or 1
    y_min = min(values) - 1
    y_max = max(values) + 1

    def x_position(generation):
        return 80 + 680 * generation / x_max

    def y_position(value):
        return 340 - 280 * (value - y_min) / (y_max - y_min)

    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="820" height="420" viewBox="0 0 820 420">',
        '<rect width="820" height="420" fill="white"/>',
        '<g font-family="Arial" font-size="14" fill="#222">',
        f'<text x="410" y="28" text-anchor="middle">'
        f'{problem} — najlepszy wynik w kolejnych generacjach</text>',
    ]

    for i in range(6):
        value = y_min + (y_max - y_min) * i / 5
        y = y_position(value)

        elements.append(
            f'<line x1="80" y1="{y}" x2="760" y2="{y}" '
            f'stroke="#ddd"/>'
        )
        elements.append(
            f'<text x="68" y="{y + 5}" text-anchor="end">'
            f'{value:.1f}</text>'
        )

        generation = round(x_max * i / 5)
        x = x_position(generation)
        elements.append(
            f'<text x="{x}" y="365" text-anchor="middle">'
            f'{generation}</text>'
        )

    # Schodki: wynik zmienia się dopiero w danej generacji.
    points = [(x_position(generations[0]), y_position(values[0]))]

    for i in range(1, len(values)):
        x = x_position(generations[i])
        points.append((x, y_position(values[i - 1])))
        points.append((x, y_position(values[i])))

    coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)

    elements.extend([
        '<path d="M80 60 V340 H760" fill="none" stroke="#222"/>',
        f'<polyline points="{coordinates}" fill="none" '
        'stroke="#2563eb" stroke-width="2"/>',
        '<text x="420" y="400" text-anchor="middle">Generacja</text>',
        '<text transform="translate(22 200) rotate(-90)" '
        'text-anchor="middle">Najlepsza wartość funkcji celu</text>',
        '</g></svg>',
    ])

    output_path = csv_path.with_suffix(".svg")
    output_path.write_text("\n".join(elements), encoding="utf-8")
    print(f"Zapisano wykres: {output_path}")


if __name__ == "__main__":
    results_dir = Path(__file__).resolve().parent / "results"
    csv_files = sorted(results_dir.glob("*.csv"))

    if not csv_files:
        print("Brak plików trajectory.csv w folderze results.")

    for csv_path in csv_files:
        create_plot(csv_path)