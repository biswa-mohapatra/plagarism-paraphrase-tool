import pytest
from src.plagarism_paraphrase.scrape_google import scrape_google
from src.plagarism_paraphrase.check_plagarism import check_similarity


class Testscrapegoogle:
    good_response = [
        ("HI",dict)
    ]

    @pytest.mark.parametrize("Query,Response",good_response)
    def test_search(self,Query,Response):
        assert type(Query) == str
        assert type(scrape_google(Query).search_result()) == Response

class Testcheckplagarism:
    good_response = [
        ("HI",list)
    ]

    @pytest.mark.parametrize("Query,Response",good_response)
    def test_search(self,Query,Response):
        assert type(Query) == str
        assert type(check_similarity(Query)) == Response