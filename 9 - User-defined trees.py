"""
Assignment 9, by Leonardo Blas.
08/04/2019.
In this assignment we will implement the general tree classes FhSdTreeNode,
FhSdTree, FhSdDataTreeNode and FhSdDataTree.
"""
import copy


def main():
    """
    ORIGINAL TEST
    # instantiate a "data" tree of strings
    scene_tree = FhSdDataTree(str)

    scene_tree.add_child_to_cur("room")

    # add three objects to the scene tree
    scene_tree.find("room")
    scene_tree.add_child_to_cur("Lily the canine")
    scene_tree.add_child_to_cur("Miguel the human")
    scene_tree.add_child_to_cur("table")

    # add some parts to Miguel
    scene_tree.find_in_cur_subtree("Miguel the human")
    scene_tree.add_child_to_cur("torso")

    # Miguel's arms
    scene_tree.find_in_cur_subtree("torso")
    scene_tree.add_child_to_cur("left arm")
    scene_tree.add_child_to_cur("right arm")

    # add things Miguel's left arm (only one in room)
    scene_tree.find("left arm")
    scene_tree.add_child_to_cur("left hand")

    # for variety, we won't label fingers left/right
    scene_tree.find_in_cur_subtree("left hand")
    scene_tree.add_child_to_cur("thumb")
    scene_tree.add_child_to_cur("index finger")
    scene_tree.add_child_to_cur("middle finger")
    scene_tree.add_child_to_cur("ring finger")
    scene_tree.add_child_to_cur("pinky")

    # add things Miguel's right arm (only one in room)
    scene_tree.find("right arm")
    scene_tree.add_child_to_cur("right hand")

    # for variety, we won't label fingers left/right
    scene_tree.find_in_cur_subtree("right hand")
    scene_tree.add_child_to_cur("thumb")
    scene_tree.add_child_to_cur("index finger")
    scene_tree.add_child_to_cur("middle finger")
    scene_tree.add_child_to_cur("ring finger")
    scene_tree.add_child_to_cur("pinky")

    # add some parts to Lily
    scene_tree.find("Lily the canine")
    scene_tree.add_child_to_cur("torso")

    # we are careful to add to Liliy's "torso" not Miguel's
    scene_tree.find_in_cur_subtree("torso")
    scene_tree.add_child_to_cur("right front paw")
    scene_tree.add_child_to_cur("left front paw")
    scene_tree.add_child_to_cur("right rear paw")
    scene_tree.add_child_to_cur("left rear paw")
    scene_tree.add_child_to_cur("spare mutant paw")
    scene_tree.add_child_to_cur("wagging tail")

    # add some parts to table
    scene_tree.find("table")
    scene_tree.add_child_to_cur("north east leg")
    scene_tree.add_child_to_cur("north west leg")
    scene_tree.add_child_to_cur("south east leg")
    scene_tree.add_child_to_cur("south west leg")

    # test of deep copy and low-level node protection -----------------------
    my_copy = copy.deepcopy(scene_tree)

    # remove some real and imagined parts from original
    scene_tree.remove("spare mutant paw")
    scene_tree.remove("Miguel the human")
    scene_tree.remove("an imagined higgs boson")

    # remove and add some parts of copy and compare with original
    my_copy.remove("left rear paw")
    my_copy.find("Miguel the human")
    my_copy.add_child_to_cur("head")
    my_copy.find_in_cur_subtree("torso")
    my_copy.remove_at_cur()

    # add a few items to each tree
    my_copy.find("table")
    my_copy.add_child_to_cur("vase")
    my_copy.reset_cur()
    my_copy.add_child_to_cur("person viewing vase")

    scene_tree.find("table")
    scene_tree.add_child_to_cur("fruit bowl")
    scene_tree.reset_cur()
    scene_tree.add_child_to_cur("person viewing fruit")

    # low-level but LEGAL attempt to "set orig cur" then add pencil to table
    print(scene_tree.find("table"))
    orig_cur = scene_tree.current
    scene_tree.reset_cur()
    scene_tree.current = orig_cur  # manually overwrite current
    print(scene_tree.add_child_to_cur("#2 pencil"))

    # low-level ILLEGAL attempt to "set orig cur" then add pen to table
    print(my_copy.find("table"))
    my_copy_cur = my_copy.current
    scene_tree.reset_cur()
    scene_tree.current = my_copy_cur  # contaminate scene_tree
    print(scene_tree.add_child_to_cur("monte blanc pen"))
    print()

    print("ORIGNIAL, after removing miguel and the mutant paw \n"
          + "and adding fruit,  person to view fruit and #2 pencil:\n"
          + str(scene_tree))
    print("COPY, after removing miguel's torso and Lily's left rear\n"
          + "and adding vase and person to view vase:\n"
          + str(my_copy))
    """

    # NEW MAIN
    # instantiate a "data" tree of strings
    scene_tree = FhSdDataTree(str)

    print("Starting tree empty? " + str(scene_tree.empty()))

    scene_tree.add_child_to_cur("1")

    # add three objects to the scene tree
    scene_tree.find("1")
    scene_tree.add_child_to_cur("2")
    scene_tree.add_child_to_cur("3")
    scene_tree.add_child_to_cur("4")

    # add some parts to Miguel
    scene_tree.find_in_cur_subtree("Miguel the human")
    scene_tree.add_child_to_cur("torso")

    print("\n------------ Loaded Tree --------------- \n", scene_tree)

    # test of deep copy and soft deletion --------------------------
    my_copy = copy.deepcopy(scene_tree)




