import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def mulai_1() :
	# Grafik 1
	plh = st.selectbox("Pilih negara",u_negara)
	
	pp, ps = st.columns(2)

	bol = data_mentah.loc[plh]
	data = bol.drop(['kode_negara','tahun'], axis = 1).set_index(bol['tahun'])
	
	fig = px.line(data)
	fig.update_layout(showlegend = False)

	pp.write("Data Produksi Negara " + plh)
	pp.write(data)
	ps.write(fig)

	# Grafik 2
	tahun_s, pos_s = st.columns(2)

	tahun = tahun_s.number_input("Tahun", min_value = data_mentah['tahun'].min(), max_value = data_mentah['tahun'].max(), value = data_mentah['tahun'].min())
	pos = pos_s.number_input("Peringkat", min_value = 5, max_value = 15, value = 5, key = 0)


	data_1 = data_mentah[data_mentah['tahun'] == tahun].drop(['kode_negara','tahun'],axis = 1).sort_values(by = 'produksi', ascending = False)
	fig2 = px.bar(data_1.iloc[:pos], y = 'produksi', orientation = "v")
	fig2.update_layout(showlegend = False)

	st.write(data_1.iloc[:pos])
	st.write(fig2)

	# Grafik 3

	st.write("Data Produksi Kumulatif")
	ppos = st.number_input("Peringkat", min_value = 5, max_value = 15, value = 5, key = 1)
	data_2 = kml.sort_values (by = 'kumulatif', ascending = False)
	data_2.index.names = ["Negara"]
	fig3 = px.bar(data_2.iloc[:ppos], y = 'kumulatif')
	fig3.update_layout(showlegend = False)

	st.write(data_2.iloc[:ppos])
	st.write(fig3)


	#Informasi Umum

	thn = st.number_input("Tahun", min_value = data_mentah['tahun'].min(), max_value = data_mentah['tahun'].max(), value = data_mentah['tahun'].min(), key = 2)
	
	dn = data_mentah.copy()[data_mentah['tahun'] == thn].drop(['tahun'],axis = 1)
	dn['region'] = [data_kode[data_kode['name'] == i].region.item() for i in dn.index]
	dn['sub_region'] = [data_kode[data_kode['name'] == i]['sub-region'].item() for i in dn.index]
	dn['produksi_kumulatif'] = [kml.loc[i].item() for i in dn.index]
	
	dn = dn[['kode_negara','region','sub_region','produksi','produksi_kumulatif']].sort_values(by = 'produksi', ascending = False)
	zv = dn[dn['produksi'] == 0]
	
	dn.drop(dn[dn['produksi'] == 0].index,inplace = True)
	mm = dn[(dn['produksi'] == dn['produksi'].max()) | (dn['produksi'] == dn['produksi'].min())]
	st.write("Produksi Maksimum dan Minimum pada Tahun " + str(thn),mm)
	st.write("Tidak Produksi",zv)

def info_data() :
	st.write ("Web App ini dibuat oleh Kamila Rohmah Lusiana")
	


data_mentah = pd.read_csv('produksi_minyak_mentah.csv')
data_kode = pd.read_json('kode_negara_lengkap.json')

print(data_mentah.head())
print(data_kode.head())
print('\nBATAS\n\n\n')

#Menerjemahkan kode negara
negara = list()
anonim = list()
for i in list(data_mentah['kode_negara']) :
	if i in list(data_kode['alpha-3']) : 
		negara+=[data_kode[data_kode['alpha-3'] == i]['name'].item()]
	else : anonim += [i]

#print(negara)

#Ubah jadi numpy array
negara = np.asarray(negara)
anonim = np.asarray(anonim)

#Unik
u_negara = np.unique(negara)


#Menghapus negara anonim
for i in np.unique(anonim) : data_mentah.drop(data_mentah[data_mentah['kode_negara'] == i].index,inplace = True)

#Merubah index
data_mentah.set_index(negara, inplace = True)

#Data Kumulatif
kumulatif = [data_mentah.loc[i]['produksi'].sum() for i in u_negara]
kml = pd.DataFrame (kumulatif, columns=['kumulatif']).set_index(u_negara)
kml.index.names = ['negara']


st.write("### Selamat Datang di Laman Data Produksi Minyak Mentah Dunia")
st.write("oleh Kamila_ 12220032")
cek = st.selectbox("Mode", ['Menu', 'Tentang'])

if cek == "Menu" : mulai_1()
else : info_data