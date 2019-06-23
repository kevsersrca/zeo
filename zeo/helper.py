import pydgraph
import json
import threading
from TurkishStemmer import *
from .models import ThreadTask
import time


class Helper():

        def __init__(self):
            self.client_stub = pydgraph.DgraphClientStub('134.209.105.213:9080')
            self.client = pydgraph.DgraphClient(self.client_stub)
            self.data = []

        def getUid(self, uid):
            query = """query all($a: string){
                              all(func: uid($a)) {
                                  uid
                                  name@tr
                                  name@en
                                  name@de
                                starring {
                                    performance.actor {
                                      uid
                                      name@en
                                    }
                                    performance.character {
                                      uid
                                      name@en
                                    }
                                  }
                                  genre {
                                    uid
                                    name@en
                                  }
                                  director.film {
                                    uid
                                    name@en
                                  }
                                  initial_release_date
                              }
                            }"""
            try:
                txn = self.client.txn(read_only=True)
                res = txn.query(query,variables={"$a": uid})
                ppl = json.loads(res.json)
                return ppl["all"]
            except:
                return ""

        def stremmer(self, data, task):
            query = """query all($a: string) {
              all(func:anyofterms(name@en, $a)) @filter(has(genre)) {
                name : name@en
              }
            }"""
            stemmer = TurkishStemmer()
            temp = stemmer.stem(data)
            time.sleep(3)
            res = self.client.txn(read_only=True).query(query, variables={"$a": temp})
            ppl = json.loads(res.json)
            task = ThreadTask.objects.get(pk=task)
            task.is_done = True
            if ppl["all"] != []:
                for i in ppl["all"]:
                    self.data.append(i["name"])
            task.task = str(task.task) + str(self.data)
            task.save()
            return task

        def query1(self):
            query = """{
                              all(func: allofterms(name@tr, "Herşey Çok Güzel Olacak")) {
                                  uid
                                  name@tr
                                  name@en
                                  name@de
                                starring {
                                    performance.actor {
                                      uid
                                      name@en
                                    }
                                    performance.character {
                                      uid
                                      name@en
                                    }
                                  }
                                  genre {
                                    uid
                                    name@en
                                  }
                                  director.film {
                                    uid
                                    name@en
                                  }
                                  initial_release_date
                              }
                            }"""
            try:
                txn = self.client.txn(read_only=True)
                res = txn.query(query)
                ppl = json.loads(res.json)
                return [ppl["all"], query]
            except:
                return ["", query]

        def query2(self):
            txn = self.client.txn(read_only=True)
            # Run query.
            query = """{
              var(func:has(director.film)) {
                director.film @groupby(genre) {
                  a as count(uid)
                }
              }

              all(func: uid(a), orderdesc: val(a)) {
                name@en
                total_movies : val(a)
              }
            }"""
            query2 = """
                        {
              dates(func: has(genre)) {
               initial_release_date
              }
            }"""
            res = txn.query(query)
            ppl = json.loads(res.json)
            res2 = self.client.txn(read_only=True).query(query2)
            ppl2 = json.loads(res2.json)
            return [ppl["all"], ppl2["dates"], query]

        def query3(self, name, surname):
            query = '''query all($a: string) {
              var(func: allofterms(name@en, $a)) {
                actor.film {
                  F as performance.film {
                    G as genre
                  }
                }
              }

              all(func: uid(G)) {
                films : ~genre @filter(uid(F)) {
                  film_name : name@en
                  starring{
                     performance.actor @filter(allofterms(name@en, $a))  {
                        name@en
                    }
                  }
                }
              }
            }
            '''
            res = self.client.txn(read_only=True).query(query, variables={"$a": name})
            ppl = json.loads(res.json)
            res2 = self.client.txn(read_only=True).query(query, variables={"$a": surname})
            ppl2 = json.loads(res2.json)
            return [ppl["all"], ppl2["all"], query]

        def query4(self):
            query = """{
              all(func: allofterms(name@en, "Cem Yılmaz")) @filter(has(~director.film) ) {
                name@en
            
                ~director.film {
                uid
                name@en
                starring{
                        performance.actor{
                        name@en
                        }
                    performance.character{
                        name@en
                        }
                  }
                }
              }
            }"""
            res = self.client.txn(read_only=True).query(query)
            ppl = json.loads(res.json)
            return [ppl["all"], query]

        def query5(self, task):
            hitabe = """Ey Türk gençliği Birinci vazifen Türk istiklâlini Türk Cumhuriyetini ilelebet muhafaza ve müdafaa etmektir Mevcudiyetinin ve istikbalinin yegâne temeli budur Bu temel senin en kıymetli hazinendir İstikbalde dahi seni bu hazineden mahrum etmek isteyecek dahilî ve haricî bedhahların olacaktır Bir gün istiklâl ve cumhuriyeti müdafaa mecburiyetine düşersen vazifeye atılmak için içinde bulunacağın vaziyetin imkân ve şeraitini düşünmeyeceksin Bu imkân ve şerait çok nâmüsait bir mahiyette tezahür edebilir İstiklâl ve cumhuriyetine kastedecek düşmanlar bütün dünyada emsali görülmemiş bir galibiyetin mümessili olabilirler Cebren ve hile ile aziz vatanın bütün kaleleri zaptedilmiş bütün tersanelerine girilmiş bütün orduları dağıtılmış ve memleketin her köşesi bilfiil işgal edilmiş olabilir Bütün bu şeraitten daha elîm ve daha vahim olmak üzere memleketin dahilinde iktidara sahip olanlar gaflet ve dalâlet ve hattâ hıyanet içinde bulunabilirler Hatta bu iktidar sahipleri şahsî menfaatlerini müstevlilerin siyasî emelleriyle tevhit edebilirler Millet fakr ü zaruret içinde harap ve bîtap düşmüş olabilir Ey Türk istikbalinin evlâdı İşte bu ahval ve şerait içinde dahi vazifen Türk istiklâl ve cumhuriyetini kurtarmaktır Muhtaç olduğun kudret damarlarındaki asil kanda mevcuttur"""
            temp = hitabe.split()
            for i in temp:
                try:
                    t = threading.Thread(target=self.stremmer, args=[i, task])
                    t.setDaemon(True)
                    t.start()
                except:
                    print("Error: unable to start thread")
            return True

        def query6(self):
            query = """{
              all(func: has(name@en)) {
               Man_films as director.film @filter(regexp(name@en, /[^wo]+man$/i)) {
                  film_name : name@en
                  starring(first:2){
                    performance.actor{
                        name@en
                        actor.film(first:2){
                            performance.film @filter(not uid(Man_films)) {
                          	name@en
                        }
                        }
                    }
                  }
                }
              }
            }
            """
            res = self.client.txn(read_only=True).query(query)
            ppl = json.loads(res.json)
            return [ppl["all"], query]

        def query7(self, date, genre):
            query = """query all($a: string, $b: string) {
              all(func:has(director.film), first:10, offset:1) {
                director.film @filter(lt(initial_release_date, $a))  {
                  initial_release_date
                  name : name@en
                   genre @filter(allofterms(name@en, $b)) {
                 	 	name : name@en
                	}
                }
              }
            }"""
            res = self.client.txn(read_only=True).query(query, variables={"$a": date, "$b": genre})
            ppl = json.loads(res.json)
            return ppl["all"]

        def query8(self, movie, actor, character, genre, date, director):
            query = """query all($a: string, $b: string, $c:string, $d:string, $e:string, $f:string){
                            all(func: anyofterms(name@tr, $a)) {
                                  uid
                                  name@tr
                                  name@en
                                  name@de
                                starring {
                                    performance.actor @filter(anyofterms(name@tr, $b)){
                                      uid
                                      name@en
                                    }
                                    performance.character@filter(anyofterms(name@tr, $c)){
                                      uid
                                      name@en
                                    }
                                  }
                                  genre @filter(anyofterms(name@tr, $d)){
                                    uid
                                    name@en
                                  }
                                  director.film @filter(eq(initial_release_date, $e)) and @filter(anyofterms(name@tr, $f)){
                                    uid
                                    name@en
                                  }
                                  initial_release_date
                              }
                            }"""
            res = self.client.txn(read_only=True).query(query, variables={"$a": movie, "$b": actor, "$c": character, "$d": genre, "$e": date, "$f": director})
            ppl = json.loads(res.json)
            return ppl["all"]
