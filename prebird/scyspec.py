#Importaciones
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal
from scipy.io import wavfile
from sklearn.preprocessing import normalize
import glob
import pickle
import statistics
from skimage import morphology
from skimage.morphology import square
import scipy.io.wavfile as wavf
from playsound import playsound
import copy
import argparse

#Lectura de wavs
def reader(route,lim,start=0):
    out=[] 
    for wave_file in glob.glob(route+"/*.wav"):
        if start and start==lim: 
            break
        else:
            start+=1
        print("Processing {}...".format(wave_file))
        out.append(wave_file)
    return out

#Obtener samples
def sampler(names):
    out_sr=[]
    out_s=[]
    for name in names:
        sr,s=wavfile.read(name)
        out_sr.append(sr)
        out_s.append(s)
    return out_sr,out_s

#Obtener espectogramas mediante los samples
def get_spec(samples,samples_rates):
    f=[]
    t=[]
    s=[]
    for x in range(0,len(samples)):
        frequency,time,spec=signal.spectrogram(samples[x],samples_rates[x],scaling='spectrum',mode='magnitude')
        spec=normalize(spec)
        #spec=np.abs(np.log(spec+1e-10))
        spec=np.log(spec+1e-10)+10
        #print(type(spec[0][0]))
        f.append(frequency)
        t.append(time)
        s.append(spec)
    return f,t,s
		
#Muestra graficamente los espectogramas de los wavs
def plotter(frequencies,times,spectrograms,specific=False,i=0):
    if specific==True: 
        plt.pcolormesh(times[i],frequencies[i],spectrograms[i]) 
        plt.ylabel('Frequency [Hz]') 
        plt.xlabel('Time [s]')
        plt.show()
        return
    for x in range(0,len(spectrograms)):
        plt.pcolormesh(times[x],frequencies[x],spectrograms[x])
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.show()
    return

#Seleccionador de pixeles
def blackandwhite(spectrograms):
    bwspecs=[]
    for x in range(0,len(spectrograms)):
        spectrograms[x]=normalize(np.abs(spectrograms[x]))
        X=np.max(spectrograms[x],axis=1)*0.6 
        Y=np.max(spectrograms[x],axis=0)*0.6 
        b2=np.subtract(spectrograms[x],Y)
        b1=np.subtract(spectrograms[x].T,X).T
        b1[b1>0]=1
        b2[b2>0]=1
        b1[b1<0]=0
        b2[b2<0]=0
        bw=np.logical_and(b1,b2)
        bwspecs.append(bw)
    return bwspecs

#Erosion y dilatacion de pixeles seleccionados
def adjustment(spectograms):
    for x in range(0,len(spectograms)):
        spectograms[x]=morphology.dilation(spectograms[x])
        spectograms[x]=morphology.dilation(spectograms[x])
        spectograms[x]=morphology.erosion(spectograms[x])
    return spectograms

#Muestra graficamente los pixeles seleccionados
def plotterbw(frequencies,times,spectrograms,specific=False,i=0):
    if specific==True: 
        plt.pcolormesh(times[i],frequencies[i],spectrograms[i],cmap='Greys') 
        plt.ylabel('Frequency [Hz]') 
        plt.xlabel('Time [s]')
        plt.show()
        return
    for x in range(0,len(spectrograms)):
        plt.pcolormesh(times[x],frequencies[x],spectrograms[x],cmap='Greys')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.show()
    return

#Devuelve una lista donde clasifica entre actividad (1) y no actividad (0)
def activity(specT,percentage=0.6,show=True):
    activities=[]
    #for x in range(0,len(specT)):
     #   for i in range(0, len(specT[x])):
      #      print(specT[x][i])
    for x in range(0,len(specT)):
        parameter=np.max(specT[x])*(percentage)
        a=specT[x]
        a[a>parameter]=1.0
        a[a<parameter]=0.0
        a=np.sum(a,axis=0)
        a[a>0.99]=1.0
        if show:
            plt.plot(a)
            plt.show()
        activities.append(a)
    return activities

