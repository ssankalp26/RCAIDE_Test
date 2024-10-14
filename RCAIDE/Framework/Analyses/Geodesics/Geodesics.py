from  RCAIDE.Library.Methods.Geodesics.Geodesics import Geodesic_Calculate

def  Calculate_Distance(coord1, coord2):
    distance = Geodesic_Calculate(coord1, coord2).kilometers
    return(distance)

if __name__ == '__main__': 
    Calculate_Distance()