class FhSdTreeNode:
    """ FhSdTreeNode class for a FhSdTree - not designed for
        general clients, so no accessors or exception raising """

    # initializer ("constructor") method ------------------------
    def __init__(self,
                 sib=None,
                 first_child=None,
                 prev=None,
                 root=None,
                 dltd=False):
        # instance attributes
        self.sib, self.first_child, self.prev, self.my_root, self.dltd \
            = sib, first_child, prev, root, dltd

    def __str__(self):
        return "(generic tree node)"


class FhSdTree:
    """ FhSdTree is our base class for a data-filled general trees """

    # static constant helpers for stringizer
    BLANK_STRING = "                                    "
    BLANK_STR_LEN = len(BLANK_STRING)

    def __init__(self):
        self.clear()

    def empty(self):
        """ traditionally, is_empty() is just called empty() """
        return self.size() == 0

    def size_rec(self, tree_node, level=0):
        ret_size = 0
        if tree_node is not None:
            if not tree_node.dltd:
                ret_size += 1
                ret_size += self.size_rec(tree_node.first_child, level + 1)
            if level > 0:
                ret_size += self.size_rec(tree_node.sib, level)
        return ret_size

    def size(self):
        """ traditionally, get() for size is just siae() """
        return self.size_rec(self.m_root)

    def size_physical(self):
        return self.m_size

    def reset_cur(self):
        self.current = self.m_root

    def set_cur(self, tree_node):
        if not self.valid_node_in_tree(tree_node) \
                or tree_node.dltd:
            self.current = None
            return False
        # else
        self.current = tree_node
        return True

    def clear(self):
        self.m_root = None
        self.m_size = 0
        self.reset_cur()

    def remove_node_rec(self, node_to_delete):
        """ node_to_delete points to node in tree to be removed
            (along w/entire subtree). deletes children recursively
            errors handled by caller (remove_at_cur()) """

        ntd = node_to_delete  # alias for shorter lines
        # remove all the children of this node (need loop unfortunately)
        while ntd.first_child:
            self.remove_node_rec(ntd.first_child)

        # we have a non-null prev pointer
        # either it has a left sib ...
        if ntd.prev.sib == node_to_delete:
            ntd.prev.sib = node_to_delete.sib
        # ... or it's the first_child of some parent
        else:
            ntd.prev.first_child = ntd.sib

        # deal with a possible right sib
        if ntd.sib != None:
            ntd.sib.prev = ntd.prev

        # node is now out of the tree (Python will g.c. if appropriate)
        # wipe the fields to prevent client from doing harm
        ntd.first_child, ntd.prev, ntd.sib, ntd.my_root \
            = None, None, None, None

        # finally, update tree size
        self.m_size -= 1

    def remove_at_cur(self):
        """ calls remove_node() passing cur, and resets cur
           handles all errors here to avoid repetition in rec call """

        ntd = self.current  # saves cur so we can reset early
        self.reset_cur()  # no matter what, we'll return fresh cur

        # bad current or empty tree
        if not self.valid_node_in_tree(ntd) \
                or self.size() == 0 \
                or ntd.dltd:
            return False

        # deleting root?
        if ntd is self.m_root:
            self.clear()
            return True

        ntd.dltd = True
        return True

    def add_child_node_to_cur(self, to_add=None):
        """ 'push' node_to_add as new first child of parent.
             return None (error) or ref to newly created node
             expect parent == None IFF tree is empty """

        if not self.valid_node_to_add(to_add) \
                or to_add.dltd:
            return False

        # empty tree
        if self.m_size == 0:
            self.m_root = to_add
            self.m_root.my_root = self.m_root
            self.m_size = 1
            self.reset_cur()  # for empty tree we ignore what cur *was*
            return True

        if not self.valid_node_in_tree(self.current):
            return False

        # "push" new_node as the head of the sibling list; adjust all ptrs
        # notice "None": any "subtree: hanging off to_add, is trimmed
        cur = self.current  # for brevity...
        ta = to_add  # ... of next block

        ta.sib, ta.first_child, ta.prev, ta.my_root \
            = cur.first_child, None, cur, self.m_root
        cur.first_child = ta
        if ta.sib != None:
            ta.sib.prev = ta
        self.m_size += 1
        return True

    def valid_node_to_add(self, am_i_valid):
        """ insists that node is an FhSdTreeNode """
        if not isinstance(am_i_valid, FhSdTreeNode):
            return False
        return True

    def valid_node_in_tree(self, am_i_valid):
        """ insists that node is an FhSdTreeNode AND in this tree """
        if (not isinstance(am_i_valid, FhSdTreeNode)) \
                or (am_i_valid.my_root != self.m_root):
            return False
        return True

    def collect_garbage(self):
        return self.collect_garbage_rec(self.m_root)

    def collect_garbage_rec(self, tree_node):
        ret_bool = False
        if self.valid_node_in_tree(tree_node):
            if tree_node.first_child is not None:
                ret_bool = self.collect_garbage_rec(tree_node.first_child)
            if tree_node.sib is not None:
                ret_bool = self.collect_garbage_rec(tree_node.sib)
            if tree_node.dltd:
                self.remove_node_rec(tree_node)
                ret_bool = True

        return ret_bool

    def str_recurse_phys(self, tree_node, level=0):
        """ recursive tree stringizer (with indentation)
            for subtree with root tree_node in this instance's tree """

        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if self.valid_node_in_tree(tree_node):
            # stop runaway indentation, otherwise set indent for this level
            if level > self.BLANK_STR_LEN - 1:
                return self.BLANK_STRING + " ... "

            # this call's node
            indent = self.BLANK_STRING[0:level]
            deleted_flag = ''
            if tree_node.dltd:
                deleted_flag = ' (D)'

            ret_str += (indent + str(tree_node) + deleted_flag + "\n")

            # recurse over children
            ret_str += self.str_recurse_phys(tree_node.first_child, level + 1)

            # recurse over siblings
            if level > 0:
                ret_str += self.str_recurse_phys(tree_node.sib, level)

        return ret_str

    def str_physical(self):
        ret_str = "The Actual Tree -----------------------\n" \
                  + self.str_recurse_phys(self.m_root, 0) \
                  + "---------- End of Tree --------\n"

        return ret_str

    def str_recurse(self, tree_node, level=0):
        """ recursive tree stringizer (with indentation)
            for subtree with root tree_node in this instance's tree """

        ret_str = ""

        # multi-purpose termination:  error, None or not-in-self
        if not self.valid_node_in_tree(tree_node):
            return ret_str

        # stop runaway indentation, otherwise set indent for this level
        if level > self.BLANK_STR_LEN - 1:
            return self.BLANK_STRING + " ... "

        if not tree_node.dltd:
            indent = self.BLANK_STRING[0:level]
            ret_str += (indent + str(tree_node) + "\n")
            ret_str += self.str_recurse(tree_node.first_child, level + 1)

        # recurse over siblings
        if level > 0:
            ret_str += self.str_recurse(tree_node.sib, level)

        return ret_str

    def __str__(self):
        ret_str = "The Tree -----------------------\n" \
                  + self.str_recurse(self.m_root, 0) \
                  + "---------- End of Tree --------\n"

        return ret_str


