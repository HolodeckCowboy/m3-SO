class FileSystem:

    def __init__(self):
        pass

class Node:
  def __init__(self, data):
    self.data = data
    self.left = None
    self.right = None
    self.is_parent = False

#TODO Apagar um diretóro parent deve apagar todas as children