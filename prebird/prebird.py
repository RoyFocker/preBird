"""Biblioteca para el preprocesamiento de audio orientada al canto de aves"""
import numpy as np
import matplotlib.pyplot as plt 
from scipy import signal
from scipy.io import wavfile
from sklearn.preprocessing import normalize
import glob
from skimage import morphology
import scipy.io.wavfile as wavf
from playsound import playsound

class process:
    """
    Clase dirigida a realizar operaciones y procesos lógicos que afectan a los
    espectrogramas
    """
    def adjustment(spectograms):
        """Realiza operaciones morfologicas a los espectrogramas"""
        for x in range(0,len(spectograms)):
            spectograms[x]=morphology.dilation(spectograms[x])
            spectograms[x]=morphology.dilation(spectograms[x])
            spectograms[x]=morphology.erosion(spectograms[x])
        return spectograms

    def activity(specT,percentage=0.6,show=True):
        """Clasifica entre actividad y no actividad en el eje del tiempo"""
        activities=[]
        for x in range(0,len(specT)):
            parameter=np.max(specT[x])*(percentage)
            a=specT[x] 
            a=np.where(a>parameter,1.0,0.0)
            a=np.sum(a,axis=0)
            a=np.where(a>0.99,1.0,0.0)
            if show:
                plt.plot(a)
                plt.show()
            activities.append(a)
        return activities

    def intervals(specs,show=True):
        """Obtiene los intervalos exactos de tiempo en los que hubo actividad 
        y en los que no la hubo"""
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
            if len(ini.tolist())==0 and len(fin.tolist())==0:
                indicesAve.append([(0,len(specs[x]))])
            else:
                if len(ini.tolist())==0:
                    indicesAve.append([(0,fin)])
                if len(fin.tolist())==0:
                    indicesAve.append([(ini,len(specs[x]))])
                else:
                    indicesAve.append(zip(ini.tolist(),fin.tolist()))
        for x in range(0,len(indicesAve)):
            finales,inicios=zip(*indicesAve[x])
            inicios=list(inicios)
            finales=list(finales)
            inicios.insert(0,0)
            finales.append(len(specs[x]))
            indicesFondo.append(zip(inicios,finales))   
        return indicesAve,indicesFondo

    def index2samples(index,samples,specs):
        """Convierte los indices a momentos del muestreo de los archivos wav"""
        convertedindex=[]
        for x in range(0,len(samples)):
            lenindex=len(specs[x])
            lensamples=len(samples[x])
            convertedindex.append([])
            for ini,fin in index[x]:
                ini=int((ini*lensamples)/lenindex)
                fin=int((fin*lensamples)/lenindex)
                convertedindex[-1].append((ini,fin))
        return convertedindex

    def bird(convertedindex,samples):
        """Obtiene una lista con la informacion para escribir wavs"""
        indices=[]
        for x in range(0,len(samples)):
            indices.append([])
            for ini,fin in convertedindex[x]:
                indices[-1].append(samples[x][ini:fin]) 
            if len(indices[-1])==0:
                indices[-1]=[]
            else:
                indices[-1]=np.hstack(indices[-1])
        return indices

class spec:
    """
    Clase dirigida a la obtención de espectrogramas a partir de los
    audios utilizados por el usuario
    """
    def reader(route,lim,start=0):
        """Lee los archivos wav de un directorio"""
        out=[] 
        for wave_file in glob.glob(route+"/*.wav"):
            if start and start==lim: 
                break
            else:
                start+=1
            print("Processing {}...".format(wave_file))
            out.append(wave_file)
        return out

    def sampler(names):
        """Obtiene el muestreo de los archivos wav"""
        out_sr=[]
        out_s=[]
        for name in names:
            sr,s=wavfile.read(name)
            out_sr.append(sr)
            out_s.append(s)
        return out_sr,out_s

    def get_spec(samples,samples_rates):
        """Obtiene espectrogramas de archivos wav"""
        f=[]
        t=[]
        s=[]
        for x in range(0,len(samples)):
            frequency,time,spec=signal.spectrogram(samples[x],samples_rates[x],scaling='spectrum',mode='magnitude',window='hann')
            spec=normalize(spec)
            spec=np.log(spec+1e-10)+10
            f.append(frequency)
            t.append(time)
            s.append(spec)
        return f,t,s

    def blackandwhite(spectrograms):
        """Selecciona pixeles de un espectrograma"""
        bwspecs=[]
        for x in range(0,len(spectrograms)):
            spectrograms[x]=normalize(np.abs(spectrograms[x]))
            X=np.max(spectrograms[x],axis=1)*0.6 
            Y=np.max(spectrograms[x],axis=0)*0.6 
            b2=np.subtract(spectrograms[x],Y)
            b1=np.subtract(spectrograms[x].T,X).T
            b1=np.where(b1>0,1.0,0.0)
            b2=np.where(b2>0,1.0,0.0)
            bw=np.logical_and(b1,b2)
            bwspecs.append(bw)
        return bwspecs

