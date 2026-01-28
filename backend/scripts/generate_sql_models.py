#!/usr/bin/env python3
"""
Generate SQLAlchemy models from goodcollect.schema.sql
"""
import re
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "domain" / "models" / "SQL" / "goodcollect.schema.sql"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "domain" / "models" / "sql.py"


def parse_enums(content: str) -> list[tuple[str, list[str]]]:
    """Parse CREATE TYPE ... AS ENUM from schema."""
    enums = []
    pattern = r'CREATE TYPE public\.("[\w]+") AS ENUM \(\s*(.*?)\s*\);'
    for match in re.finditer(pattern, content, re.DOTALL):
        name = match.group(1).strip('"')
        values_str = match.group(2)
        values = [v.strip().strip("'") for v in values_str.split(",")]
        enums.append((name, values))
    return enums


def parse_tables(content: str) -> list[tuple[str, list[tuple[str, str, bool, str | None]]]]:
    """Parse CREATE TABLE public."..." ( ... ); and return (table_name, [(col_name, sql_type, nullable, default)])"""
    tables = []
    # Match CREATE TABLE public."TableName" or public._prisma_migrations
    table_pattern = r'CREATE TABLE public\.("?[\w]+"?)\s*\(\s*(.*?)\s*\)\s*;'
    for match in re.finditer(table_pattern, content, re.DOTALL):
        table_name = match.group(1).strip('"') if match.group(1).startswith('"') else match.group(1)
        body = match.group(2)
        columns = []
        for line in body.split("\n"):
            line = line.strip().rstrip(",").strip()
            if not line:
                continue
            # Column: "name" type ... or name type ...
            col_match = re.match(r'^("?)([\w]+)\1\s+(.+)$', line)
            if not col_match:
                continue
            col_name = col_match.group(2)
            rest = col_match.group(3)
            # Extract base type (first token) and check NOT NULL / DEFAULT
            parts = rest.split()
            sql_type_raw = ""
            i = 0
            while i < len(parts):
                p = parts[i]
                if p.upper() == "NOT":
                    i += 2
                    continue
                if p.upper() == "NULL":
                    i += 1
                    continue
                if p.upper() == "DEFAULT":
                    i += 1
                    # skip default value (until next comma or end)
                    while i < len(parts) and parts[i] != ",":
                        i += 1
                    continue
                sql_type_raw = p
                i += 1
                break
            # Rebuild full type for enums: public."EnumName" or timestamp(3) without time zone etc
            type_start = rest.find(sql_type_raw)
            type_end = len(rest)
            for kw in ["NOT NULL", "DEFAULT", "NULL"]:
                idx = rest.find(kw, type_start)
                if idx != -1:
                    type_end = min(type_end, idx)
            full_type = rest[:type_end].strip().rstrip(",")
            nullable = "NOT NULL" in rest.upper() and "DEFAULT" not in rest.upper()
            nullable = "NOT NULL" not in rest.upper()
            # Actually: NOT NULL means not nullable
            nullable = "NOT NULL" not in rest.upper()
            columns.append((col_name, full_type, nullable, None))
        tables.append((table_name, columns))
    return tables


def sql_type_to_sqlalchemy(sql_type: str, enum_name: str | None) -> str:
    """Map SQL type string to SQLAlchemy type expression."""
    sql_type = sql_type.strip()
    if enum_name:
        return f'Enum({enum_name}, name="{enum_name}", create_constraint=False)'
    if sql_type == "text":
        return "Text"
    if sql_type == "integer":
        return "Integer"
    if "timestamp" in sql_type and "without time zone" in sql_type:
        return "DateTime(timezone=False)"
    if "timestamp" in sql_type and "with time zone" in sql_type:
        return "DateTime(timezone=True)"
    if sql_type == "double precision":
        return "Float"
    if sql_type == "boolean":
        return "Boolean"
    if sql_type == "jsonb":
        return "JSONB"
    if sql_type == "text[]":
        return "ARRAY(Text)"
    if sql_type == "integer[]":
        return "ARRAY(Integer)"
    if sql_type.startswith("character varying") or sql_type.startswith("varchar"):
        m = re.search(r"\((\d+)\)", sql_type)
        n = m.group(1) if m else "255"
        return f"String({n})"
    # public."EnumName"
    m = re.match(r'public\.("?)([\w]+)\1', sql_type)
    if m:
        return f'Enum({m.group(2)}, name="{m.group(2)}", create_constraint=False)'
    return "Text"


