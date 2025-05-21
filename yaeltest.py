import time
from AVLTree import AVLTree

def main(): 
    print("here")
    avl_tree = AVLTree()
    start = time.time()
    for i in range(10000):
        avl_tree.insert(i, "num" + str(i))
    print("Insertions:", time.time() - start)

    start = time.time()
    for i in range(10000):
        node = avl_tree.search(i)
        if node is not None:
            avl_tree.delete(node)
    print("Deletions:", time.time() - start)

if __name__ == '__main__':
    main()