import pyhepmc
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd

pid_translator = {
        211:"pi+",
        -211:"pi-",
        22:"gamma",
        2112:"neutron",
        -2112:"antineutron",
        2212:"proton",
        -2212:"antiproton",
        }

pid_marker = {
        211:"+",
        -211: "_",
        22:".",
        2112:"o",
        -2112:"o",
        2212:"*",
        -2212:"*",
        }


if __name__ == "__main__":
    
    # user options
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inFileName", help="Input file name", default="test.hepmc")
    parser.add_argument("-o", "--outFileName", help="Output file name", default="out.txt")
    ops = parser.parse_args()

    # list for tracks
    #tracks = [] # cotb cota p flp localx localy pT
    fname = ops.inFileName
    outFile = (fname.split('/')[-1]).split('.')[0]
    
    # pyhepmc.open can read most HepMC formats using auto-detection
    with pyhepmc.open(fname) as f:
        # loop over events
        particle_id = []
        event_number = []
        status = []
        mass = []
        pt = []
        eta = []
        phi = []
        energy = []

        for iF, event in enumerate(f):
            # loop over particles


            if iF >99:
                break # I just want to plot a few events
            
            print(f"Event {iF} has {len(event.particles)} particles")
            for particle in event.particles:
                

                # # to get the production vertex and position
                prod_vertex = particle.production_vertex
                prod_vector = prod_vertex.position
                prod_R = prod_vector.perp() # [mm]

                # # to get the decay vertex
                # decay_vertex = particle.end_vertex
                # decay_vector = decay_vertex.position
                
                # decide which particles to keep
                
                accept = (abs(particle.momentum.eta()) != float("inf")) # non infinite eta
                
                # for now I won't cut in final state partiles or particles in the detectors, I want to see intermediate particles too
                #accept *= (particle.status == 1) # final state particle
                #accept *= (particle.momentum.pt()>1)
                #accept *= ( (prod_R >= 30) * (prod_R <= 130) ) # within pixel detector ~ 30-130mm

                if not accept:
                    continue

                #print(particle.id, particle.pid, particle.status, particle.momentum.pt(), particle.momentum.eta(), particle.momentum.phi(), prod_vector.x, prod_vector.y)

                # track properties
                #eta = particle.momentum.eta()
                #phi = particle.momentum.phi()
                #p = particle.momentum.p3mod()
                #localx = prod_vector.x # this needs to be particle position at start of pixel detector or only save particles that are produced within epsilon distance of detector
                #localy = prod_vector.y # [mm]
                #pT = particle.momentum.pt()
                



                particle_id.append(particle.pid)
                event_number.append(iF)
                status.append(particle.status)
                eta.append(particle.momentum.eta())
                phi.append(particle.momentum.phi())
                pt.append(particle.momentum.pt())
                mass.append(particle.momentum.m())
                energy.append(particle.momentum.e)




        dict ={"id":particle_id,"event":event_number,"status":status,"mass":mass,"energy":energy,"pt":pt,"eta":eta,"phi":phi}

        particles = pd.DataFrame(dict)

        # select status 1
        particles = particles[particles['status']==1]

        plt.style.use('ggplot')
        fig, ax = plt.subplots()
           

        #ax.scatter(etas,phis,label=f"Event {iF}: {len(event.particles)} particles", marker='.')
        #ax.hist(particles['mass'],range=(0,20),log=True,bins=50)
        ax.hist(particles['eta'],log=True,bins=20)
        ax.set_xlabel("eta")
        ax.set_ylabel("counts")
        ax.set_title(f"eta histogram status 1")
            

        ax.legend()
            
          
        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/kinematics/eta/status1/"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)
        

        print(f"Saving figure: {outFolder}/{outFile}.png")
        plt.savefig(f"{outFolder}/{outFile}.png")


        plt.cla()

