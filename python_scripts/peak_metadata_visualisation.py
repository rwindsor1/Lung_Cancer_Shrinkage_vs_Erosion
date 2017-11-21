import matplotlib.pyplot as plt
import os
import numpy as np

input_folder_address = "C:/Users/Rhydian/Documents/Work/MPhysProject/peakchanges_metadata"
def nll3(parms,hd,vals):
        
        test = make_triple_gaussian(hd,parms)
        
        # Poisson negative loglikelihood:
        # NOTE: if there are any zero-valued data points in
        # your prediction (test) this will return a NaN.
        ll = -np.sum(test) + np.sum(vals*np.log(test)) - np.sum(sp.special.gammaln(vals + 1))
        nll = -1.*ll
        
        # L2 norm:
        #nll = np.sum((test - vals)**2)
        
        return nll

def make_triple_gaussian(hd,parms):
        
        a1,mu1,sig1,a2,mu2,sig2,a3,mu3,sig3 = parms
        vals =[]
        for element in hd:
            vals.append(a1*np.exp(-1.*(element-mu1)**2/(2.*sig1**2)) + a2*np.exp(-1.*(element-mu2)**2/(2.*sig2**2)) + a3*np.exp(-1.*(element-mu3)**2/(2.*sig3**2)))
        
        return vals        

        
for name in os.listdir(input_folder_address):
    file_of_interest = open(os.path.join(input_folder_address,name),"r")
    scan_no = 2
    for line in file_of_interest:
        line = line.split(",")[:-1]
        line = list(map(float,line))
        hu = list(np.linspace(1,1200,1200))
        print(name[:-4] + " " + str(scan_no))
        fitted = make_triple_gaussian(hu,line)
        plt.plot(hu,fitted)
        plt.title(name[:-4] + " scan " + str(scan_no))
        plt.savefig(name[:-4] + " scan " + str(scan_no))
        scan_no += 1 
        plt.clf()
    