from hydralogc.deploy import deploy_to_fpaa

def test_deploy():
    result = deploy_to_fpaa("dummy.cfg")
    assert "Deployed dummy.cfg" in result