#!/usr/bin/env python3


###  !!! EDITOR WITH CORRECT LINE NUMBER !!!  ###


import os, time



ansi = "\u001b["
red = f"{ansi}31;1m"
green = f"{ansi}32;1m"
yellow = f"{ansi}33;1m"
blue = f"{ansi}34;1m"
darkBlue = f"{ansi}34m"
reset = f"{ansi}0m"

outed = False


# defs
def execute(c):
    global a, br, ram, hdd, cF, pc, acc, outed
    
    a = int(a)
    l = [int(f"0b{c[:4]}", 2), int(f"0b{c[4:]}", 2)]  # split line in two and change each to denary
    
    if l[0] == 0:  # nop
        pass

    elif l[0] == 1:  # out
        outed = True
        print(f"{red}{a}{reset}")

    elif l[0] == 2:  # hlt
        br = True

    elif l[0] == 3:  # lha
        a = hdd[l[1]]

    elif l[0] == 4:  # lra
        a = ram[l[1]]

    elif l[0] == 5:  # svr
        ram[l[1]] = a

    elif l[0] == 6:  # svh
        hdd[l[1]] = ram[a]

    elif l[0] == 7:  # add
        x = bin(a + ram[l[1]])[2:]
        acc = int(f"0b{x[-8:]}", 2)
        a = acc
        if acc < int(x, 2):
            cF = 1

    elif l[0] == 8:  # sub
        acc = a - ram[l[1]]
        a = acc

    elif l[0] == 9:  # jmp
        pc = ram[l[1]]-1
        step()

    elif l[0] == 10:  # jmc
        if cF == 1:
            pc = ram[l[1]]-1
            step()


def decode(c):
    l = c.split()
    n = bin(int(l[1]))[2:]

    if l[0] == "nop":
        return f"0000{n}"

    elif l[0] == "out":
        return f"0001{n}"

    elif l[0] == "hlt":
        return f"0010{n}"

    elif l[0] == "lha":
        return f"0011{n}"

    elif l[0] == "lra":
        return f"0100{n}"

    elif l[0] == "svr":
        return f"0101{n}"

    elif l[0] == "svh":
        return f"0110{n}"

    elif l[0] == "add":
        return f"0111{n}"

    elif l[0] == "sub":
        return f"1000{n}"

    elif l[0] == "jmp":
        return f"1001{n}"

    elif l[0] == "jmc":
        return f"1010{n}"


def step():
    global pc, mar, mdr, ir, i

    pc += 1  # pc increments
    mar = pc  # mar copies pc
    mdr = hdd[mar]  # mdr gets instruction from memory (fetch)
    ir = mdr  # ir copies mdr

    i = decode(ir)  # decode ir instruction (decode)
    execute(i)  # execute instruction (execute)



def clear():  # clear based on os
    if os.name == "windows":
        os.system("cls")
    else:
        os.system("clear")



def menu():  # main menu
    errMes = f"\n{red}That's not an option - try again{reset}"
    
    clear()
    print(f"{darkBlue}MENU{reset}\n\n{blue}Options:{reset}\n1. Run a program\n")
    while True:
        ch = input("> ")
        if ch == "1":
            files = os.listdir("./hdds")

            clear()
            print(f"{darkBlue}MENU{reset}\n")
            print(f"Which file do you want to load?\n{blue}Options:{reset}")
            for i in range(len(files)):
                print(f"{i+1}. {files[i]}")
            print()
            
            while True:
                hddFile = input("> ")
                if hddFile in [str(i+1) for i in range(len(files))]:
                    break
                else:
                    print(errMes)
            
            run(f"./hdds/{files[int(hddFile)-1]}")

        else:
            print(errMes)



def run(hddFile):  # main run code
    global hdd, pc, mar, mdr, ir, i, br, a, ram, cF, acc

    pc, mar, mdr, ir, i, a, cF, acc, br = -1, 0, 0, 0, "00000000", 0, 0, 0, False  # reset vars
    ram = [0 for i in range(8)]

    hdd = ["nop 0\n" for i in range(16)]  # reset hard drive to 16 bytes "nop"
    with open(hddFile, "r") as f:  # read hdd.txt to hard drive
        lines = f.readlines()
    for i in range(0, len(lines)):
        hdd[i] = lines[i]


    clear()
    while True:  # debug?
        debug = input("View in debug view (y/n)? ")
        if debug in ["y", "n"]:
            past = []
            break
        else:
            print(f"\n{red}That's not a valid answer{reset}")


    clear()
    while True:  # run
        if debug == "y":
            pR = ram
            
            pcF = str(pc)  # don't show "-1", show "-"
            if pcF == "-1":
                pcF = "-"

            iF = str(i)  # get i to right length
            while len(iF) < 8:
                iF = f"0{iF}"
            
            if pc == -1:  # if at beginning, reset
                iF, mar, mdr, ir = "-\t", "-", "-", "-"
            

            past.append([pcF, str(mar), str(mdr), str(ir), iF, str(cF), str(acc), str(a), f"[ {pR[0]} {pR[1]} {pR[2]} {pR[3]} {pR[4]} {pR[5]} {pR[6]} {pR[7]} ]"])
            for r in range(len(past)):
                for c in range(len(past[r])):
                    if "\n" in past[r][c]:
                        past[r][c] = past[r][c][:-1]
            
            clear()
            print(f"{blue}PC\tMAR\tMDR\tIR\tIR (BIN)\t\tCF\tACC\tA\tRAM{reset}")
            for p in range(len(past)):
                l = f"{past[p][0]}\t{past[p][1]}\t{past[p][2]}\t{past[p][3]}\t{past[p][4]}\t\t{past[p][5]}\t{past[p][6]}\t{past[p][7]}\t{past[p][8]}"
                if past[p] != past[-1]:
                    print(l)
                else:
                    print(f"{green}{l}{reset}")


            ch = input("\nPress 'ENTER' to step or type 'e' to end the program\n> ")  # continue?
            if ch == "e":
                break
            elif ch == "":
                pass
    
        step()
        
        if br:
            if debug == "y":  # show final command (hlt, etc)
                pR, pcF, iF = ram, str(pc), str(i)
                while len(iF) < 8:
                    iF = f"0{iF}"

                past.append([pcF, str(mar), str(mdr), str(ir), iF, str(cF), str(acc), str(a), f"[ {pR[0]} {pR[1]} {pR[2]} {pR[3]} {pR[4]} {pR[5]} {pR[6]} {pR[7]} ]"])
                for r in range(len(past)):
                    for c in range(len(past[r])):
                        if "\n" in past[r][c]:
                            past[r][c] = past[r][c][:-1]
                
                clear()
                print(f"{blue}PC\tMAR\tMDR\tIR\tIR (BIN)\t\tCF\tACC\tA\tRAM{reset}")
                for p in range(len(past)):
                    l = f"{past[p][0]}\t{past[p][1]}\t{past[p][2]}\t{past[p][3]}\t{past[p][4]}\t\t{past[p][5]}\t{past[p][6]}\t{past[p][7]}\t{past[p][8]}"
                    if past[p] != past[-1]:
                        print(l)
                    else:
                        print(f"{green}{l}{reset}")

            if not outed:
                if debug == "y":  # nice formatting
                    print()
                print(f"{red}This program didn't output anything{reset}")

            ch = input("\nPress 'ENTER' to end the program\n> ")
            break
    
    menu()



# main
menu()
