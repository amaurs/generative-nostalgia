from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

LINK_TEMPLATE = "http://www.morellajimenez.com.do/%s"
LINKS = ["letadoro.htm",
         "letadoro.htm",
         "letacariciame.htm",
         "letacariciame.htm",
         "letalaorilladelmar.html",
         "letalgocontigo.htm",
         "letalgodiferente.htm",
         "letamaryvivir.htm",
         "letamorsinesperanza.htm",
         "letamorconllanto.htm",
         "letamordelacalle.htm",
         "letamorgitano.htm",
         "letamorperdido.html",
         "letamordemivida.html",
         "letamordecobre.htm",
         "letamorosamente.htm",
         "letamorosamente.htm",
         "letamorcitocorazon.htm",
         "letangustia.html",
         "letaquelviejoamor.htm",
         "letarrancamelavida.htm",
         "letarrancamelavida2.htm",
         "letarrancamelavida2.htm",
         "letarrepentida.htm",
         "letaunquemecueste.htm",
         "letbajocero.htm",
         "letbesameotravez.htm",
         "letbesameamor.htm",
         "letbesame.htm",
         "letbuscotrecuerdo.htm",
         "letcataclismo.htm",
         "letcaribesoy.htm",
         "letceloso.htm",
         "letcercadelmar.htm",
         "letcaminemos.htm",
         "letcaminopuente.htm",
         "letcenizas.htm",
         "letciegodamor.htm",
         "letciegodamor.htm",
         "let5centavitos.htm",
         "let5centavitos.htm",
         "letcienanos.htm",
         "letcienanos.htm",
         "letcondicion.htm",
         "letcongoja.htm",
         "letcongoja.htm",
         "letconmicorazon.htm",
         "letcontigolospanchos.htm",
         "letcontigo2.htm",
         "letconaprendi.htm",
         "letcomohanpasado.html",
         "letcomohepodido.htm",
         "letcomofue.htm",
         "letconciertootono.htm",
         "letcorazonhotel.htm",
         "letcorazonloco.htm",
         "letcorazondeacero.htm",
         "letcosasdalma.htm",
         "letcosascomotu.htm",
         "letcosascomotu.htm",
         "letcrei.htm",
         "letcuanvuelva.htm",
         "letcuandonomequieras.htm",
         "letcuandoelamor.htm",
         "letcuandotmquieras.htm",
         "letcuandoestoycontigo.htm",
         "letcuandoestemosviejos.htm",
         "letcuandoestemosviejos.htm",
         "letdecigarroencigarro.htm",
         "letdemujeramujer.htm",
         "letdondestascorazon.htm",
         "letdosalmas.htm",
         "letdosgardenias.htm",
         "letdondequieraqestes.htm",
         "letdileque.htm",
         "letdelito.htm",
         "letdimelo.htm",
         "letegoismo.htm",
         "letel19.htm",
         "letelarbol.htm",
         "letelarbol.htm",
         "letelpayador.htm",
         "Letenorillamar.htm",
         "letencadenados.htm",
         "letesperanzinutil.htm",
         "letesperare.htm",
         "letenunrincon.htm",
         "letenlaoscuridad.htm",
         "letenunbesovida.html",
         "letentretuamor.htm",
         "letenamorado.htm",
         "letenvidia.htm",
         "letesoshombres.htm",
         "letelamoracaba.htm",
         "letelmalquerido.htm",
         "letelmaryelcielo.htm",
         "letescandalo.htm",
         "letescribeme.htm",
         "letespumas.htm",
         "letevocacion.htm",
         "letesperame.htm",
         "letesperame.htm",
         "letesa.htm",
         "letfalsa.htm",
         "letfichasnegras.htm",
         "letflordazalea.htm",
         "letfloresnegras.htm",
         "letfrenesi.htm",
         "lethazunmilagro.htm",
         "lethayqsaberperder.htm",
         "lethesabidoqtamaba.htm",
         "letholasoledad.htm",
         "lethipocrita.htm",
         "lethdunamor.htm",
         "lethojaseca.htm",
         "lethoyesviernes.htm",
         "letincertidumbre.htm",
         "letinolvidable.htm",
         "letjurame.htm",
         "letjuguete.htm",
         "letlabarca.htm",
         "letlagrimasalma.htm",
         "letlagrimasnegras.htm",
         "letaretesdeluna.htm",
         "letlapared.htm",
         "letluzysombras.htm",
         "letlacoparota.htm",
         "letlapuerta.htm",
         "letloquetuvecontigo2.htm",
         "letlagloria.htm",
         "letllantodeluna.html",
         "letllevame.htm",
         "letllevatela.htm",
         "letmadrigal.htm",
         "letmuchcorazon.htm",
         "letmienteme.html",
         "letmujer.htm",
         "letmisnochesinti.htm",
         "letmicorazonada.htm",
         "letmujerdivina.htm",
         "letmilbesos.htm",
         "letmigajas.htm",
         "letmiraquelinda.htm",
         "letmiultimofracaso.htm",
         "letmitodo.htm",
         "letmotivos.htm",
         "letmorirdeamor.htm",
         "letmunequitalinda.htm",
         "letmicarino.htm",
         "letnegrura.htm",
         "letnaufragio.htm",
         "letnosotros.htm",
         "letnostalgia.htm",
         "letnoplatiques.htm",
         "letnomevayasaenganar.htm",
         "letnuestrojuramento.htm",
         "letnocheronda.htm",
         "letnoesvenganza.htm",
         "letnoquieroqtvayas.htm",
         "letolvidame.htm",
         "letojostristes.htm",
         "letorgasmo.htm",
         "letobsesion.htm",
         "letpalabrasmujer.htm",
         "letpalabrascielo.htm",
         "letparaquevolver.htm",
         "letpareceayer.htm",
         "letperfidia.htm",
         "letperfidia.htm",
         "letperfumegardenia.htm",
         "letpeleas.htm",
         "letporquenollorar.htm",
         "letporqahora.htm",
         "letpordoscaminos.htm",
         "letporfin.htm",
         "letpoquitafe.htm",
         "letprisionero.html",
         "letpresentimiento.htm",
         "letpuedendecir.htm",
         "letquiereme.htm",
         "letquequierestudemi.htm",
         "letrondandotuesquina.htm",
         "letregalamenoche.htm",
         "letrayitoluna.htm",
         "letrayitoluna.htm",
         "letreloj.htm",
         "letsabordengano.htm",
         "letsaboranada.htm",
         "letsaborami.htm",
         "letsabrasqtequiero.htm",
         "letsentimiento.htm",
         "letsemeolvidotn.htm",
         "letsenora.htm",
         "letsenorabonita.htm",
         "letseteolvida.htm",
         "letsinegoismo.htm",
         "letsinunamor.htm",
         "letsimecomprendieras.htm",
         "letsitecontara.htm",
         "letsomosdiferentes2.html",
         "letsoyloprohibido.htm",
         "letsolamente1vez.htm",
         "letsonar.htm",
         "lettextrano.htm",
         "lettristezamarina.htm",
         "leteodioytequiero.html",
         "lettiemblas.htm",
         "letumeacostumbraste.htm",
         "letumehacesfalta.htm",
         "lettemeridad.htm",
         "letunocomprendes.htm",
         "letupanuelo.htm",
         "letriunfamos.htm",
         "letupromesadamor.htm",
         "letotal.htm",
         "lettodomegustadeti.htm",
         "let3palabras.htm",
         "leteamaretodalavida.htm",
         "letunacopamas.htm",
         "letunviejoamor.htm",
         "letunsiglodausencia.htm",
         "letunpocomas.htm",
         "letusted.htm",
         "letunalimosna.htm",
         "letunamorparalahistoria.htm",
         "letunamorcalle.htm",
         "letunicamentetu2.html",
         "letunaventuramas.htm",
         "letviajera.htm",
         "letvidaconsentida.htm",
         "letvirgenmediancohe.htm",
         "letvoy.htm",
         "letvuelvemequerer.htm",
         "letviejaluna.htm",
         "leyasonlas12.html",
         "letlinda.htm",
         "letyovivomivida.htm"]
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def main():
    """
    Parses and filters content for the bolero songs.
    """
    file = open("boleros.txt","w") 
    for link in list(set(LINKS)):
        try:
            final_link = LINK_TEMPLATE % link
            raw_html = simple_get(final_link)
            html = BeautifulSoup(raw_html, 'html.parser')
            song = ""
            for p in html.find_all('p', align=True):
                sentence = " ".join(p.text.split())
                if "Página Principal" in sentence or \
                   "Imágenes" in sentence or \
                   "Imagen" in sentence or \
                   "Tube" in sentence:
                    break
                else:
                    if not "Autor" in sentence:
                        song = song + " " + sentence
            file.write(song.strip() + "\n") 
        except Exception as e:
            log_error(e)
    file.close() 

if __name__ == '__main__':
    main()