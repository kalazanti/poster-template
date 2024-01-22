#!/usr/bin/python3

import os
from sys import argv
from typing import TextIO

BEGIN = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
"""
END = "</body></html>"
TEMPLATE = """<table>
    <tr>
        <td class="img"><img src="IMG_1"></td>
        <td class="img"><img src="IMG_2"></td>
    </tr>
    <tr>
        <td>NAME_1</td>
        <td>NAME_2</td>
    </tr>
    <tr>
        <td>DESC_1</td>
        <td>DESC_2</td>
    </tr>
    <tr>
        <td class="img"><img src="IMG_3"></td>
        <td class="img"><img src="IMG_4"></td>
    </tr>
    <tr>
        <td>NAME_3</td>
        <td>NAME_4</td>
    </tr>
    <tr>
        <td>DESC_3</td>
        <td>DESC_4</td>
    </tr>
</table>
<div class="break"></div>
"""

INPUT = argv[1]
FOLDER = argv[2]
OUTPUT = argv[3]

with open(INPUT, "r") as inf:
    lines = [line.strip().split(";") for line in inf.readlines()]

duplicates = []


def render(template: list[str], name: str, troop: str, year: str, i: int):
    template[0] = template[0].replace(f"NAME_{i}", name)
    img_name = f"{FOLDER}/{name}.jpg"
    template[0] = template[0].replace(f"IMG_{i}", img_name)
    desc = troop
    if "-" in year:
        desc += f" {year}"
    elif year != "NA":
        desc += f", {year}."
    template[0] = template[0].replace(f"DESC_{i}", desc)


def process(lines: list, file: TextIO):
    template = [TEMPLATE]
    for i, line in enumerate(lines):
        name, troop, year, _ = line
        render(template, name, troop, year, i + 1)
    file.write(template[0])
    file.write("\n")

def does_file_exist(line:str)->bool:
    try:
        name, _, _, _ = line
        exists = os.path.isfile(f"{FOLDER}/{name}.jpg")
        if not exists:
            print(f"⚠️ File does not exist for {name}")
        return exists
    except ValueError as e:
        print(line)
        raise e
    

def process_groups_of_four(lines: list, duplicates: list | None, file: TextIO):
    working_memory = []
    for line in lines:
        if len(working_memory) == 4:
            process(working_memory, file)
            working_memory = []
        if duplicates is not None and line[3] == "DUPLICATE":
            duplicates.append(line)
            continue
        
        if not does_file_exist(line):
            continue
        working_memory.append(line)
    if working_memory:
        process(working_memory, file)


with open(OUTPUT, "w") as out:
    out.write(BEGIN)
    out.write("\n")
    process_groups_of_four(lines, duplicates, out)
    process_groups_of_four(duplicates, None, out)
    out.write(END)
