from django.test import TestCase
from zeo.helper import *


class TasksTestCase(TestCase):
    def test_get_task_1_values(self):
        response = list([{'uid': '0xf9069', 'name@tr': 'Herşey Çok Güzel Olacak', 'name@en': "Everything's Gonna Be Great", 'name@de': 'Alles wird gut', 'starring': [{'performance.actor': [{'uid': '0xf9072', 'name@en': 'Selim Nasit'}], 'performance.character': [{'uid': '0xf906c', 'name@en': 'Cevat Camli'}]}, {'performance.actor': [{'uid': '0xf906f', 'name@en': 'Ceyda Düvenci'}], 'performance.character': [{'uid': '0xf9071', 'name@en': 'Ayla Camli'}]}, {'performance.actor': [{'uid': '0xf9068', 'name@en': 'Mustafa Uzunyilmaz'}], 'performance.character': [{'uid': '0xf9062', 'name@en': 'Nusret'}]}, {'performance.actor': [{'uid': '0xf906e', 'name@en': 'Mazhar Alanson'}], 'performance.character': [{'uid': '0xf906b', 'name@en': 'Nuri Camli'}]}, {'performance.actor': [{'uid': '0xf9065', 'name@en': 'Cem Yılmaz'}], 'performance.character': [{'uid': '0xf906a', 'name@en': 'Altan Camli'}]}], 'genre': [{'uid': '0xf9063', 'name@en': 'Comedy'}, {'uid': '0xf9064', 'name@en': 'Drama'}], 'director.film': [{'uid': '0xf9073', 'name@en': 'Ömer Vargi'}], 'initial_release_date': '1998-11-27T00:00:00Z'}])
        helper = Helper()
        [data, _] = helper.query1()
        self.assertEqual(response, data)


    def test_get_actors_for_name(self):
        response = list([{'films': [{'film_name': 'Carlos', 'starring': [{'performance.actor': [{'name@en': 'Cem Sultan Ungan'}]}]}]}, {'films': [{'film_name': 'Soul Kitchen', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}]}, {'films': [{'film_name': 'Carlos', 'starring': [{'performance.actor': [{'name@en': 'Cem Sultan Ungan'}]}]}, {'film_name': 'Short Sharp Shock', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}]}, {'films': [{'film_name': 'Carlos', 'starring': [{'performance.actor': [{'name@en': 'Cem Sultan Ungan'}]}]}, {'film_name': 'Short Sharp Shock', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}]}, {'films': [{'film_name': 'Carlos', 'starring': [{'performance.actor': [{'name@en': 'Cem Sultan Ungan'}]}]}, {'film_name': 'Soul Kitchen', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}, {'film_name': 'Short Sharp Shock', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}]}, {'films': [{'film_name': 'Soul Kitchen', 'starring': [{'performance.actor': [{'name@en': 'Cem Akın'}]}]}]}, {'films': [{'film_name': 'Carlos', 'starring': [{'performance.actor': [{'name@en': 'Cem Sultan Ungan'}]}]}]}])
        helper = Helper()
        [data, _, _] = helper.query3("cem", "yilmaz")
        self.assertEqual(response, data)

    def test_get_actors_for_surname(self):
        response = list([{'films': [{'film_name': 'Ghosts… of the Civil Dead', 'starring': [{'performance.actor': [{'name@en': 'Yilmaz Tuhan'}]}]}]}, {'films': [{'film_name': 'Ghosts… of the Civil Dead', 'starring': [{'performance.actor': [{'name@en': 'Yilmaz Tuhan'}]}]}]}, {'films': [{'film_name': 'Ghosts… of the Civil Dead', 'starring': [{'performance.actor': [{'name@en': 'Yilmaz Tuhan'}]}]}]}, {'films': [{'film_name': 'Ghosts… of the Civil Dead', 'starring': [{'performance.actor': [{'name@en': 'Yilmaz Tuhan'}]}]}]}])
        helper = Helper()
        [_, data, _] = helper.query3("cem", "yilmaz")
        self.assertEqual(response, data)