class display:
    """
    Clase orientada a mostrar los resultados y otros datos de interés provenientes de
    las funciones de las otras clases.
    """
    def plotter(frequencies,times,spectrograms,specific=False,i=0):
        """Grafica espectrogramas"""
        if specific==True: 
            plt.pcolormesh(times[i],frequencies[i],spectrograms[i],shading='auto') 
            plt.ylim(0,10000)
            plt.ylabel('Frequency [Hz]') 
            plt.xlabel('Time [s]')
            plt.show()
            return
        for x in range(0,len(spectrograms)):
            plt.pcolormesh(times[x],frequencies[x],spectrograms[x],shading='auto')
            plt.ylim(0,10000)
            plt.ylabel('Frecuencia [Hz]')
            plt.xlabel('Tiempo [s]')
            plt.show()
        return

    def plotterbw(frequencies,times,spectrograms,specific=False,i=0):
        """Grafica espectrogramas de la funcion blackadnwhite"""
        if specific==True: 
            plt.pcolormesh(times[i],frequencies[i],spectrograms[i],cmap='Greys',shading='auto') 
            plt.ylim(0,10000)
            plt.ylabel('Frecuencia [Hz]') 
            plt.xlabel('Tiempo [s]')
            plt.show()
            return
        for x in range(0,len(spectrograms)):
            plt.pcolormesh(times[x],frequencies[x],spectrograms[x],cmap='Greys',shading='auto')
            plt.ylim(0,10000)
            plt.ylabel('Frecuencia [Hz]')
            plt.xlabel('Tiempo [s]')
            plt.show()
        return

    def player(wavs,lim,start=0):
        """Reproduce audios seleccionados"""
        for x in range(0,len(wavs)):
            if start and start==lim: 
                break
            else:
                start+=1
            print("Playing {}...".format(wavs[x]))
            playsound(wavs[x])

    def stats(specs):
        """Muestra estadisticas de una lista de espectrogramas"""
        for x in range(0,len(specs)):
            print("Espectrograma "+str(x)+":")
            print("Media: "+str(specs[x].mean())),
            print("Maximo: "+str(specs[x].max())),
            print("Corte: "+str(specs[x].max()*0.6)),
        return

class result:
    """
    Clase orientada a entregar los resultados finales del procesamiento
    realizado por las otras clases
    """
    def outwavAves(index,route):
        """Escribe wavs con cantos de aves"""
        wavs=[]
        fs=44100
        for x in range(0,len(index)):
            if len(index[x])==0:
                out_f=route+'Ave'+str(x)+'.wav'
                wavs.append(out_f)
                open(route+'Ave'+str(x)+'.wav', "x")
            else:
                out_f=route+'Ave'+str(x)+'.wav'
                wavs.append(out_f)
                wavf.write(out_f,fs,index[x])
        return wavs

    def outwavFondos(index,route):
        """Escribe wavs con ruido de fondo"""
        wavs=[]
        fs=44100
        for x in range(0,len(index)):
            if len(index[x]==0):
                out_f=route+'Fondo'+str(x)+'.wav'
                wavs.append(out_f)
                open(route+'Fondo'+str(x)+'.wav', "x")
            else:
                out_f=route+'Fondo'+str(x)+'.wav'
                wavs.append(out_f)
                wavf.write(out_f,fs,index[x])
        return wavs

def main():
    pass

if __name__ == '__main__':
    main()