class FhSdDataTreeNode(FhSdTreeNode):
    """ FhSdDataTreeNode subclass of FhSdTreeNode.
    It is the node class for a data tree.
    Requires data item, x, be vetted by client (FhSdDataTree) """

    def __init__(self, x,
                 sib=None,
                 first_child=None,
                 prev=None,
                 root=None,
                 dltd=False):
        # first chain to base class
        super().__init__(sib, first_child, prev, root, dltd)

        # added attribute
        self.data = x

    # ultimate client, main(), can provide data stringizer if needed
    def __str__(self):
        return str(self.data)


class FhSdDataTree(FhSdTree):
    """ FhSdDataTree subclass of FhSdTree """
    # default type is string
    DEFAULT_TYPE = type("")

    def __init__(self, tree_type=None):
        super().__init__()
        self.set_tree_type(tree_type)

    # current pointer mutators --------------------------------------
    def find(self, x):
        """ look for x in entire tree.
            if found and valid, current will point to it and return T,
            else current None and return F (all done by find_rec())"""

        self.reset_cur()
        return self.find_in_cur_subtree(x)

    def find_in_cur_subtree(self, x):
        """ look for x in subtree rooted at self.current.
           if x valid and found, current will point to it and return T,
           else current None and return F """

        if not self.current or not self.valid_data(x):
            return False

        return self.find_rec(x, self.current) is not None

    def find_rec(self, x, root):
        """ recursively search for x in subtree rooted at root.
           if found, current set to node and returned,
           else current/return = None.
           x and current vetted by non-recursive originator """

        # default current if all recursive calls fail
        self.current = None

        # not found (in this sub-search)
        if root and not root.dltd:
            # found (current will survive all higher-level calls)
            if root.data == x:
                self.current = root
                return root

            # recurse children
            child = root.first_child
            while child:
                test_result = self.find_rec(x, child)
                if test_result:
                    return test_result
                child = child.sib

        return None

    # tree mutators --------------------------------------------------
    def set_tree_type(self, the_type):
        # make sure it's a subclass of type
        if isinstance(the_type, type):
            self.tree_type = the_type
        else:
            self.tree_type = self.DEFAULT_TYPE

    def remove(self, x):
        """ looks for x in entire tree.
           if valid and found, remove node, return T (cur reset by base
           call, remove_at_cur()). else curr = None and return F """

        self.current = None  # prepare for not found or error return
        if self.size() == 0 or (not self.valid_data(x)):
            return False

        found_node = self.find_rec(x, self.m_root)
        if not found_node:
            return False

        # found x
        self.current = found_node
        self.remove_at_cur()  # not overriden, so base call
        return True

    def add_child_to_cur(self, x):
        """ calls base add_child_node_to_cur(). no change to cur """
        if not self.valid_data(x):
            return False

        new_node = FhSdDataTreeNode(x)
        return (super().add_child_node_to_cur(new_node))

    # helpers -------------------------------------------------
    def valid_data(self, am_i_valid):
        if not isinstance(am_i_valid, self.tree_type):
            return False
        # else
        return True