def _pascal_split(name: str) -> list[str]:
    """Split PascalCase or mixed name into words."""
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+", name)


def python_class_name(table_name: str) -> str:
    """Convert table name to Python class name (preserve PascalCase)."""
    if table_name.startswith("_"):
        if table_name == "_prisma_migrations":
            return "PrismaMigrations"
        # _ActivityZoneDepartmentToProvider -> ActivityZoneDepartmentToProvider
        parts = _pascal_split(table_name.lstrip("_"))
        return "".join(w.capitalize() for w in parts)
    # ActivityZoneDepartment -> keep as-is (already PascalCase)
    if table_name[0].isupper() and "_" not in table_name:
        return table_name
    # snake_case -> PascalCase
    return "".join(w.capitalize() for w in table_name.split("_"))


def main():
    content = SCHEMA_PATH.read_text(encoding="utf-8")
    enums = parse_enums(content)
    tables = parse_tables(content)

    # Build enum name -> Python enum class
    enum_map = {}
    for name, values in enums:
        safe_name = name.replace(" ", "_")
        enum_map[name] = safe_name

    lines = [
        '"""',
        "SQLAlchemy models generated from goodcollect.schema.sql",
        "Do not edit manually; regenerate with scripts/generate_sql_models.py if needed.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "import enum",
        "from datetime import datetime",
        "from typing import Optional",
        "",
        "from sqlalchemy import (",
        "    ARRAY,",
        "    Boolean,",
        "    DateTime,",
        "    Enum,",
        "    Float,",
        "    Integer,",
        "    String,",
        "    Text,",
        ")",
        "from sqlalchemy.dialects.postgresql import JSONB",
        "from sqlalchemy.orm import Mapped, mapped_column, declarative_base",
        "",
        "Base = declarative_base()",
        "",
    ]

    # Emit Python enums (use string enum for SQL compatibility)
    for name, values in enums:
        class_name = enum_map[name]
        lines.append(f"class {class_name}(str, enum.Enum):")
        for v in values:
            safe_v = v.replace(" ", "_")
            lines.append(f'    {safe_v} = "{v}"')
        lines.append("")
        lines.append("")

    # Emit table models
    for table_name, columns in tables:
        class_name = python_class_name(table_name)
        if table_name == "_prisma_migrations":
            class_name = "PrismaMigrations"
        lines.append(f"class {class_name}(Base):")
        lines.append(f'    __tablename__ = "{table_name}"')
        lines.append('    __table_args__ = {"schema": "public"}')
        lines.append("")

        for idx, (col_name, full_type, nullable, _default) in enumerate(columns):
            enum_match = re.match(r'public\.("?)([\w]+)\1', full_type)
            enum_class = enum_match.group(2) if enum_match else None
            if enum_class and enum_class in enum_map:
                sa_type = sql_type_to_sqlalchemy(full_type, enum_map[enum_class])
            else:
                sa_type = sql_type_to_sqlalchemy(full_type, None)

            py_attr = col_name
            optional = " | None" if nullable else ""

            is_pk = (col_name == "id" and idx == 0) or (
                table_name.startswith("_") and table_name != "_prisma_migrations" and col_name in ("A", "B")
            )
            is_int_pk = "integer" in full_type.lower() and col_name == "id" and idx == 0 and table_name != "User"
            autoinc = is_int_pk

            kwargs = [f'"{col_name}"', sa_type, f"nullable={nullable}"]
            if is_pk:
                kwargs.append("primary_key=True")
            if autoinc:
                kwargs.append("autoincrement=True")

            lines.append(f"    {py_attr}: Mapped[{sa_type}{optional}] = mapped_column({', '.join(kwargs)})")
        lines.append("")
        lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
