#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  

"""A class represnting a node in an AVL tree"""
class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.height = -1 if key is None else 0 # Height of a virtual node is -1, real node 0
        self.BF = 0 # Balance Factor for a newly created real node (leaf) is 0

        # If it's a real node, its children are initially virtual nodes.
        # If it's a virtual node (key is None), its children are None.
        if key is not None:
            self.left = AVLNode() # Virtual child
            self.right = AVLNode() # Virtual child
        else:
            self.left = None # Virtual node has no children
            self.right = None # Virtual node has no children

    def __repr__(self):
        # A more robust __repr__ for debugging that handles virtual nodes nicely
        if self.is_real_node():
            return f"({self.key}:{self.BF})"
        return "V" # Representation for a virtual node
        
    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""
class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.  
    """
    def __init__(self):
        self.root = None
        self.max_node = None # Stores the node with the maximum key
        self._size = 0 
        self.bf_zero_cnt = 0 # Counter for nodes with BF = 0

    def __repr__(self):  # you don't need to understand the implementation of this method
        def printree(root):
            # Ensure we only try to print real nodes, or represent virtual as '#'
            if not root or not root.is_real_node():
                return ["#"]

            # Simplified root_key and calculation for visual spacing
            root_key = str(root.key) + ":" + str(root.BF)
            left_lines = printree(root.left)
            right_lines = printree(root.right)

            lwid = len(left_lines[-1])
            rwid = len(right_lines[-1])
            rootwid = len(root_key)
            
            result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]
            
            ls = len(left_lines[0].rstrip())
            rs = len(right_lines[0]) - len(right_lines[0].lstrip())
            result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")
            
            for i in range(max(len(left_lines), len(right_lines))):
                row = ""
                if i < len(left_lines):
                    row += left_lines[i]
                else:
                    row += lwid * " "
                row += (rootwid + 2) * " " 

                if i < len(right_lines):
                    row += right_lines[i]
                else:
                    row += rwid * " "
                result.append(row)
            return result

        return '\n'.join(printree(self.root))


    def fix_node_attr(self, node): 
        """Fix node height + BF. Assumes node is a real node."""
        if not node or not node.is_real_node(): # Should not happen if called correctly
            return
        
        old_bf = node.BF # Store old BF to update bf_zero_cnt
        
        # Get height of children. Virtual nodes have height -1.
        # Ensure we check if child is not None before accessing attributes
        left_h = node.left.height if node.left is not None and node.left.is_real_node() else -1
        right_h = node.right.height if node.right is not None and node.right.is_real_node() else -1
        
        node.height = 1 + max(left_h, right_h)
        node.BF = left_h - right_h
        
        self.update_zero_count(old_bf, node.BF)


    def update_zero_count(self, old_bf, new_bf):
        """Updates the count of nodes with BF = 0."""
        if old_bf == 0 and new_bf != 0:
            self.bf_zero_cnt -= 1
        elif old_bf != 0 and new_bf == 0:
            self.bf_zero_cnt += 1
        

    def right_rotation(self, B):
        A = B.left
        B.left = A.right
        # Update parent for A's old right child if it's real and not None
        if B.left is not None and B.left.is_real_node():
            B.left.parent = B
        
        A.right = B
        A.parent = B.parent # A takes B's parent
        
        # Update parent's child pointer
        if A.parent is None:
            self.root = A
        elif B.parent.right == B: # B was right child
            A.parent.right = A
        else: # B was left child
            A.parent.left = A
        B.parent = A # B's new parent is A

        # Fix attributes bottom-up (B then A)
        self.fix_node_attr(B)
        self.fix_node_attr(A)
        return A # Return the new root of the rotated subtree


    def left_rotation(self, B):
        A = B.right
        B.right = A.left
        # Update parent for A's old left child if it's real and not None
        if B.right is not None and B.right.is_real_node():
            B.right.parent = B
        
        A.left = B
        A.parent = B.parent # A takes B's parent

        # Update parent's child pointer
        if A.parent is None:
            self.root = A
        elif B.parent.right == B: # B was right child
            A.parent.right = A
        else: # B was left child
            A.parent.left = A
        B.parent = A # B's new parent is A
        
        # Fix attributes bottom-up (B then A)
        self.fix_node_attr(B)
        self.fix_node_attr(A)
        return A # Return the new root of the rotated subtree


    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key
    """
    def search(self, key):
        node = self.root
        while node is not None and node.is_real_node():
            if key == node.key:
                return node 
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None # Key not found


    """inserts a new node into the dictionary with corresponding key and value

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @param start: can be either "root" or "max"
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def insert(self, key, val, start="root"):
        if key is None:
            return 0
        
        # Handle empty tree case
        if self.root is None:
            self.root = AVLNode(key, val)
            self.max_node = self.root # Max node is also the root for a single-node tree
            self._size = 1
            self.bf_zero_cnt = 1 # A single node (leaf) has BF = 0
            return 0

        parent = None
        current = None

        if start == "max" and self.max_node and key > self.max_node.key:
            # Optimization: If inserting a key larger than max_node, directly go to max_node's right
            parent = self.max_node
            current = self.max_node.right # This will be a virtual node
        elif start == "root" or not self.max_node:
            # Standard traversal from root (or if max_node is not reliable/set)
            current = self.root
            # Descend to find insertion point
            while current is not None and current.is_real_node():
                parent = current
                if key == current.key: # Key already exists, update value and return 0 rotations
                    current.value = val
                    return 0
                elif key < current.key:
                    current = current.left
                else:
                    current = current.right
        else: # start == "max" but key is not strictly greater than max_node.key, fall back to root search
            return self.insert(key, val, start="root")
        
        # Create the new node
        new_node = AVLNode(key, val)
        new_node.parent = parent

        # Link new node to its parent
        if parent is None: # This case should be handled by the initial empty tree check
            self.root = new_node # Safety fallback
        elif key < parent.key:
            parent.left = new_node
        else: # key > parent.key
            parent.right = new_node
            # Update max_node if the new node is the largest
            if self.max_node is None or key > self.max_node.key: # Ensure max_node is updated correctly
                self.max_node = new_node
        
        self._size += 1
        self.bf_zero_cnt += 1 # New leaf node has BF 0
        
        # Start rebalancing from the parent of the newly inserted node
        rotation_cnt = self.rebalance_upward(new_node.parent, "insert")
        
        return rotation_cnt


    def rebalance_upward(self, node, op):
        """
        Rebalances the AVL tree upwards from a given node.
        
        Parameters:
        node (AVLNode): The node to start rebalancing from (typically parent of inserted/deleted node).
        op (str): "insert" or "delete", to determine rebalancing behavior.
        
        Returns:
        int: The number of rotations performed.
        """
        rotation_cnt = 0
        current_node = node

        while current_node is not None and current_node.is_real_node():
            old_height = current_node.height
            old_bf = current_node.BF # Store old BF for update_zero_count

            # Update height and BF of current_node based on its children's *current* states
            self.fix_node_attr(current_node)

            # Determine if height changed at THIS level
            height_changed_this_level = (old_height != current_node.height)

            abs_BF = abs(current_node.BF)
            if abs_BF < 2: # Balance Factor is within AVL limits (-1, 0, 1)
                if op == "insert" and not height_changed_this_level:
                    # For insertion, if BF is fine and height didn't change, we're done.
                    return rotation_cnt
                # For deletion, if BF is fine but height didn't change, we're done (no more propagation needed).
                # If height did change (e.g., a branch shrunk), we need to continue upwards.
                elif op == "delete" and not height_changed_this_level:
                    return rotation_cnt
                
                # Continue upwards
                current_node = current_node.parent 
            elif abs_BF == 2: # Balance Factor is problematic, needs rotation
                # Perform rotations
                if current_node.BF == -2: # Right heavy
                    if current_node.right.BF == -1 or (op == "delete" and current_node.right.BF == 0):
                        rotated_node = self.left_rotation(current_node)
                        rotation_cnt += 1
                    elif current_node.right.BF == 1: # LR Rotation
                        self.right_rotation(current_node.right) # First rotation
                        rotated_node = self.left_rotation(current_node) # Second rotation
                        rotation_cnt += 2
                    else: # This case should ideally not happen if BF is maintained correctly
                        return rotation_cnt # Safety break
                elif current_node.BF == 2: # Left heavy
                    if current_node.left.BF == 1 or (op == "delete" and current_node.left.BF == 0):
                        rotated_node = self.right_rotation(current_node)
                        rotation_cnt += 1
                    elif current_node.left.BF == -1: # RL Rotation
                        self.left_rotation(current_node.left) # First rotation
                        rotated_node = self.right_rotation(current_node) # Second rotation
                        rotation_cnt += 2
                    else: # This case should ideally not happen if BF is maintained correctly
                        return rotation_cnt # Safety break
                
                # After rotation, if it's an insertion, we are done.
                if op == "insert":
                    return rotation_cnt
                
                # For deletion, rotations might reduce the height of the subtree.
                # We need to continue upwards to propagate height changes.
                # The 'rotated_node' is the new root of the just-balanced subtree.
                # We need to continue rebalancing from its parent.
                current_node = rotated_node.parent 
            
        return rotation_cnt


    def Min(self, node):
        """Find Min value in sub tree of node"""
        if not node or not node.is_real_node(): # Handle virtual nodes/None input
            return None
        while node.left is not None and node.left.is_real_node():
            node = node.left
        return node
    
    def successor(self, node):
        """Find successor of node"""
        if not node or not node.is_real_node():
            return None
        
        # If node has a right child, successor is the minimum in right subtree
        if node.right is not None and node.right.is_real_node():
            return self.Min(node.right)
        
        # Otherwise, successor is the lowest ancestor y of x such that x is in y's left subtree
        y = node.parent
        while (y is not None and y.is_real_node()) and (node == y.right):
            node = y
            y = node.parent
        return y


    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """
    def remove_leaf(self, node):
        # Case 1: node deleted is a leaf - Simply delete
        parent = node.parent
        if parent is None: # node is root and the only node
            self.root = None
        elif parent.left == node:
            parent.left = AVLNode() # Replace with a virtual node
            # Virtual nodes do NOT have a parent attribute pointing back to their "parent"
        else: # parent.right == node
            parent.right = AVLNode() # Replace with a virtual node
        return parent # Return parent for rebalancing starting point


    def remove_single_child(self, node):
        # Case 2: node deleted has only 1 real child
        parent = node.parent
        # Determine the real child (which must be real as per case description)
        child = node.left if node.left is not None and node.left.is_real_node() else node.right
        
        # Connect child to grandparent (parent of node)
        if child is not None and child.is_real_node(): # Only assign parent for real nodes
            child.parent = parent
        
        if parent is None: # If node was the root
            self.root = child
        elif parent.left == node: # If node was left child of parent
            parent.left = child
        else: # If node was right child of parent
            parent.right = child
        return parent # Return parent for rebalancing starting point


    def update_max(self, key_of_deleted_node):
        # If the tree becomes empty after deletion
        if self.root is None:
            self.max_node = None
            return

        # If the deleted node was the max_node, we need to find the new max_node
        if self.max_node and key_of_deleted_node == self.max_node.key:
            curr = self.root
            while curr is not None and curr.right is not None and curr.right.is_real_node():
                curr = curr.right
            self.max_node = curr


    def delete(self, node):
        if not node or not node.is_real_node(): # Input validation
            return 0 # Nothing to delete if node is None or virtual

        parent_for_rebalance = None # This will be the node from which rebalancing starts
        node_key_deleted = node.key # Store the key before it potentially changes (if swapped with successor)

        # Decrement bf_zero_cnt if the node being *conceptually* deleted (or its successor) had BF=0
        if node.BF == 0: # This is the node that will be removed from its position
            self.bf_zero_cnt -= 1
        
        # Determine which removal case
        if not node.left.is_real_node() and not node.right.is_real_node():
            # Case 1: node to delete is a leaf (has two virtual children)
            parent_for_rebalance = self.remove_leaf(node)
        elif not node.left.is_real_node() or not node.right.is_real_node():
            # Case 2: node to delete has only 1 real child
            parent_for_rebalance = self.remove_single_child(node)
        else: # Node has two real children - Case 3: replace with successor
            successor = self.successor(node)
            
            # If successor had BF=0 at its original position, decrement count.
            if successor.BF == 0:
                self.bf_zero_cnt -= 1 

            # Swap key and value from successor to the node being conceptually deleted
            node.key, node.value = successor.key, successor.value
            
            # Now, physically delete the successor (which is either a leaf or has only a right child)
            # The parent_for_rebalance is the parent of the *physically removed* node (the successor's old parent).
            if successor.right is not None and successor.right.is_real_node():
                parent_for_rebalance = self.remove_single_child(successor)
            else:
                parent_for_rebalance = self.remove_leaf(successor)

        self._size -= 1 # Decrement size after successful deletion
        self.update_max(node_key_deleted) # Update max_node only after size is decremented

        # Rebalance upwards from the determined parent
        rotation_cnt = self.rebalance_upward(parent_for_rebalance, "delete")
        
        return rotation_cnt

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        result = []

        def inorder(node):
            if node is None or not node.is_real_node():
                return
            inorder(node.left)
            result.append((node.key, node.value))
            inorder(node.right)
        
        inorder(self.root)
        return result
        
    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self._size


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root


    """gets amir's suggestion of balance factor

    @returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
    """
    def get_amir_balance_factor(self):
        if self._size == 0:
            return 0
        return self.bf_zero_cnt / self._size