from streamlit.testing.v1 import AppTest


def test_demo_opportunity_can_be_analyzed_end_to_end():
    app = AppTest.from_file("app.py", default_timeout=20).run()

    assert not app.exception
    assert app.title[0].value == "SignalForge AI"
    app.button(key="analyze_opportunity").click().run()

    assert not app.exception
    assert app.metric[0].value == "62%"
    assert app.metric[1].value == "32%"
    assert app.metric[2].value == "3"
    assert app.metric[3].value == "2"
    assert any("Meridian Hospitality Group" in markdown.value for markdown in app.markdown)
