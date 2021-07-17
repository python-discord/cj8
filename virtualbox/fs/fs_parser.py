import xml.etree.ElementTree as xml
from typing import Any, Callable


def savexml(dicit: dict, path: str, naming: list, name: str) -> None:
    """Saves dicit into xml file"""
    root = xml.Element(name)

    for name, content in dicit.items():
        child = xml.Element(name)
        for item, subname in zip(content, naming):
            value = xml.SubElement(child, subname)
            value.text = str(item)

        root.append(child)

    with open(path, "wb") as f:
        xml.ElementTree(root).write(f)


def readxml(path: str, mapf: Callable[[str], Any]) -> dict:
    """Reads dicit saved by savexml function"""
    Result = {}
    try:
        root = xml.ElementTree(file=path).getroot()
    except Exception as e:
        raise Exception("XML ERROR " + path + " ERROR: " + str(e))

    for element in root:
        Result[element.tag] = [mapf(i.text) for i in element]

    return Result
