
"""
El codigo aqui presentado es una muestra del funcionamiento de la biblioteca preBird y esta disenado para
correr desde consola de la siguiente forma:

python3 test2.py /ruta/a/directorio/wavs --num_wavs n --percentage m

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

    print("\nComienza muestreo de gráficas de la funcion plotter")
    display.plotter(frequencies,times,specs)

    print("\nComienza muestreo de estadisticas de la funcion stats")
    display.stats(specs)

    specprueba=specs[:]
    specprueba=process.adjustment(specprueba)

    print("\nVisualizador de la función activity")
    specprueba=process.activity(specprueba,args.percentage,show=True)

    print("\nVisualizador de la función intervals")
    indicesAve,indicesFondo=process.intervals(specprueba,show=True)

    indicesAve=process.index2samples(indicesAve,samples,specs)
    ave=process.bird(indicesAve,samples)
    
    indicesFondo=process.index2samples(indicesFondo,samples,specs)
    fondo=process.bird(indicesFondo,samples)

    wavsAve=result.outwavAves(ave,'/home/royfocker/samples/out/bird/')

    print("\nAsi es como se ve la consola cuando reproduce audio mediante la funcion player")
    display.player(wavsAve,1)

    wavsFondo=result.outwavFondos(fondo,'/home/royfocker/samples/out/background/')





















if __name__ == '__main__':
    main()