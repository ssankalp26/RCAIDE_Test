# RCAIDE/Compoments/Airfoils/Airfoil.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components   import Component 
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Airfoils 
class Airfoil(Component):
    """
    A base class for defining and managing airfoil characteristics and geometry.

    Attributes
    ----------
    tag : str
        Identifier for the airfoil, defaults to 'Airfoil'
    
    coordinate_file : str
        Path to the file containing airfoil coordinates
    
    geometry : Data
        Geometric properties of the airfoil
    
    polar_files : list
        List of files containing airfoil polar data
    
    polars : Data
        Collection of airfoil polar data
    
    prev : Airfoil
        Reference to previous airfoil in a sequence
    
    next : Airfoil
        Reference to next airfoil in a sequence
    
    number_of_points : int
        Number of points used to define airfoil geometry, defaults to 201

    Methods
    -------
    __defaults__()
        Sets the default values for the airfoil attributes

    Notes
    -----
    The Airfoil class serves as a base class for all airfoil types in RCAIDE.
    It provides the fundamental structure for storing and managing airfoil
    properties, coordinates, and aerodynamic characteristics.
    
    **Definitions**
    'Polar Data'
        Aerodynamic coefficients (lift, drag, moment) at various angles of attack
    'Coordinate File'
        File containing x,y coordinates that define the airfoil shape. Typically a text file with two columns of numbers
        adhering tot eh Selig format: https://m-selig.ae.illinois.edu/ads/coord_database.html#seligFmt. 

    
    References
    ----------
    .. [1] None currently listed
    """
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """         
        
        self.tag                        = 'Airfoil' 
        self.coordinate_file            = None     
        self.geometry                   = None
        self.polar_files                = None
        self.polars                     = None
        self.prev                       = None
        self.next                       = None
        self.number_of_points           = 201
       