#Hace una lista con intervalos de tiempo de actividad y no actividad
def intervals(specs,show=True):
    indicesAve=[]
    indicesFondo=[]
    for x in range(0,len(specs)):
        index=np.diff(specs[x])
        if show:
            plt.plot(index)
            plt.show()
            print(index.shape)
        fin,=np.where(index==-1)
        ini,=np.where(index==1)
        if len(ini.tolist())==0:
            indicesAve.append([(0,fin)])
        if len(fin.tolist())==0:
            indicesAve.append([(ini,len(specs[x]))])
        else:
            indicesAve.append(zip(ini.tolist(),fin.tolist()))
    #print(indicesAve)
    for x in range(0,len(indicesAve)):
        finales,inicios=zip(*indicesAve[x])
        inicios=list(inicios)
        finales=list(finales)
        inicios.insert(0,0)
        finales.append(len(specs[x]))
        indicesFondo.append(zip(inicios,finales))   
    #print(indicesFondo)
    return indicesAve,indicesFondo

#Convierte los indices a muestras del wav
def index2samples(index,samples,specs):
    indices=[]
    for x in range(0,len(samples)):
        lenindex=len(specs[x])
        lensamples=len(samples[x])
        indices.append([])
        for ini,fin in index[x]:
            ini=int((ini*lensamples)/lenindex)
            fin=int((fin*lensamples)/lenindex)
            indices[-1].append((ini,fin))
    return indices

#Usa los indices para cortar los wavs con los segmentos indicados
def bird(convertedindex,samples):
    indices=[]
    for x in range(0,len(samples)):
        indices.append([])
        for ini,fin in convertedindex[x]:
            indices[-1].append(samples[x][ini:fin])
        indices[-1]=np.hstack(indices[-1])
    return indices

#Escribe wavs donde hay actividad
def outwavAves(index):
    wavs=[]
    fs=44100
    for x in range(0,len(index)):
        out_f='out/bird/Ave'+str(x)+'.wav'
        wavs.append(out_f)
        wavf.write(out_f,fs,index[x])
    return wavs

#Escribe wavs donde no hay actividad
def outwavFondos(index):
    wavs=[]
    fs=44100
    for x in range(0,len(index)):
        out_f='out/background/Fondo'+str(x)+'.wav'
        wavs.append(out_f)
        wavf.write(out_f,fs,index[x])
    return wavs

#Reproduce los wavs indicados
def player(wavs,lim,start=0):
    for x in range(0,len(wavs)):
        if start and start==lim: 
            break
        else:
            start+=1
        print("Playing {}...".format(wavs[x]))
        playsound(wavs[x])

#Muestra la media y el maximo de cada espectrograma
def stats(specs):
    for x in range(0,len(specs)):
        print("Espectrograma "+str(x)+":")
        print("Media: "+str(specs[x].mean())),
        print("Maximo: "+str(specs[x].max())),
        print("Corte: "+str(specs[x].max()*0.6)),
    return

#######################################################Pruebas#######################################################


def main():
    parser = argparse.ArgumentParser()

    # Parametros requeridos
    parser.add_argument(
        "DIR",
        default=None,
        type=str,
        help="Directorio con archivos wav a procesar",
    )
    parser.add_argument(
        "--num_wavs",
        default=0,
        type=int,
        help="Numero de wavs a procesar [0] process all",
    )
    parser.add_argument(
        "--percentage",
        default=0.6,
        type=float,
        help="Umbral de corte con respecto a porcentange del maximo",
    )

    args = parser.parse_args()

    specs_names=reader(args.DIR,args.num_wavs)
    samples_rates,samples=sampler(specs_names)
    frequencies,times,specs=get_spec(samples,samples_rates)
    
    statspecs=copy.deepcopy(specs)
    processpecs=copy.deepcopy(specs)
    
    processpecs=activity(processpecs,args.percentage,show=False)
    processpecs=adjustment(processpecs)
   
    indicesAve,indicesFondo=intervals(processpecs,show=False)

    indicesAve=index2samples(indicesAve,samples,specs)
    ave=bird(indicesAve,samples)

    indicesFondo=index2samples(indicesFondo,samples,specs)
    fondo=bird(indicesFondo,samples)

    wavsAve=outwavAves(ave)
    player(wavsAve,1)

    wavsFondo=outwavFondos(fondo)
    player(wavsFondo,1)


    stats(statspecs)

if __name__ == '__main__':
    main()