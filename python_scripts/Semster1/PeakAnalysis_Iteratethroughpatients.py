
# coding: utf-8

# In[87]:


import os
import numpy as np
import matplotlib.pyplot as plt
dict = {"NSCLC1_":[1200,900,100],
        "NSCLC2_":[1200,300,80],
        "NSCLC5_":[1200,1400,100],
        "NSCLC6_":[1200,400,100],
        "NSCLC7_":[1200,2200,100],
        "NSCLC10":[1200,500,100],
        "NSCLC11":[1200,1600,200],
        "NSCLC16":[1200,500, 100]}
input_file= "C:/Users/Rhydian/Documents/Work/MPhysProject/nparrays/inside"

array_names = os.listdir(input_file)
    

# In[88]:

for nparr in array_names:
    outputfile = open("C:/Users/Rhydian/Documents/Work/MPhysProject/peakchanges_metadata/"+nparr[0:7]+".csv","a")
    array_name = nparr
    print(array_name)
    info_array = dict[array_name[0:7]]
    arr = np.load(os.path.join(input_file,array_name))
    values, bins, _ = plt.hist(arr[~np.isnan(arr)], bins = info_array[2])

    # In[89]:

    from sklearn.neighbors.kde import KernelDensity
    specialboy = zip(bins,values)
    my_matrix = []
    for i in list(specialboy):
        my_matrix.append(list(i))

    """kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(my_matrix)
    samples = kde.sample(1000)
    samples = np.array(samples)
    plt.scatter(samples[:,0],samples[:,1])
    plt.show()"""


    # In[90]:


    print(len(values))
    print(len(bins))
    bins_median = []
    for i in range(1,len(bins)):
        bins_median.append(0.5*(bins[i-1]+bins[i]))

    bins = bins_median
        
    print(len(bins))


    # In[91]:


    import numpy as np
    import pylab as pl
    import scipy as sp

    def make_double_gaussian(hd,parms):
        
        a1,mu1,sig1,a2,mu2,sig2 = parms
        
        vals = a1*np.exp(-1.*(hd-mu1)**2/(2.*sig1**2)) + a2*np.exp(-1.*(hd-mu2)**2/(2.*sig2**2))
        
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

    def make_triple_gaussian(hd,parms):
        
        a1,mu1,sig1,a2,mu2,sig2,a3,mu3,sig3 = parms
        
        vals = a1*np.exp(-1.*(hd-mu1)**2/(2.*sig1**2)) + a2*np.exp(-1.*(hd-mu2)**2/(2.*sig2**2)) + a3*np.exp(-1.*(hd-mu3)**2/(2.*sig3**2))
        
        return vals



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

    import scipy.optimize as op
    bounds = [(50.,100.),(400.,600.),(50.,200.),(300,500),(700,900),(30,200)]
    bounds_3 = [(10.,2000.),(380.,450.),(10.,1000.),(10.,3000.),(500.,800.),(10.,400.),(10.,2000.),(800.,1200.),(10.,400.)]
    p0 = [1.,400.,50.,1.,900.,50.]
    p0_3 = [1.,400.,50.,1.,600.,50.,1.,900.,50.]

    #popt = op.minimize(nll, p0, bounds = bounds, args=(bins,values)) #MAKES 2 PEAK GUASSIAN MODEL
    popt = op.minimize(nll3, p0_3, bounds = bounds_3, args=(bins,values)) #MAKES 3 PEAK GUASSIAN MODEL
    print(popt.x)
    astring = ""
    peak1_data,peak2_data,peak3_data = popt.x[0:3],popt.x[6:9],popt.x[3:6]
    peak_data = list(peak1_data) + list(peak2_data) + list(peak3_data)
    for element in peak_data:
        astring+= str(element)+","
    outputfile.write(astring)
    outputfile.write("\n")
    outputfile.close()
    # In[92]:

    #make plots with scattered points on them
    fitted = make_triple_gaussian(bins,popt.x)
    plt.plot(bins,fitted,c='r')
    plt.title(array_name)
    plt.savefig("C:/Users/Rhydian/Documents/Work/MPhysProject/scatter_and_fit_histograms/"+array_name+".png")
    #plt.show()
    plt.cla()
    # In[98]:

    

