
import os

class Value:
    def __init__(self,val=None):
        self.candle = val
        self.next = None


class OHLC_store:

    def __init__(self):
        self.head_ptr = None
        pass

    def add(self,data):
        if self.head_ptr == None:
            self.head_ptr = Value(data)
        else:
            temp = self.head_ptr
            self.head_ptr = Value(data)
            self.head_ptr.next = temp

    def clear_console(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def print_data(self,):
        self.clear_console()
        temp = self.head_ptr
        while temp is not None:
            print(temp.candle)
            temp = temp.next