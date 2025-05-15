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
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = 0
		self.BF = 0 #not sure about this
	
	def __repr__(self):
		return "(" + str(self.key) + ":" + str(self.val) + ")"

		
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



	def right_rotation(self, B):
		A = B.left
		B.left = A.right
		if A.right != None:
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


	#B has to have a B.right.left son
	def left_rotation(self, B):
		A = B.right
		B.right = A.left
		if A.left != None:
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





	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		node = self.root
		while node != None:
			if key == node.key:
				return node.val # found!
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

		while node != None: # keep descending the tree
			if key == node.key:
				node.val = val     # update the val for this key
				break
			
			parent = node
			if key < node.key:
				node = node.left
			else:
				node = node.right

		height_changed = False

		if parent == None: # was empty tree, need to update root
			self.root = AVLNode(key, val)
			parent = self.root
			height_changed = True

		elif key < parent.key: 
			parent.left = AVLNode(key, val) # "hang" new node as left child
			if parent.right is None:
				parent.height += 1
				height_changed = True
		else:  
			parent.right = AVLNode(key, val) # "hang"    ...     right child
			if parent.left is None:
				parent.height += 1
				height_changed = True
		
		left_son_height = -1 if parent.left is None else parent.left.height
		right_son_height = -1 if parent.right is None else parent.right.height
		parent.BF = left_son_height - right_son_height
		rotation_cnt = 0

		while parent != None:
			abs_BF = abs(parent.BF) 
			if abs_BF < 2 and not height_changed:
				return 0 # IS THIS REALLY WHAT WE NEED TO RETURN? NO GILGULIM
			elif abs_BF < 2 and height_changed:
				parent = parent.parent
			else:
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

		
		#self.size += 1
		#return None
		return rotation_cnt # need to return number of rotations


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		return -1


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
		return -1	


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