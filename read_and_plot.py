#!/bin/env python2.7

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 09:29:24 2016

@author: Hugo, Geng
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy
from scipy import special
from scipy.optimize import curve_fit
import numpy as np
import sys,os
import glob

def fitFunc(t, mu, sigma, y0, p0): #Def of the erf function for the fit
    return y0+(p0/2)*scipy.special.erf((np.sqrt(2)*(t-mu))/sigma)

choose = glob.glob("*Data_*")
print
themean=[]
thesigma=[]
Tmean=[]
Tsigma=[]
print 
print "---------------- List Of the Files --------------"
print choose
for path, subdirs, files in os.walk(r'./'):
    meanALL = [] #to plot VCal means for all channels on all chips
    VCALmean14 = [] #to plot VCal means for one channel (14) for all chips
    covALL = [] #to plot VCal covs for all channels on all chips
    VCALcov14 = [] #to plot VCal covs for one channel (14) for all chips
    thresholdALL = [] #to plot thresholds for all chips

    for fname in files:
        cities = fname.split("_")
        for city in cities:
            if city == 'Data':
                nameIt = fname.find("Data")
                slotIt = fname.find("GLIB")
                newFormat = False
                if slotIt < 0:
                    slotIt = fname.find("AMC")
                    newFormat = True
                    pass                 
                linkIt = fname.find("OH")
                vfatIt = fname.find("VFAT2")
                chipIt = fname.find("ID")
                print nameIt,slotIt,linkIt,vfatIt,chipIt
                nameS = fname[0:nameIt-1]
                slotS = fname[slotIt:linkIt-1]
                linkS = fname[linkIt:vfatIt-1]
                vfatS = fname[vfatIt:chipIt-1]
                chipS = fname[chipIt:]
                print nameS,slotS,linkS,vfatS,chipS
                print len(cities),cities
                #print fname
                TestName = nameS
                slot = -1
                if slotS[0] == "AMC":
                    slot     = int(slotS.split('_')[1])
                elif slotS[0] == "GLIB":
                    slot     = int(slotS.split('_')[4])-160
                else:
                    pass
                pos      = vfatS.split('_')[1]
                port     = chipS.split('_')[1]
# print choose
# TestName = raw_input("> Name of the Test? [Name Before '_Data_...'] : ")
# slot = raw_input("> GLIB slot used for the test? [1-12]: ")
# pos  = raw_input("> Position? [0-23]: ")
# port = raw_input("> ID of the VFAT2? : ")

# Number of the channel for which the SCURVE and its fit are printed.
                SCUVRE = 14
