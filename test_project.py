from project import load_start, get_job, create_player


def test_load_start():
    start_data = load_start("start.json")
    assert "logo" in start_data
    assert "common" in start_data
    assert "start" in start_data["hp"]
    assert "home" in start_data["hp"]
    assert "start" in start_data["bofh"]
    assert "home" in start_data["bofh"]
    assert "help" in start_data


def test_get_job():
    assert get_job("  HP ") == "hp"
    assert get_job("bofh") == "bofh"
    assert get_job("random") == None


def test_create_player():
    hp = create_player("hp")
    assert hp.job == "hp"
    assert hp.hit_points == 3
    assert hp.max_hit_points == 3
    assert hp.inventory == {}
    assert hp.score == 0

    bofh = create_player("bofh")
    assert bofh.job == "bofh"
    assert bofh.hit_points == 2
    assert bofh.max_hit_points == 2
    assert bofh.inventory == {}
    assert bofh.score == 0

    unemployed = create_player(None)
    assert unemployed.hit_points == 0
    assert unemployed.max_hit_points == 0
    assert unemployed.inventory == {}
    assert unemployed.score == 0
