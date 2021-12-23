#!/usr/bin/env python3
import argparse
def __main__():
    parser = argparse.ArgumentParser(
        description='Adds New topologies to gromacs topology file')
    parser.add_argument(
                        '--top_file', default=None,
                        help="System topology input")
    parser.add_argument(
                        '--insertingmol_file', default=None,
                        help="Inserting topology input")
    parser.add_argument(
                        '--out', default=None,
                        help='Path to output')
    args = parser.parse_args()

    #extracts the atom types from the new molecules and puts them in a new file
    inFile = open(args.insertingmol_file)
    outFile = open("nonbondparam.top", "w")
    buffer = []
    for line in inFile:
        if line.startswith(";name"):
            buffer = ['']
        elif line.startswith("[ moleculetype ]"):
            outFile.write("".join(buffer))
            buffer = []
        elif buffer:
            buffer.append(line)
    inFile.close()
    outFile.close()
    
    
    #extracts the molecule types (rest of the force field parameters) and puts them in a new file
    inFile = open(args.insertingmol_file)
    outFile = open("bondparam.top", "w")
    for line in inFile:
        if line.startswith("[ moleculetype ]"):
            buffer = ["\n[ moleculetype ]\n"]
        elif line.startswith("[ system ]"):
            outFile.write("".join(buffer))
            buffer = []
        elif buffer:
            buffer.append(line)
    inFile.close()
    outFile.close()


    # with the extracted info from the inserting molecule above, we can now
    # add these sections respectively to the topology file for the 
    # system we are populating with gmx insert-molecules
    with open(args.out, 'w') as fh_out:
        with open(args.top_file, 'r') as fh:
            #these two short loop takes care of adding the atom types and molecule types.
            for line in fh:
                fh_out.write(line)
                if ';name   bond_type' in line:
                    for contents in open("nonbondparam.top"):
                        fh_out.write(contents)
                    break
            for line in fh:
                if '[ system ]' in line:
                    fh_out.write("\n; Begin NewTopologyInfo\n")
                    for contents in open("bondparam.top"):
                        fh_out.write(contents)
                    fh_out.write("; end NewTopologyInfo\n\n")
                    fh_out.write(line)
                    break
                fh_out.write(line)
            for line in fh:
                fh_out.write(line)
           
if __name__ == "__main__":
    __main__()
