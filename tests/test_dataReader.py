import builtins
from utils.encounter import Encounter
import utils.dataReader
from collections.abc import Iterable
import csv
from unittest.mock import mock_open, patch
import pytest
from testdatagenerator import random_data_gen

class mock_textFileObject:
    def __next__(*args, **kwargs):
        return 'test'
    def __iter__(self):
        return self

class mock_nontextFileObject:
    def __next__():
        return 2
    def __iter__(self):
        return self

class Test_dataRead_Unit:
    
    def test_dataRead(self, monkeypatch):
        with patch("builtins.open", mock_open(read_data='text,text2,text3,text4,text5,text6,text7')):
            assert isinstance(utils.dataReader.dataRead(mock_textFileObject), Iterable)

    def test_dataRead_fileNotExist(self):
        with pytest.raises(FileNotFoundError):
            assert isinstance(utils.dataReader.dataRead('test.file'), Iterable)

    def test_dataRead_binaryFile(self):
        with pytest.raises(csv.Error):
            with patch("builtins.open", mock_open(read_data=b'text')):
                assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject), Iterable)
    
    def test_dataRead_wrongColumns(self):
        with patch("builtins.open", mock_open(read_data='text,text2,text3')):
            with pytest.raises(IndexError):
                assert isinstance(utils.dataReader.dataRead(mock_nontextFileObject), Iterable)

class Test_dataPrint_Unit:
  
    test_data = [['x','y','z','a','b','d']]

    def test_dataPrint(self):
        assert utils.dataReader.dataPrint(self.test_data) == None
    
    def test_dataPrint_Error(self, monkeypatch):
        def mock_exception():
            raise RuntimeError
        with pytest.raises(Exception):
            monkeypatch.setattr(builtins, 'print', mock_exception)
            assert utils.dataReader.dataPrint(self.test_data) == None

class Test_encounterSplit_Unit:
    
    test_validData = [['7/13/2021 18:07', 'AddLoot', '', 'Byakko Totem', 0, 1],['7/13/2021 18:07', 'GreedLoot', 'Your Character', 'Byakko Totem', 0, 1],['7/13/2021 18:07', 'ObtainLoot', 'Your Character', 'Byakko Totem', 0, 1]]
    test_noEncounter = [['7/13/2021 18:07', 'GreedLoot', 'Your Character', 'Byakko Totem', 0, 1]]
    test_partialEncounter = [['7/13/2021 18:07', 'AddLoot', '', 'Byakko Totem', 0, 1],['7/13/2021 18:07', 'AddLoot', '', 'Byakko Axe', 0, 1]]
    test_randomizedData = random_data_gen(8,3)

    def test_encounterSplitter(self):
        result = utils.dataReader.encounterSplitter(self.test_validData, "Akiva Cookiepouch")
        assert len(result) == 1
        assert isinstance(result[0],Encounter)
    
    def test_encounterSplitter_noEncountersFound(self):
        assert utils.dataReader.encounterSplitter(self.test_noEncounter, "Akiva Cookiepouch") == []
    
    def test_encounterSplitter_partialEncounter(self):
        assert utils.dataReader.encounterSplitter(self.test_noEncounter, "Akiva Cookiepouch") == []
    
    def test_encounterSplitter_randomized(self):
        result = utils.dataReader.encounterSplitter(self.test_randomizedData, "Akiva Cookiepouch")
        assert len(result) == 1
        assert isinstance(result[0], Encounter)

class Test_textParser_Unit:
    testfile = "tests/test_data/testChatLog.txt"

    expected_output = [
        ['0:0:0', 'ObtainLoot', 'Karou Cookiepouch', 'Allagan tomestones of poetics', '0', '12'],
        ['0:0:0', 'AddLoot', '', 'the Axe of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Ares Asterlight', 'the Axe of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Luwu Xp', 'the Axe of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Karou Cookiepouch', 'the Axe of Crags', '0', '1'],
        ['0:0:0', 'GreedLoot', 'Karou Cookiepouch', 'the Axe of Crags', '33', '1'],
        ['0:0:0', 'GreedLoot', 'Ares Asterlight', 'the Axe of Crags', '25', '1'],
        ['0:0:0', 'GreedLoot', 'Luwu Xp', 'the Axe of Crags', '78', '1'],
        ['0:0:0', 'ObtainLoot', 'Luwu Xp', 'the Axe of Crags', '0', '1'],
        ['0:0:0', 'AddLoot', '', 'Culverin of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Ares Asterlight', 'Culverin of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Luwu Xp', 'Culverin of Crags', '0', '1'],
        ['0:0:0', 'CastLoot', 'Karou Cookiepouch', 'Culverin of Crags', '0', '1'],
        ['0:0:0', 'NeedLoot', 'Luwu Xp', 'Culverin of Crags', '43', '1'],
        ['0:0:0', 'ObtainLoot', 'Luwu Xp', 'Culverin of Crags', '0', '1'],
        ['0:0:0', 'AddLoot', '', 'Dark Divinity brok', '0', '1'],
        ['0:0:0', 'CastLoot', 'Karou Cookiepouch', 'Dark Divinity brok', '0', '1'],
        ['0:0:0', 'CastLoot', 'Akiva Cookiepouch', 'Dark Divinity brok', '0', '1'],
        ['0:0:0', 'GreedLoot', 'Karou Cookiepouch', 'Dark Divinity brok', '49', '1'],
        ['0:0:0', 'ObtainLoot', 'Karou Cookiepouch', 'Dark Divinity brok', '0', '1']
    ]

    def test_textParser(self):
        assert utils.dataReader.textParser(self.testfile, "Karou Cookiepouch") == self.expected_output
