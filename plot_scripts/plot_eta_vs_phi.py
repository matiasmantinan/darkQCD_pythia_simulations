import pyhepmc
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os

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
    outFolder = (fname.split('/')[-1]).split('.')[0]
    print(outFolder)
    # pyhepmc.open can read most HepMC formats using auto-detection
    with pyhepmc.open(fname) as f:
        # loop over events

        for iF, event in enumerate(f):
            # loop over particles
            particles_id = []
            particles_status = []
            etas = []
            phis = []

            event_dict = {}


            if iF >9:
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
                accept *= (particle.status == 1) # final state particle
                accept *= (particle.momentum.pt()>1)
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
                


                if not (particle.pid in  event_dict):
                    event_dict[particle.pid] = []

                event_dict[particle.pid].append([particle.momentum.eta(),particle.momentum.phi(),particle.momentum.p3mod()])
                
                particles_id.append(particle.pid)
                particles_status.append(particle.status)
                etas.append(particle.momentum.eta())
                phis.append(particle.momentum.phi())




            plt.style.use('ggplot')
            fig, ax = plt.subplots()
           
            for pid in event_dict:
                if pid in pid_translator:
                    print(f"Ploting particle {pid} -> {pid_translator[pid]} ")
                    scatter = ax.scatter(np.array(event_dict[pid])[:,0],np.array(event_dict[pid])[:,1],c=np.array(event_dict[pid])[:,2],cmap="magma",label=f"{pid_translator[pid]}",marker=f"{pid_marker[pid]}")
                else:
                    print(f"Ploting particle {pid} -> other ")
                    scatter = ax.scatter(np.array(event_dict[pid])[:,0],np.array(event_dict[pid])[:,1],c=np.array(event_dict[pid])[:,2],cmap="magma",label="other",marker="s")


                
            #ax.scatter(etas,phis,label=f"Event {iF}: {len(event.particles)} particles", marker='.')
            ax.set_xlabel("eta")
            ax.set_ylabel("phi")
            ax.set_title(f"Event {iF}: {len(event.particles)} particles (cut status=1)")
            
            cbar = plt.colorbar(scatter,ax=ax, label='Momentum')

            ax.legend()

            if not os.path.exists(f"../figures/eta_phi/{outFolder}/"):
                print(f"Creating directory ../figures/eta_phi/{outFolder}/")
                os.makedirs(f"../figures/eta_phi/{outFolder}/")


            print(f"Saving figure: ../figures/eta_phi/{outFolder}/eta_vs_phi_event_{iF}_status=1.png")
            plt.savefig(f"../figures/eta_phi/{outFolder}/eta_vs_phi_event_{iF}_status=1_anyR.png")
            plt.cla()

            #break # need to understand what to put in track_list between events

        # save to file
        #np.savetxt(ops.outFileName, tracks, delimiter=' ', fmt="%f")
