import streamlit as st
from two_way_designer import design_two_way
st.title("Two-way slab designer (final)")
st.markdown("**Manya Rajib Jain (210004027)**  
**Dr. Akshay Pratap Singh**")
Lx=st.number_input("Lx",4.5)
Ly=st.number_input("Ly",6.3)
D=st.number_input("D (mm)",200)
floor=st.number_input("floor finish",1.5)
live=st.number_input("live",4.0)
fck=st.selectbox("fck",[20,25,30,35,40],index=1)
fy=st.selectbox("fy",[250,415,500],index=1)
cover=st.number_input("cover",20)
bar=st.selectbox("bar dia",[8,10,12,16,20],index=2)
if st.button("Run"):
    res=design_two_way(Lx,Ly,D,floor,live,fck=fck,fy=fy,cover=cover,bar_dia=bar)
    st.write(res)
