from src.fstree.FileStructureTree import FileStructureTree

tree = FileStructureTree('.')

# demo
currentNode = tree.root
while True:
    print(f'\nin {currentNode.path} \
        \n\tchildren: {[node.path for node in currentNode.children]} \
        \n\tfiles: {currentNode.files}\n')
    next = int(input('enter child index, -2 for parent, or -1 to exit: '))
    if next == -1:
        break
    elif next == -2:
        if currentNode.parent is None:
            pass
        currentNode = currentNode.parent
    else:
        currentNode = currentNode.children[next]
