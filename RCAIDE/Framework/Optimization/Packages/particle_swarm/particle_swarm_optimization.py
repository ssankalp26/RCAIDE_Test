## @ingroup Optimization-Package_Setups
# particle_swarm_optimization.py
# 
# Created:  Sep. 2019, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# RCAIDE imports
import numpy as np
import scipy as sp
 
## @ingroup Optimization-Package_Setups
def particle_swarm_optimization(problem,npart,bounds,iterations=100,
                              min_split=0.1,max_split=0.5,accel=0.5,
                              init_guess=None,init_vals=None):
    """Particle swarm optimization algorithm

    Assumptions:
    None

    Source:
    None

    Inputs:
    problem     - function that evaluates the objective
    npart       - number of particles
    bounds      - bounds on the design space
    iterations  - maximum number of iterations
    min_split   - minimum split ratio for design space
    max_split   - maximum split ratio for design space
    accel       - particle acceleration
    init_guess  - initial guess for optimization
    init_vals   - initial values for particles

    Returns:
    xopt - optimal design vector
    fopt - optimal objective value

    Properties Used:
    None
    """
    
    # License 
    ''' 
    Copyright (c) 2015, Sebastian M. Castillo Hair
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
    3. All advertising materials mentioning features or use of this software
        must display the following acknowledgement:
        This product includes software developed by Sebastian M. Castillo Hair.
    4. Neither the name of Sebastian M. Castillo Hair nor the
        names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY SEBASTIAN M. CASTILLO HAIR ''AS IS'' AND ANY
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL SEBASTIAN M. CASTILLO HAIR BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''
    
    assert len(bounds)==2, 'Bounds must be a list of two elements'
    assert hasattr(problem, '__call__'), 'Invalid function handle'
    lb = np.array(bounds[0])
    ub = np.array(bounds[1])
    assert np.all(ub>lb), 'All upper-bound values must be greater than lower-bound values'
   
    vhigh = np.abs(ub - lb)
    vlow = -vhigh
    
    # Initialize the particle swarm ############################################
    S = npart
    D = len(lb)  # the number of dimensions each particle has
    x = np.random.rand(S, D)  # particle positions
    v = np.zeros_like(x)  # particle velocities
    p = np.zeros_like(x)  # best particle positions
    fp = np.zeros(S)  # best particle function values
    g = []  # best swarm position
    fg = 1e100  # artificial best swarm position starting value
    
    for i in range(S):
        # Initialize the particle's position
        x[i, :] = lb + x[i, :]*(ub - lb)
   
        # Initialize the particle's best known position
        p[i, :] = x[i, :]
       
        # Calculate the objective's value at the current particle's
        fp[i] = problem(p[i, :])
       
        # At the start, there may not be any feasible starting point, so just
        # give it a temporary "best" point since it's likely to change
        if i==0:
            g = p[0, :].copy()

        # If the current particle's position is better than the swarm's,
        # update the best swarm position
        if fp[i]<fg:
            fg = fp[i]
            g = p[i, :].copy()
       
        # Initialize the particle's velocity
        v[i, :] = vlow + np.random.rand(D)*(vhigh - vlow)
       
    # Iterate until termination criterion met ##################################
    it = 1
    while it<=iterations:
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))
        for i in range(S):

            # Update the particle's velocity
            v[i, :] = accel*v[i, :] + max_split*rp[i, :]*(p[i, :] - x[i, :]) + \
                      min_split*rg[i, :]*(g - x[i, :])
                      
            # Update the particle's position, correcting lower and upper bound 
            # violations, then update the objective function value
            x[i, :] = x[i, :] + v[i, :]
            mark1 = x[i, :]<lb
            mark2 = x[i, :]>ub
            x[i, mark1] = lb[mark1]
            x[i, mark2] = ub[mark2]
            fx = problem(x[i, :])
            
            # Compare particle's best position (if constraints are satisfied)
            if fx<fp[i]:
                p[i, :] = x[i, :].copy()
                fp[i] = fx

                # Compare swarm's best position to current particle's position
                # (Can only get here if constraints are satisfied)
                if fx<fg:
                    if debug:
                        print('New best for swarm at iteration {:}: {:} {:}'.format(it, x[i, :], fx))

                    tmp = x[i, :].copy()
                    stepsize = np.sqrt(np.sum((g-tmp)**2))
                    if np.abs(fg - fx)<=minfunc:
                        print('Stopping search: Swarm best objective change less than {:}'.format(minfunc))
                        return tmp, fx
                    elif stepsize<=minstep:
                        print('Stopping search: Swarm best position change less than {:}'.format(minstep))
                        return tmp, fx
                    else:
                        g = tmp.copy()
                        fg = fx

        if debug:
            print('Best after iteration {:}: {:} {:}'.format(it, g, fg))
        it += 1

    print('Stopping search: maximum iterations reached --> {:}'.format(iterations))
    
    if not is_feasible(g):
        print("However, the optimization couldn't find a feasible design. Sorry")
    return g, fg

