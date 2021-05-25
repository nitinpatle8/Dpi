import deletecsv as dl
import sys 

def __main__():    
    try:
        dl.delete_csv(str(sys.argv[1]))
        print("successfully deleted")
    except:
        print("some error occured")
        exit(0)


__main__()