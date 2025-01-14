import os, sys, traceback, re, json;

sys.path.append( os.environ["RAIZ"] );

from engine.chrome_engine import ChromeEngine;

class Deputados():
    def __init__(self):
        self.engine = ChromeEngine();
        self.deputados = [];

    def listar(self):
        try:
            self.deputados = [];
            self.engine.navegate("https://www.camara.leg.br/deputados/quem-sao");
            deputados = self.engine.elements('//*[@id="parametro-nome"]/option');
            for deputado in deputados:
                if deputado.get_attribute("value") == None or deputado.get_attribute("value") == "":
                    continue;
                self.deputados.append({"id" : deputado.get_attribute("value"), "nome" : deputado.get_attribute("textContent")});
            return True;
        except:
            traceback.print_exc();
        return False;
    
    def __carregar_campo_detalhes__(self, elements, campo):
        for li in elements:
            texto = li.get_attribute("textContent").strip();
            partes = texto.split(":");
            if partes[0].strip().lower() == campo.lower():
                buffer = partes[1].strip();
                buffer = re.sub(r'\n+', ' ', buffer);
                buffer = re.sub(r'\s+', ' ', buffer);
                return buffer;
        return "";

    def carregar_detalhes(self, deputado):
        self.engine.navegate("https://www.camara.leg.br/deputados/" + deputado["id"]);
        deputado["apelido"] = self.engine.element_value('//*[@id="nomedeputado"]',  "textContent");
        elementos_li = self.engine.elements('//*[@class="informacoes-deputado"]/li');
        deputado["nome"] = self.__carregar_campo_detalhes__( elementos_li, "Nome Civil"  );
        deputado["partido"] = self.__carregar_campo_detalhes__( elementos_li, "Partido" ).split("-")[0].strip();
        deputado["data_nascimento"] = self.__carregar_campo_detalhes__( elementos_li, "Data de Nascimento"     );
        deputado["naturalidade"] = self.__carregar_campo_detalhes__( elementos_li, "Naturalidade"     );
        deputado["email"] = self.__carregar_campo_detalhes__( elementos_li, "E-mail"     );
        deputado["endereco"] = self.__carregar_campo_detalhes__( elementos_li, "Endereço"     );
        deputado["telefone"] = self.__carregar_campo_detalhes__( elementos_li, "Telefone"     );

        buffer = self.engine.element_value('//*[@class="cargo-periodo__anos"]', "textContent").strip();
        if buffer.find("-") > 0:
            buffer = buffer.split("-");
            deputado["inicio"] = buffer[0].strip();
            deputado["fim"] = buffer[1].strip();
        else:
            deputado["inicio"] = None;
            deputado["fim"] = None;           
        return deputado;

if __name__ == "__main__":
    d = Deputados();
    if d.listar():
        for i in range(len(d.deputados)):
            d.deputados[i] = d.carregar_detalhes( d.deputados[i] );
            print(d.deputados[i]);
        with open("/tmp/deputados.json") as f:
            f.write( json.dumps( d.deputados ) );
        print("fim");




