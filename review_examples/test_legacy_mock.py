from unittest.mock import Mock

# Heredado para revisión; fuera de la suite obligatoria.
def test_repository_failure():
    repository = Mock()
    repository.get_project.return_value = {"status_code": 503}
    result = repository.get_project("unavailable")
    assert result["status_code"] == 503
