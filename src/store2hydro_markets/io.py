from pathlib import Path
import pypsa


def load_network(path: str | Path) -> pypsa.Network:
    """
    Load a PyPSA network from either:
    - a NetCDF file (.nc), or
    - a CSV folder exported from PyPSA
    """
    path = Path(path)

    if path.is_file() and path.suffix == ".nc":
        return pypsa.Network(path)

    if path.is_dir():
        n = pypsa.Network()
        n.import_from_csv_folder(path)
        return n

    raise ValueError(f"Unsupported network path: {path}")