# build a rectangle in axes coords


                threshold1x = []
                threshold1y = []
                # scurvex = []
                # scurvey = []
                threshold2x = []
                threshold2y = []
                mean = []
                cov = []
                ma = np.zeros(shape=(128,255))
                #ma = np.zeros(shape=(127,255))
                count=0
                meanthreshold=0
                meanthreshold1=0
                sigmathreshold=0
                sigmathreshold1=0
                SCName = "S_CURVE_" + str(SCUVRE+1)

                # Read the file Data_GLIB_IP_192_168_0_161_VFAT2_X_ID_Y with the 2 threshold- 
                # Scans and the final Scurve by channel VFAT
                if newFormat:
                    print "%s_Data_%s_%s_%s_%s"%(nameS,slotS,linkS,vfatS,chipS)
                    pass
                print fname
                # print ""%(TestName)+"_Data_GLIB_IP_192_168_0_"+str(160+int(slot))+"_VFAT2_"+str(pos)+"_ID_"+str(port)
                filename = glob.glob("%s*"%(fname))
                if filename == []:
                    print "No VFAT2 with ID " +str(port)+" at the position " + str(pos) + " with name " +str(TestName)
                for k in range(0,len(filename)):
                    filename = glob.glob("%s*"%(fname))[k]
                    threshold1x = []
                    threshold1y = []
                    # scurvex = []
                    # scurvey = []
                    threshold2x = []
                    threshold2y = []
                    mean = []
                    cov = []
                    ma = np.zeros(shape=(128,255))
                    #ma = np.zeros(shape=(127,255))
                    count=0
                    f=open(filename)

                    line = (f.readline()).rstrip('\n')
                    thresholdValue = (float(line.strip('Threshold set to: ')))
                    thresholdALL.append(thresholdValue)
                    if line == "0": #If no threshold have been set, VFAT2 is all 0 or all 1
                        print "Broken VFAT"
                        while (line != ""):
                            if newFormat:
                                vals = line.split("\t")
                                threshold1x.append(float(vals[0]))
                                threshold1y.append(float(vals[1]))
                            else:
                                threshold1x.append(float(line))
                                threshold1y.append(float((f.readline()).rstrip('\n')))
                                pass
                            line = (f.readline()).rstrip('\n') 
                        plt.xlim(0,255)
                        plt.plot(threshold1x, threshold1y,'bo')
                        plt.show()
                    else :
                        line = (f.readline()).rstrip('\n')
                        while ("S_CURVE" not in line): #Read the first TH Scan
                            if "Latency" in line:
                                line = (f.readline()).rstrip('\n')
                                continue
                            if line == "":
                                break
                            if newFormat:
                                vals = line.split("\t")
                                threshold1x.append(float(vals[0]))
                                threshold1y.append(float(vals[1]))
                            else:
                                threshold1x.append(float(line))
                                threshold1y.append(float((f.readline()).rstrip('\n')))
                                pass
                            sys.stdout.flush()
                            line = (f.readline()).rstrip('\n')
                            pass
                        # def fitFunc(t, mu, sigma, y0, p0): #Def of the erf function for the fit
                        #     return y0+(p0/2)*scipy.special.erf((np.sqrt(2)*(t-mu))/sigma)
                        if line != "":
                            line = (f.readline()).rstrip('\n')
                            while True:  # Read all the SCurve   
                                scurvex = []
                                scurvey = []
                                while ("S_CURVE" not in line or "" not in line):
                                    if "second_threshold" in line or "Latency" in line:
                                        break
                                    if newFormat:
                                        vals = line.split("\t")
                                        scurvex.append(float(vals[0]))
                                        scurvey.append(float(vals[1]))
                                    else:
                                        scurvex.append(float(line))
                                        scurvey.append(float((f.readline()).rstrip('\n')))
                                        # line = (f.readline()).rstrip('\n')
                                        # scurvey.append(float(line))
                                        pass
                                    sys.stdout.flush()
                                    line = (f.readline()).rstrip('\n')  
                                # if "second_threshold" in line:
                                #     break
                                    pass
                                ma[count]=scurvey
                                count = count+1
                                while 0 in scurvey:
                                    scurvey.pop(0)
                                    scurvex.pop(0)
                                while 1 in scurvey:
                                    scurvey.pop(len(scurvey)-1)
                                    scurvex.pop(len(scurvex)-1)
                                    # plt.xlim(min(scurvex),max(scurvex))
                                scurvex2 = []
                                for i in scurvex:
                                    scurvex2.append(i-min(scurvex))
                                if SCName in line:
                                # print str(line)
                                # if line in line:
                                    # if "second_threshold" in line:
                                    #     line = "S_CURVE_" + str(128)
                                    scurvex3 = []
                                    fit=[]
                                    t = np.linspace(min(scurvex2), max(scurvex2), 250)
                                    fitParams, fitCovariances = curve_fit(fitFunc, scurvex2, scurvey)
                                    for i in t:
                                        fit.append(fitFunc(i, fitParams[0], fitParams[1],fitParams[2],fitParams[3]))
                                    # print "---------- Scurve and the erf fit of channel " + str(line) + "-1 in the transition zone ----------"    
                                    print "---------- Scurve and the erf fit of channel " + str(SCUVRE) + " in the transition zone ----------"    
                                    # print str(line) + "-1 ----- " + str(fitParams[0]+min(scurvex)) + " ----- " + str(fitParams[1]) + " ----- " + str(fitParams[2]) + " ----- " + str(fitParams[3])    
                                    plt.xlim(min(scurvex),max(scurvex))
                                    plt.ylabel('Efficiency')
                                    plt.xlabel('Calibration pulse ')
                                    plt.suptitle("%s_VFAT%s_ID_%s_ScurveAndErfFit"%(TestName,pos,port), fontsize=14, fontweight='bold')
                                    plt.plot(scurvex, scurvey,'bo',t+min(scurvex),fit,'r')
                                    plt.savefig("%s_VFAT%s_ID_%s_14_ScurveAndErfFit.png"%(TestName,pos,port))
                                    # plt.show()
                                    plt.clf()
                                    scurvex3 = []
                                    VCALmean14.append(fitParams[0]+min(scurvex))
                                    VCALcov14.append(fitParams[1])
                                    # print "VCal for channel 14: " + str(mean)
                                if scurvey==[]: # If the SCURVE of a channel was only 1 or 0
                                    print "line " + str(line) + " -1 is broken"
                                    mean.append(0) # If the channel is broken, the mean and covariance of the are set to 0
                                    meanALL.append(0)
                                    cov.append(0)
                                    covALL.append(0)
                                    scurvex  = []
                                    scurvey  = []
                                    scurvex2 = []
                                    line = (f.readline()).rstrip('\n')
                                    continue
                                try: # Fit the SCurve with the erf function
                                    fitParams, fitCovariances = curve_fit(fitFunc, scurvex2, scurvey)
                                    mean.append(fitParams[0]+min(scurvex))
                                    meanALL.append(fitParams[0]+min(scurvex))
                                    cov.append(fitParams[1])
                                    covALL.append(fitParams[1])
                                    themean.append(fitParams[0]+min(scurvex))
                                    thesigma.append(fitParams[1])
                                    meanthreshold1  = meanthreshold + fitParams[0]+min(scurvex)
                                    meanthreshold   = meanthreshold1
                                    sigmathreshold1 = sigmathreshold + fitParams[1]
                                    sigmathreshold  = sigmathreshold1
                                    # if "second_threshold" in line:
                                    #     line = "S_CURVE_" + str(128)
                                    # print str(line) + "-1 ----- " + str(fitParams[0]+min(scurvex)) + " ----- " + str(fitParams[1]) + " ----- " + str(fitParams[2]) + " ----- " + str(fitParams[3])    
                                except: # If the SCURVE of a channel can not be fit
                                    print "line" + str(line) + " -1 is broken"
                                    mean.append(0) # If the channel is broken, the mean and covariance of the are set to 0
                                    meanALL.append(0)
                                    cov.append(0)
                                    covALL.append(0)
                                if "S_CURVE_128" in line:
                                    # print str(TestName)+"_VFAT"+str(pos)+"_ID_"+str(port)+": mean of the threshold = "+str(meanthreshold/128.)+"; mean of the sigma = "+str(sigmathreshold/128.)
                                    # print str(meanthreshold/128.)
                                    # print str(sigmathreshold/128.)
                                    break
                                if "second_threshold" in line:
                                    Tmean.append(meanthreshold/128.)
                                    Tsigma.append(sigmathreshold/128.)
                                    # print str(TestName)+"_VFAT"+str(pos)+"_ID_"+str(port)+": mean of the threshold = "+str(meanthreshold/128.)+"; mean of the sigma = "+str(sigmathreshold/128.)
                                    # print str(meanthreshold/128.)
                                    # print str(sigmathreshold/128.)
                                    break
                                scurvex  = []
                                scurvey  = []
                                scurvex2 = []
                                line = (f.readline()).rstrip('\n')
                                pass  # closes while true
                            line = (f.readline()).rstrip('\n')   
                            while (line != ""):
                                if newFormat:
                                    vals = line.split("\t")
                                    threshold2x.append(float(vals[0]))
                                    threshold2y.append(float(vals[1]))
                                else:
                                    threshold2x.append(float(line))
                                    threshold2y.append(float((f.readline()).rstrip('\n')))
                                    pass
                                line = (f.readline()).rstrip('\n')
                                pass # close while loop
                            f.close()
                            pass # close if line != ""
                        # Plot the 2 TH Scans
                        print("---------- Threshold Scans ----------")    
                        plt.xlim(0,255)
                        plt.ylim(0,100)
                        plt.ylabel('Noise')
                        plt.xlabel('Threshold')
                        plt.suptitle("%s_VFAT%s_ID_%s_thresholds"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.plot(threshold1x, threshold1y,'bo',threshold2x, threshold2y,'ro')
                        plt.savefig("%s_VFAT%s_ID_%s_thresholds.png"%(TestName,pos,port))
                        # plt.show() 
                        plt.clf()
                        if threshold2x == []:
                            print "Only the TH worked for", str(filename)
                            continue

                        print("---------- Mean of the Erf Function by channel ----------")
                        plt.ylim(0,255)
                        plt.ylabel('Calibration pulse [per Channel]')
                        plt.xlabel('128 Strip Channels')
                        plt.suptitle("%s_VFAT%s_ID_%s_meanerfbychan"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.plot(mean,'bo')
                        plt.savefig("%s_VFAT%s_ID_%s_meanerfbychan.png"%(TestName,pos,port))
                        # plt.show()
                        plt.clf()
                        
                        print("---------- cov of the Erf Function by channel ----------")
                        plt.ylabel('S-curve Sigma of the Erf Function by Channel [per Channel]')
                        plt.xlabel('128 Strip Channels')
                        plt.suptitle("%s_VFAT%s_ID_%s_coverfbychan"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.plot(cov,'ro')
                        plt.savefig("%s_VFAT%s_ID_%s_coverfbychan.png"%(TestName,pos,port))
                        # plt.show()
                        plt.clf()
                        
                        print("---------- Histogram of the covariance of the Erf Function ----------")
                        plt.ylabel('Covariance of the Erf Function')
                        plt.xlabel('S-curve Sigma')
                        plt.hist(cov, 50, normed=1, facecolor='y', alpha = 0.8)
                        plt.suptitle("%s_VFAT%s_ID_%s_covhisterf"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.savefig("%s_VFAT%s_ID_%s_covhisterf.png"%(TestName,pos,port))
                        # plt.show()
                        plt.clf()
                        
                        # Read and plot the SCurve before the scan                       
                        fileN = "%s_SCurve_by_channel_%s_%s"%(nameS,vfatS,chipS)
                        if newFormat:
                            fileN = "%s_SCurve_by_channel_%s_%s_%s_%s"%(nameS,slotS,linkS,vfatS,chipS)
                            pass
                        print fileN
                        fi = glob.glob("%s"%(fileN))[k]
                        g=open(fi)
                                                        
                        maSC = np.zeros(shape=(128,255))
                        count = 0
                        line = (g.readline()).rstrip('\n')
                        line = (g.readline()).rstrip('\n')
                        SCx = []
                        SCy = []
                        while True:     
                            while ("SCurve" not in line):
                                if not line: break
                                if newFormat:
                                    vals = line.split("\t")
                                    SCx.append(float(vals[0]))
                                    SCy.append(float(vals[1]))
                                else:
                                    SCx.append(float(line))
                                    SCy.append(float((g.readline()).rstrip('\n')))
                                    pass
                                line = (g.readline()).rstrip('\n')
                                pass # closes while ("SCurve" not in line):
                            if not line:
                                break
                            print "SCy",SCy
                            print "SCx",SCx
                            maSC[count]=SCy
                            count = count+1 
                            SCx = []
                            SCy = []
                            line = (g.readline()).rstrip('\n')
                            pass # closes while True
                        print("---------- S-Curve by channel Before the Script ----------")    
                        plt.ylabel('128 Strip Channels')
                        plt.xlabel('Calibration Pulse')
                        plt.suptitle("%s_VFAT%s_ID_%s_scurvebefore"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.imshow(maSC)
                        plt.savefig("%s_VFAT%s_ID_%s_scurvebefore.png"%(TestName,pos,port))
                        # plt.show()
                        plt.clf()
                        g.close()
                        
   # Plot the S_Curve after fitting
                        print("---------- S-Curve by channel after the Script ----------")
                        plt.ylabel('128 Strip Channels')
                        plt.xlabel('Calibration Pulse')
                        plt.suptitle("%s_VFAT%s_ID_%s_scurveafter"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        plt.imshow(ma)
                        plt.savefig("%s_VFAT%s_ID_%s_scurveafter.png"%(TestName,pos,port))
                        #plt.show()
                        plt.clf()     
                        
                    
                        vcal0 = []
                        vcal31 = []
                        vcalfinal = []
                        fileN = "%s_VCal_%s_%s"%(nameS,vfatS,chipS)
                        if newFormat:
                            fileN = "%s_VCal_%s_%s_%s_%s"%(nameS,slotS,linkS,vfatS,chipS)
                            pass
                        filename = glob.glob("%s"%(fileN))[k]
                        #filename = glob.glob(str(TestName)+"_VCal_VFAT2_"+str(pos)+"_ID_" + str(port))[k]
                        f=open(filename,'r')
                        line = (f.readline()).rstrip('\n')
                        vcal= line.split()
                        for ele in vcal:
                            if ele.startswith('['):
                                ele = ele[1:]
                            ele = ele.rstrip(']') 
                            ele = ele.rstrip('L,') 
                            vcal0.append(int(ele))
                        print("---------- Histogram of the '0.5 point' for a TrimDAC of 0/31 and after the Script ----------")   
                        plt.hist(vcal0, bins=range(min(vcal0), max(vcal0) + 1, 1), normed=1, facecolor='g', alpha = 0.8)
                        
                        line = (f.readline()).rstrip('\n')
                        vcal= line.split()
                        for ele in vcal:
                            if ele.startswith('['):
                                ele = ele[1:]
                            ele = ele.rstrip(']') 
                            ele = ele.rstrip('L,') 
                            vcal31.append(int(ele))
                        
                        plt.hist(vcal31,  bins=range(min(vcal31), max(vcal31) + 1, 1), normed=1, facecolor='r', alpha = 0.8)
                        
                        line = (f.readline())
                        vcal= line.split()
                        for ele in vcal:
                            if ele.startswith('['):
                                ele = ele[1:]
                            ele = ele.rstrip(']') 
                            ele = ele.rstrip('L,') 
                            vcalfinal.append(int(ele))
                        
                        plt.hist(mean,  bins=range(int(min(mean)), int(max(mean)) + 1, 1) , normed=1, facecolor='b', alpha = 0.8)
                        plt.suptitle("%s_VFAT%s_ID_%s_hist05pointafter"%(TestName,pos,port), fontsize=14, fontweight='bold')
                        
                        plt.savefig("%s_VFAT%s_ID_%s_hist05pointafter.png"%(TestName,pos,port))
                        #plt.show()
                        plt.clf()
                        f.close()
