from maxsurf_integration.maxsurf_connector import MaxsurfConnector


def test_connection_and_hydro_mock():
    c = MaxsurfConnector(visible=False)
    assert c.connect() is True
    assert c.is_connected() is True
    # En macOS se espera mock
    assert getattr(c, '_is_mock', True) is True
    c.set_length(12.0)
    c.set_beam(3.8)
    c.set_draft(1.8)
    hs = c.run_hydrostatics()
    assert isinstance(hs, dict)
    assert 'displacement_t' in hs and hs['displacement_t'] > 0
