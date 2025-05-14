
class Tree_node:
    def __init__(self, key, val):
        self.key   = key
        self.val   = val
        self.left  = None
        self.right = None

    def __repr__(self):
        return "(" + str(self.key) + ":" + str(self.val) + ")"

    
class Binary_search_tree:

    def __init__(self):
        self.root = None
        self.size = 0


    def __repr__(self):  # you don't need to understand the implementation of this method
        def printree(root):
            if not root:
                return ["#"]

            root_key = str(root.key)
            left, right = printree(root.left), printree(root.right)

            lwid = len(left[-1])
            rwid = len(right[-1])
            rootwid = len(root_key)

            result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

            ls = len(left[0].rstrip())
            rs = len(right[0]) - len(right[0].lstrip())
            result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

            for i in range(max(len(left), len(right))):
                row = ""
                if i < len(left):
                    row += left[i]
                else:
                    row += lwid * " "
                row += (rootwid + 2) * " "

                if i < len(right):
                    row += right[i]
                else:
                    row += rwid * " "
                result.append(row)
            return result

        return '\n'.join(printree(self.root))


    def lookup(self, key):
        ''' return value of node with key if exists, else None '''

        node = self.root
        while node != None:
            if key == node.key:
                return node.val # found!
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None


    __contains__ = lookup # allow using the "in" operator to search in a tree


    def insert(self, key, val):
        ''' insert node with key,val into tree.
            if key already there, just update its value '''

        parent = None # this will be the parent of the new node
        node = self.root

        while node != None: # keep descending the tree
            if key == node.key:
                node.val = val     # update the val for this key
                return

            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if parent == None: # was empty tree, need to update root
            self.root = Tree_node(key, val)
        elif key < parent.key: 
            parent.left = Tree_node(key, val) # "hang" new node as left child

        else:  
            parent.right = Tree_node(key, val) # "hang"    ...     right child

        self.size += 1
        return None

    
    def minimum(self):
        ''' return value of node with minimal key '''
        
        if self.root == None:
            return None # empty tree has no minimum
        node = self.root
        while node.left != None:
            node = node.left
        return node.val


    def depth(self):
        ''' return depth of tree, uses recursion '''
        
        def depth_rec(node):
            if node == None:
                return -1
            else:
                return 1 + max(depth_rec(node.left), depth_rec(node.right))

        return depth_rec(self.root)




def test():
    t = Binary_search_tree() 
    t.insert(5,"a")
    t.insert(2,"b")
    t.insert(3,"c")
    t.insert(7,"d")
    t.insert(8,"e")
    t.insert(2,"bbb") # no node added, just update value
    print(t)
    print(5 in t) #calls __contains__
    print("MIN ",t.minimum())
    print("DEPTH ",t.depth())
    







