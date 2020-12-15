
"""
El codigo aqui presentado es una muestra del funcionamiento de la biblioteca preBird y esta disenado para
correr desde consola de la siguiente forma:

python3 test1.py /ruta/a/directorio/wavs --num_wavs n --percentage m

donde n es un numero entero 
donde m es un numero decimal entre el 0 y el 1
"""

from prebird import process
from prebird import spec
from prebird import display
from prebird import result
import argparse

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






    specs_names= spec.reader(args.DIR,args.num_wavs)
    print("\nSalida de reader:")
    print(specs_names)
    samples_rates,samples=spec.sampler(specs_names)
    print("\nSalida 1 (muestras usadas para cada audio) de sampler")
    print(samples_rates)
    print("\nSalida 2 (datos de audio) de sampler")
    print(samples)
    frequencies,times,specs=spec.get_spec(samples,samples_rates)
    print("\nSalida 1 (Frecuencias) de get_spec:")
    print(frequencies)
    print("\nSalida 2 (Tiempos) de get_spec:")
    print(times)
    print("\nSalida 3 (Espectrogramas) de get_spec:")
    print(specs)
    specprueba=specs[:]
    specprueba=process.adjustment(specprueba)
    specprueba=process.activity(specprueba,args.percentage,show=False)
    print("\nSalida de activity")
    print(specprueba)
    specprueba=process.adjustment(specprueba)
    print("\nSalida de adjustment")
    print(specprueba)
   
    indicesAve,indicesFondo=process.intervals(specprueba,show=False)
    print("\nSalida 1 (Indices con canto de ave) de intervals")
    print(indicesAve)
    print("\nSalida 2 (Indices con ruido de fondo) de intervals")
    print(indicesFondo)
   
    indicesAve=process.index2samples(indicesAve,samples,specs)
    print("\nSalida de index2samples para canto de ave:")
    print(indicesAve)
    ave=process.bird(indicesAve,samples)
    print("\nSalida de bird para cantos de ave")
    print(ave)
    indicesFondo=process.index2samples(indicesFondo,samples,specs)
    print("\nSalida de index2samples para ruido de fondo:")
    print(indicesFondo)
    fondo=process.bird(indicesFondo,samples)
    print("\nSalida de bird para ruido de fondo")
    print(fondo)
    wavsAve=result.outwavAves(ave,'/home/royfocker/samples/out/bird/')
    wavsFondo=result.outwavFondos(fondo,'/home/royfocker/samples/out/background/')





















if __name__ == '__main__':
    main()