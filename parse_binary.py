"""
Author: Emmanuel Kwakye Baah
Description: This is mini-parser for demonstrating data extraction from binary files. 
This parser is specifically adapted to reading a device data from a binary file.
It may however be applicable to reading device identification data files that conform with the  
American National Standard for device data.
"""

from binascii import hexlify
import json 
import getopt
import sys


file_path = "binary.dat"


#   Read raw data
def read_raw(file=file_path):
    with open(file,"rb") as bin_file:
        # Read line from file
        lines  =  bin_file.readline()
        # Split data into list based on hex notation
        raw_data = str(lines).split("\\x")
    return raw_data  

# Read formatted data 
def read_formatted(file=file_path,response={}):
    """This function reads the formatted version of the provided binary file data

    Args:
        file (_type_, optional): File path. This file hold the desired device information. Defaults to file_path.
        response (dict, optional): dictionary to hold response. Defaults to {}.

    Returns:
        dict: this holds the key-value pairs of words and their corresponding values 
    """
    with open(file,"rb") as bin_file:
        # Read line from file
        line  =  bin_file.readline()
        # Convert data to hex values
        # Group by 4 bytes
        # Split by each group
        data =  hexlify(line,sep=" ",bytes_per_sep=2).decode().split(" ")
        for index,hex_val in enumerate(data):
            # Convert hex values to int 
            # val_1 = int(hex_val[0:2],16)
            # val_2 = int(hex_val[2:],16)
            # Slice hex string into required decodable format
            val_1 = hex_val[0:2]
            val_2 = hex_val[2:]
            # Append the char value of the corresponding word to a dictionary
            response.update({f"word_{index}":f"{val_1}{val_2}"})
            # print(f"word_num:{index}\thex_val:{hex_val}\tchar_val:{chr(int_val_1)}{chr(int_val_2)} ")    
    return response

# Read range of words
def read_range(start,stop):
    response = read_formatted()
    range= list(response.values())[int(start):int(stop)]
    # print(range)
    return range


# Start Program
def main(argv):
    MODE = ""
    START = 0
    STOP = 0
    # Get command line arguements
    try:
        opts, args = getopt.getopt(argv, "hxas:p:", ["start=", "stop="])
        print(opts)
    except getopt.GetoptError:
        print(f"USAGE: parse_binary.py -a -s 0  or -p 4")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(f"USAGE: parse_binary.py -a -s 0  or -p 4")
            sys.exit()
        elif opt == "-a":
            MODE = "ascii"
        elif opt == "-x":
            MODE = "hex"
        elif opt == "-s":
            START = arg
        elif opt == "-p":
            STOP = arg
        else:
            print("No mode found")
        
    return MODE, START,STOP

    
if __name__ == "__main__":
    mode,start,stop = main(sys.argv[1:])
    data = read_range(start,stop)
    print(data)
    response = ""
    if mode == 'ascii':
        for c in data:
            c1 = int(c[0:2],16)
            c2 = int(c[2:],16)
            response = response+ chr(c1) + chr(c2)
    if mode == "hex":
        data = "".join(data)
        # print(data)
        hex_data = int(data,16)
        response  = bin(hex_data)[2:].zfill(len(data)*4)
    # print(json.dumps(response))
    print(response)
