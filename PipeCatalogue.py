# -*- coding: utf-8 -*-
"""
Pipe Catalogue Data - Single Steel Pipe by LOGSTOR

Created on Mon Nov  2 20:14:25 2020

@author: Hakan İbrahim Tol, PhD

References:
[1] LOGSTOR, Product Catalogue Version 2018.12. 
https://www.logstor.com/media/6115/product-catalogue-uk-201812.pdf 
"""

def LayerDiameters(DN,IS):
    
    # DN: Nominal pipe diameter
    # IS: Insulation series 
    
    DN_l=[20,25,32,40,50,65,80,100,125]
    
    if DN not in DN_l:
        raise TypeError("Nominal Pipe Diameter can be:", DN_l)
    
    d1_l=[21.7,28.5,37.2,43.1,54.5,70.3,82.5,107.1,132.5]
    d2_l=[26.9,33.7,42.4,48.3,60.3,76.1,88.9,114.3,139.7]
    
    if IS==1:
        d3_l=[84,84,104,104,119,134,154,193.6,218.2]
        d4_l=[90,90,110,110,125,140,160,200,225]
    elif IS==2:
        d3_l=[104,104,119,119,134,154,174,218.2,242.8]
        d4_l=[110,110,125,125,140,160,180,225,250]
    elif IS==3:
        d3_l=[119,119,134,134,154,174,193.6,242.8,272.2]
        d4_l=[125,125,140,140,160,180,200,250,280]
    else:
        raise TypeError("Insulation Series (IS) can be one of (poor) 1, 2, or 3 (good)")
        
    ind=DN_l.index(DN)
    
    return d1_l[ind]*0.001,d2_l[ind]*0.001,d3_l[ind]*0.001,d4_l[ind]*0.001
    
