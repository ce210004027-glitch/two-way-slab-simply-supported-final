import math
from utils.is_tables import interp_alpha, interp_pt, area_of_bar, choose_practical_spacing, interp_K, XU_OVER_D
def design_two_way(Lx,Ly,D,floor_finish,live,fck=25,fy=415,cover=20,bar_dia=12):
    if Ly<Lx: Lx,Ly=Ly,Lx
    if (Ly/Lx)>=2.0: return {"error":"ly/lx >=2.0"}
    unit_wt=25.0
    dead_self=unit_wt*(D/1000.0); dead_total=dead_self+floor_finish
    w=1.5*(dead_total+live)
    clear_cover = max(5.0, cover-5.0) if bar_dia<=12 else cover
    d=D-clear_cover-bar_dia/2.0
    if d<=0: d=max(D-20,1.0)
    lx_eff=Lx + d/1000.0; ly_eff=Ly + d/1000.0
    ax,ay=interp_alpha(ly_eff/lx_eff)
    Mx=ax*w*(lx_eff**2); My=ay*w*(lx_eff**2)
    d_req=math.sqrt(max(max(Mx,My)*1e6/(0.138*1000.0*fck),0.0))
    if d_req>d:
        d=d_req
        lx_eff=Lx + d/1000.0; ly_eff=Ly + d/1000.0
        ax,ay=interp_alpha(ly_eff/lx_eff)
        Mx=ax*w*(lx_eff**2); My=ay*w*(lx_eff**2)
    As_x = (Mx*1e6)/(0.87*fy*0.9*d)
    As_y = (My*1e6)/(0.87*fy*0.9*d)
    As_min = 0.12/100.0*1000.0*d
    As_x=max(As_x,As_min); As_y=max(As_y,As_min)
    def pick(As_req):
        area=area_of_bar(bar_dia)
        if area<=0: return None
        bars_per_m=As_req/area
        if bars_per_m<=0: return None
        S_calc=1000.0/bars_per_m
        S_prac,reason=choose_practical_spacing(S_calc,15.0)
        if S_prac is None: return None
        S_prac=min(S_prac,int(min(3.0*D,300.0)))
        n_bars=int(math.floor(1000.0/S_prac)) if S_prac>0 else 0
        As_prov=n_bars*area if n_bars>0 else 0.0
        return {"dia":bar_dia,"spacing_mm":S_prac,"n_bars":n_bars,"As_provided_mm2":As_prov,"reason":reason}
    main_x=pick(As_x); main_y=pick(As_y)
    dia_issues=[]
    if main_x and main_x["dia"]>D/8.0: dia_issues.append("Main X dia > D/8 (26.5.2.2)")
    if main_y and main_y["dia"]>D/8.0: dia_issues.append("Main Y dia > D/8 (26.5.2.2)")
    As_prov_x = main_x["As_provided_mm2"] if main_x else As_x
    shear_Vu_x = w*lx_eff/2.0; shear_Vu_y = w*ly_eff/2.0
    # use interp_pt roughly for service/pt checks
    # deflection
    deflection_ok=True
    return {"Lx":Lx,"Ly":Ly,"d_used_mm":d,"w":w,"Mx":Mx,"My":My,"As_x":As_x,"As_y":As_y,"main_x":main_x,"main_y":main_y,"dia_issues":dia_issues}
