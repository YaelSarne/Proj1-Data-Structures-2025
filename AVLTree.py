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
		self.left = None if key is None else AVLNode()
		self.right = None if key is None else AVLNode()
		self.parent = None
		self.height = -1 if key is None else 0
		self.BF = 0
	
	def __repr__(self):
		return "(" + str(self.key) + ":" + str(self.value) + ")"

		
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
		self._size = 0 

	
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


	def fix_node_attr(self, node): 
		"""Fix node height + BF"""
		left_h = node.left.height
		right_h = node.right.height
		node.height = 1 + max(left_h, right_h)
		node.BF = left_h - right_h

	def right_rotation(self, B):
		A = B.left
		B.left = A.right
		B.left.parent = B
		A.right = B
		A.parent = B.parent
		if A.parent == None:
			self.root = A
		elif B.parent.right == B:
			A.parent.right = A # check if root
		else:
			A.parent.left = A
		B.parent = A

		self.fix_node_attr(B)
		self.fix_node_attr(A)

	def left_rotation(self, B):
		A = B.right
		B.right = A.left
		B.right.parent = B
		A.left = B
		A.parent = B.parent
		if A.parent == None:
			self.root = A
		elif B.parent.right == B:
			A.parent.right = A # check if root
		else:
			A.parent.left = A
		B.parent = A
		
		self.fix_node_attr(B)
		self.fix_node_attr(A)


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		node = self.root
		while node != None and node.is_real_node():
			if key == node.key:
				return node 
			elif key < node.key:
				node = node.left
			else:
				node = node.right
		return None


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
		parent = None # this will be the parent of the new node
		node = self.root

		# Find place for insert
		while node != None and node.is_real_node():
			# keep descending the tree
			if key == node.key:
				node.value = val     # update the val for this key
				break
			
			parent = node
			if key < node.key:
				node = node.left
			else:
				node = node.right

		# fix AVL Tree
		height_changed = False

		if parent == None: # was empty tree, need to update root
			self.root = AVLNode(key, val)
			parent = self.root
			height_changed = True #when it doesn't exist it's -1, now it's 0

		elif key < parent.key: 
			parent.left = AVLNode(key, val) # "hang" new node as left child
			parent.left.parent = parent #update the new node parents
			if not parent.right.is_real_node():
				parent.height += 1
				height_changed = True
		else:
			parent.right = AVLNode(key, val) # "hang"    ...     right child
			parent.right.parent = parent
			if not parent.right.is_real_node():
				parent.height += 1
				height_changed = True

		rotation_cnt = self.rebalance_upward(parent, height_changed)
		
		self._size += 1
		return rotation_cnt # need to return number of rotations

	def rebalance_upward(self, parent, height_changed):
		rotation_cnt = 0
		while parent != None and parent.is_real_node():
			old_height = parent.height
			self.fix_node_attr(parent)

			if old_height != parent.height:
				height_changed = True

			abs_BF = abs(parent.BF)
			if abs_BF < 2 and not height_changed:
				return 0 # IS THIS REALLY WHAT WE NEED TO RETURN? NO GILGULIM
			elif abs_BF < 2 and height_changed:
				parent = parent.parent
			elif abs_BF == 2:
				#GILGULIM!!!!!!
				if parent.BF == -2:
					if parent.right.BF == -1:
						self.left_rotation(parent)
						rotation_cnt += 1

					elif parent.right.BF == 1:
						self.right_rotation(parent.right) #first we do a right rotation on the right son
						self.left_rotation(parent)
						rotation_cnt += 2

				elif parent.BF == 2:
					if parent.left.BF == 1:
						self.right_rotation(parent)
						rotation_cnt += 1

					elif parent.left.BF == -1: 
						self.left_rotation(parent.left) 
						self.right_rotation(parent)
						rotation_cnt += 2

				parent = parent.parent
			height_changed = False
		return rotation_cnt


	def Min(self, node):
		"""Find Min value in sub tree of node"""
		while node.left.is_real_node():
			node = node.left
		return node
	
	def successor(self, node):
		"""Find successor of node"""
		# node has right child
		if node.right != None and node.right.is_real_node():
			return self.Min(node.right)
		
		# successor is the lowest ancestor y of x Such that x is in its left tree
		y = node.parent
		while (y != None and y.is_real_node()) and (node == y.right):
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
		if parent is None: # node is root
			self.root = None
		elif parent.left == node:
			parent.left = AVLNode() 
		else:
			parent.right = AVLNode()
		return parent

	def remove_single_child(self, node):
		# Case 2: node deleted has only 1 child
		parent = node.parent
		child = node.left if node.left.is_real_node() else node.right
		child.parent = parent
		if parent is None: #node is root
			self.root = child
		elif parent.left == node: 
			parent.left = child
		else:
			parent.right = child
		return parent 
	
	def delete(self, node):
		parent = node.parent
		rotation_cnt = 0

		# Case 1: node deleted is a leaf
		if not node.left.is_real_node() and not node.right.is_real_node():
			parent = self.remove_leaf(node)
		# Case 2: node deleted has only 1 child - bypass it (connect parent and child)

		elif not node.left.is_real_node() or not node.right.is_real_node():
			parent = self.remove_single_child(node)

		# Case 3: node deleted has 2 child : replace with sucssor
		else:
			# y = successor of the node
			successor = self.successor(node)
			# replace x by y :
			node.key, node.value = successor.key, successor.value
			# delete the node y was physicly - y has no left child and it will be case 2 or 1
			if successor.right.is_real_node():
				parent = self.remove_single_child(successor)
			else:
				parent = self.remove_leaf(successor)

		# Rebalance from the parent upward
		rotation_cnt += self.rebalance_upward(parent, True)
		self._size += -1
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
		return None