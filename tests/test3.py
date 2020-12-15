
"""
El codigo aqui presentado es una muestra del funcionamiento de la biblioteca preBird y esta disenado para
correr desde consola de la siguiente forma:

python3 test3.py /ruta/a/directorio/wavs --num_wavs n --percentage m

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
    samples_rates,samples=spec.sampler(specs_names)
    frequencies,times,specs=spec.get_spec(samples,samples_rates)

    specprueba=specs[:]
    specsbw=specs[:]
    specsbw=spec.blackandwhite(specsbw)
    print("\n Salida de blackandwhite")
    print(specsbw)
    display.plotterbw(frequencies,times,specsbw)
    specprueba=process.adjustment(specprueba)

    specprueba=process.activity(specprueba,args.percentage,show=False)
    indicesAve,indicesFondo=process.intervals(specprueba,show=False)

    indicesAve=process.index2samples(indicesAve,samples,specs)
    ave=process.bird(indicesAve,samples)
    
    indicesFondo=process.index2samples(indicesFondo,samples,specs)
    fondo=process.bird(indicesFondo,samples)

    wavsAve=result.outwavAves(ave,'/home/royfocker/samples/out/bird/')
    wavsFondo=result.outwavFondos(fondo,'/home/royfocker/samples/out/background/')





















if __name__ == '__main__':
    main()