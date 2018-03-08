# Takes combined Niftis and creates histograms based on them

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
import scipy as sp
import pylab as pl
import scipy.optimize as op
#%matplotlib inline

def make_double_gaussian(hd,parms):
    
    a1,mu1,sig1,a2,mu2,sig2 = parms
    
    vals = a1*np.exp(-1.*(hd-mu1)**2/(2.*sig1**2)) + a2*np.exp(-1.*(hd-mu2)**2/(2.*sig2**2))
    
    return vals

def make_triple_gaussian(hd,parms):
        
    a1,mu1,sig1,a2,mu2,sig2,a3,mu3,sig3 = parms
    vals = []
    for element in hd:
        vals.append(a1*np.exp(-1.*(element-mu1)**2/(2.*sig1**2)) + a2*np.exp(-1.*(element-mu2)**2/(2.*sig2**2))
                    + a3*np.exp(-1.*(element-mu3)**2/(2.*sig3**2)))
    
    return vals
	
def nll(parms,hd,vals):
	
	test = make_double_gaussian(hd,parms)
	
	# Poisson negative loglikelihood:
	# NOTE: if there are any zero-valued data points in
	# your prediction (test) this will return a NaN.
	ll = -np.sum(test) + np.sum(vals*np.log(test)) - np.sum(sp.special.gammaln(vals + 1))
	nll = -1.*ll
	
	# L2 norm:
	#nll = np.sum((test - vals)**2)
	
	return nll

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
	
inputFile = "D:/combinedNiftis"
outputFile = "D:/fullTumourHistograms2"
patientNames = os.listdir(inputFile)

bounds = [(50.,100.),(400.,600.),(50.,200.),(300,500),(700,900),(30,200)]
bounds_3 = [(10.,3000.),(380.,450.),(10.,1000.),(10.,3000.),(500.,800.),(10.,400.),(10.,9000.),(800.,1200.),(10.,400.)]
p0 = [1.,400.,50.,1.,900.,50.]
p0_3 = [1.,400.,50.,1.,600.,50.,1.,900.,50.]


for patientName in patientNames:
	scanNames = os.listdir(os.path.join(inputFile,patientName))
	outputfile = open(os.path.join(outputFile,patientName)+".csv","a")
	for scanName in scanNames:
		scanPath = os.path.join(inputFile,patientName,scanName)
		scan = nib.load(scanPath)
		scanData = scan.get_data()
		pixelVals = scanData[np.where(scanData>0)]
		values, bins, _ = plt.hist(pixelVals, bins = 200)
		bins_median = []
		for i in range(1,len(bins)):
			bins_median.append(0.5*(bins[i-1]+bins[i]))
		bins = bins_median
		popt = op.minimize(nll3, p0_3, bounds = bounds_3, args=(bins,values)) #MAKES 3 PEAK GUASSIAN MODEL
		astring = ""
		peak1_data,peak2_data,peak3_data = popt.x[0:3],popt.x[6:9],popt.x[3:6]
		peak_data = list(peak1_data) + list(peak2_data) + list(peak3_data)
		for element in peak_data:
			astring+= str(element)+","
		outputfile.write(astring)
		outputfile.write("\n")
		array_name = patientName[0:3] + "_scan" + str(scanNames.index(scanName) + 2)
		fitted = make_triple_gaussian(bins,popt.x)
		plt.plot(bins,fitted,c='r')
		plt.title(array_name)
		plt.savefig(os.path.join(outputFile,patientName) + array_name + ".png")
		#plt.show()
		plt.cla()
		print(str(scanName) + " Complete.")
	outputfile.close()