if __name__ == "__main__":
    main()

"""
OLD MAIN:

True
True
True
False

ORIGNIAL, after removing miguel and the mutant paw 
and adding fruit,  person to view fruit and #2 pencil:
The Tree -----------------------
room
 person viewing fruit
 table
  #2 pencil
  fruit bowl
  south west leg
  south east leg
  north west leg
  north east leg
 Lily the canine
  torso
   wagging tail
   left rear paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------

COPY, after removing miguel's torso and Lily's left rear
and adding vase and person to view vase:
The Tree -----------------------
room
 person viewing vase
 table
  vase
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human
  head
 Lily the canine
  torso
   wagging tail
   spare mutant paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


Process finished with exit code 0


CURRENT MAIN:

Starting tree empty? True

------------ Loaded Tree --------------- 
 The Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human
  torso
   right arm
    right hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
   left arm
    left hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
 Lily the canine
  torso
   wagging tail
   spare mutant paw
   left rear paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


----------- Virtual Tree ------------ 
 The Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Lily the canine
---------- End of Tree --------


----------- Physical Tree ------------ 
 The Actual Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human (D)
  torso
   right arm
    right hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
   left arm
    left hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
 Lily the canine
  torso (D)
   wagging tail
   spare mutant paw (D)
   left rear paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


----------- Miguel and Torso should be gone ------------ 

good
good
good
good

------- Testing Sizes (compare with above) ------ 


virtual (soft) size: 7

physical (hard) size: 30

------------ Collecting Garbage ------------ 

found soft-deleted nodes? True
immediate collect again? False
-------- Hard Display after garb col ----------
 The Actual Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Lily the canine
---------- End of Tree --------

Semi-deleted tree empty? False
Completely-deleted tree empty? True

------------ Cloned Tree? ------------ 


----------- Virtual Tree ------------ 
 The Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human
  head
 Lily the canine
  torso
   wagging tail
   spare mutant paw
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


----------- Physical Tree ------------ 
 The Actual Tree -----------------------
room
 table
  south west leg
  south east leg
  north west leg
  north east leg
 Miguel the human
  head
  torso (D)
   right arm
    right hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
   left arm
    left hand
     pinky
     ring finger
     middle finger
     index finger
     thumb
 Lily the canine
  torso
   wagging tail
   spare mutant paw
   left rear paw (D)
   right rear paw
   left front paw
   right front paw
---------- End of Tree --------


------- Testing Sizes (compare with above) ------ 


virtual (soft) size: 15

physical (hard) size: 31

------------ Testing find() ------------ 

good
good
good
good
good
good
good

Process finished with exit code 0


"""
