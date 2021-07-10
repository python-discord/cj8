import xml.etree.ElementTree as xml


def savexml(dicit, path, naming, name):
    root = xml.Element(name)

    for name, content in dicit.items():
        child = xml.Element(name)
        for item, subname in zip(content, naming):
            value = xml.SubElement(child, subname)
            value.text = str(item)

        root.append(child)

    with open(path, "wb") as f:
        xml.ElementTree(root).write(f)


def readxml(path, mapf):
    Result = {}
    root = xml.ElementTree(file=path).getroot()

    for element in root:
        Result[element.tag] = [mapf(i.text) for i in element]

    return Result
