# RCAIDE/Compoments/Nacelles/Stack_Nacelle.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data, Container  
from .Nacelle import Nacelle
  
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ---------------------------------------------------------------------------------------------------------------------- 
class Stack_Nacelle(Nacelle):
    """
    A class for modeling nacelles composed of multiple segments.
    Inherits from the Nacelle class.

    Attributes
    ----------
    tag : str
        Identifier for the component, defaults to 'stack_nacelle'

    Segments : Data
        Collection of Segment objects that make up the nacelle

    Methods
    -------
    append_segment(segment)
        Adds a new segment to the nacelle

    Notes
    -----
    The Stack_Nacelle class enables the construction of complex nacelle geometries
    through the combination of multiple segments. Each segment can have unique
    dimensions and properties, allowing for detailed geometric definition of the
    nacelle shape. This approach provides flexibility in modeling various nacelle
    configurations.
    
    **Definitions**
    'Segment'
        Individual section of the nacelle with unique geometric properties
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """      
        
        self.tag                       = 'stack_nacelle'  
        self.Segments                  = Container() 
        
    def append_segment(self,segment):
        """ Adds a segment to the nacelle. 
    
        Assumptions:
        None
        Source:
        N/A
        Inputs:
        None
        Outputs:
        None
        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return  
