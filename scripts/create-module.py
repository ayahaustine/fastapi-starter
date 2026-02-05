#!/usr/bin/env python3
"""
Script to create a new module with standard structure.
Usage: poetry run create-module <module_name>
"""

import argparse
from pathlib import Path
from string import Template


def create_module(module_name: str):
    module_path = Path(f"app/{module_name}")

    if module_path.exists():
        print(f"❌ Module '{module_name}' already exists!")
        return

    # module directory
    module_path.mkdir(parents=True)

    (module_path / "__init__.py").touch()

    # standard files
    files = [
        "models.py",
        "schemas.py",
        "crud.py",
        "service.py",
        "router.py",
        "deps.py",
        "exceptions.py",
        "constants.py",
    ]

    for file in files:
        (module_path / file).touch()

    # basic content for router.py
    router_template = Template('''"""
$module_name routes.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/${module_name}", tags=["${module_name}"])


@router.get("/")
async def get_${module_name}():
    """Get ${module_name}."""
    return {"message": "Hello from ${module_name}!"}
''')

    router_content = router_template.substitute(module_name=module_name)
    (module_path / "router.py").write_text(router_content)

    print(f"Module '{module_name}' created successfully!")
    print(f"Location: {module_path}")


def main():
    parser = argparse.ArgumentParser(description="Create a new module")
    parser.add_argument("name", help="Name of the module to create")
    args = parser.parse_args()

    create_module(args.name)


if __name__ == "__main__":
    main()
