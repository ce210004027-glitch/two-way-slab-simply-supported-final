ALPHA_POINTS=[(1.0,0.062,0.062),(1.1,0.074,0.061),(1.2,0.084,0.059),(1.3,0.093,0.055),(1.4,0.099,0.051),(1.5,0.104,0.046),(1.75,0.113,0.037),(2.0,0.118,0.029),(2.5,0.122,0.020),(3.0,0.124,0.014)]
PT_GRID={"Mbds":[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.5],"pt_415":[0.084,0.113,0.142,0.171,0.201,0.231,0.261,0.291,0.321,0.346,0.449]}
FIG4_K=[(120.0,1.60),(145.0,1.45),(190.0,1.30),(240.0,1.15),(300.0,1.05)]
XU_OVER_D={250:0.53,415:0.48,500:0.46}
import math
def linear_interp(x,x0,y0,x1,y1):
    return y0 if x1==x0 else y0+(y1-y0)*(x-x0)/(x1-x0)
def interp_alpha(r):
    pts=ALPHA_POINTS
    if r<=pts[0][0]: return pts[0][1],pts[0][2]
    if r>=pts[-1][0]: return pts[-1][1],pts[-1][2]
    for i in range(len(pts)-1):
        x0,ax0,ay0=pts[i]; x1,ax1,ay1=pts[i+1]
        if x0<=r<=x1: return linear_interp(r,x0,ax0,x1,ax1), linear_interp(r,x0,ay0,x1,ay1)
    return pts[-1][1],pts[-1][2]
def interp_pt(Mbd2,fy=415):
    xs=PT_GRID["Mbds"]; ys=PT_GRID["pt_415"]
    if Mbd2<=xs[0]: return ys[0]
    if Mbd2>=xs[-1]: return ys[-1]
    for i in range(len(xs)-1):
        if xs[i]<=Mbd2<=xs[i+1]: return linear_interp(Mbd2,xs[i],ys[i],xs[i+1],ys[i+1])
    return ys[-1]
def interp_K(fs):
    pts=FIG4_K
    if fs<=pts[0][0]: return pts[0][1]
    if fs>=pts[-1][0]: return pts[-1][1]
    for i in range(len(pts)-1):
        x0,y0=pts[i]; x1,y1=pts[i+1]
        if x0<=fs<=x1: return linear_interp(fs,x0,y0,x1,y1)
    return pts[-1][1]
def area_of_bar(d): return math.pi*(d/2.0)**2
def choose_practical_spacing(S_calc_mm,tol_percent=15.0):
    if S_calc_mm<=0: return None,"invalid"
    tol=tol_percent/100.0
    for m in range(25,int(math.floor(S_calc_mm))+1,25):
        if (S_calc_mm-m)/S_calc_mm<=tol: return m,"25"
    for m in range(5,int(math.floor(S_calc_mm))+1,5):
        if (S_calc_mm-m)/S_calc_mm<=tol: return m,"5"
    if S_calc_mm>=5: return int(math.floor(S_calc_mm/5.0))*5,"fallback"
    return None,"none"
