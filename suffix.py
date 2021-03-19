'''an attempt to impliment a suffix tree for linear time genomic alignment'''


class Node:
    '''a node class that stores children nodes and a variable called letter. Note that letter can contain more than one character'''

    def __init__(self,letter,children):
        '''constructor to set instance vars '''

        '''a char or string that holds the letters of the node'''
        self.letter = letter
        '''a list that contains all the children of the particular node'''
        self.children = children
        
    def add_child(self,node):
        '''adds an additional node to the list of children for any given node'''
        self.children.append(node)
        

    def get_child(self,potential_child):
        '''returns the child node of a specific letter if it is indeeed a child, otherwise returns None, could be made faster with hashing '''
        
        #iterate over the children 
        for child in self.children:
            #check for value parity, could be cleaner with comparator overwrite 
            if child.letter  == potential_child:
                return child 
        return None 
    

    def print_subnodes(self, level=0):
        '''given an instance of a node it will print all children in a hiercical fashion, leaf nodes denoted by a *'''
        print('   ' * level + self.letter, end = "")
        print( "*") if len(self.children) == 0 else  print("\n" + '   ' * level + " " *  len(self.letter)+ "\\")
        for child in self.children:
            child.print_subnodes(level+1)
            


class Suffix_Tree:
    '''a suffix tree that is passed a string upon contstruction (from which it is constructed)'''
    def __init__(self,string):
        '''first sets an instance variable of a root with no children, and takes a string and builds out the suffix tree from the string'''
        #make a root node 
        self.root = Node("ROOT", [])
        #build out the suffix tree 
        self.build_tree(string)

    def build_tree(self,string):
        '''takes a string, collects all suffixes and then calls the add function on those suffixes. NOTE, this is non-destructive, so it can be called many times over to add 
        suffixes of a string to the same tree'''
        for i in range(1,len(string)+1):
            self.add(string[-i:])


    def add(self,suffix):
        '''does the leg work of adding an individual string to the tree.  built trees forms the suffixes and then add put them into place'''
        curr = self.root

        #iterate over the suffix
        for letter in suffix:
        #see if the current node has the letter as a child 
            child = curr.get_child(letter)
            #if it doesnt it will return none 
            if child != None:
                curr  = child
            #node we are at does not hace the next letter as a child 
            else:
                #make a new node and add it to the current nodes child 
                new_child = Node(letter, [])
                curr.add_child(new_child)
                curr = new_child


    def print_tree(self):
        '''a method to print out the tree. or more speccifically, calls print subnodes on the root '''
        self.root.print_subnodes()
        

    def compress_tree(self):
        '''calls the helper method on the root of the tree, thereby compressing the entire tree.  Any node that has strictly one child node is compressed with that childnode.
        then the children of this new compressed node and set to be the children what was the child of the node we started with.  this saves space and speeds up search time (topically) '''
        self.compress_tree_helper(self.root)

    def compress_tree_helper(self,node):
        '''a private method that does the tree compression legwork.  Adding cross links would further compress the tree, but has not been implimented yet.'''
        #if there is only one child, combine to be a single node.
        if len(node.children) == 1:
            #update the letter to be both letters
            node.letter += node.children[0].letter
            #update the children to be the children of the lower node 
            node.children = node.children[0].children  

            self.compress_tree_helper(node)
        elif len(node.children) > 1:
            for child in node.children:
                self.compress_tree_helper(child)

    def contains(self,substring):
        '''takes the given substring and checks for its presence in the tree. returns a boolean. solutions works fine if tree is compressed or not'''
        #start at the root node 
        

        #remove the matches from the substring until we either run out of things to match ( and return false) or the substring ends (return true)
        curr = self.root
        while len(substring) > 0:
            
            for child in curr.children:
                #we have a node whos string matches our substring 
                if child.letter[0] == substring[0]:
                    break
            #the entire substring is found within the letter of the child and we know the substring exsits in tree 
            if child.letter.startswith(substring):
                return True
            

            #it is possible that they have the same starting letter but the rest of the letters are not consistent 
            for char in child.letter:
                if substring[0] == char:
                    substring = substring[1:]
                else: 
                    return False
                
            #if we havent returned, we trimed down the substring but we arent at its end yet, so we must move onto the next node 
            curr = child 
        
        return True

        

def main():

    tree = Suffix_Tree("catcatcab")
    tree.compress_tree()
    tree.root.print_subnodes()
    print(tree.contains("atcatcab"))

main() 