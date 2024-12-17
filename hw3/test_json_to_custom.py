import json
import pytest
from io import StringIO
from json_to_custom import Translator, ConfigSyntaxError, main

test_cases = [
    ('{"key": "value"}', "table(\n    key => 'value'\n)"),
    ('{"key": true}', "table(\n    key => 1\n)"),
    ('{"key": false}', "table(\n    key => 0\n)")
]

def test_strip_comments():
    translator = Translator('{"key": "value"}')
    input_json = """
    {
        "key": "value", // This is a comment
        "another_key": "another_value" /* Another comment */
    }
    """
    expected = '{"key":"value","another_key":"another_value"}'
    assert translator.strip_comments(input_json) == expected

def test_process_constants():
    translator = Translator('{"const_value->CONST": "value", "key": "[CONST]"}')
    data = {"const_value->CONST": "value", "key": "[CONST]"}
    processed_data = translator.process_constants(data)
    assert processed_data == {"key": "[CONST]"}
    assert translator.constants == {"CONST": "value"}

def test_resolve_constants():
    translator = Translator('{"key": "[CONST]"}')
    translator.constants = {"CONST": "value"}
    data = {"key": "[CONST]"}
    resolved_data = translator.resolve_constants(data)
    assert resolved_data == {"key": "value"}

@pytest.mark.parametrize("input_json, expected_output", test_cases)
def test_convert_to_custom_config(input_json, expected_output):
    translator = Translator(input_json)
    translator.data = translator.process_constants(translator.data)  # Убедимся, что константы обработаны
    result = translator.convert_to_custom_config(translator.data)
    assert result == expected_output

def test_validate_key():
    translator = Translator('{"invalid key": "value"}')
    with pytest.raises(ConfigSyntaxError, match="Invalid key name"):
        translator.validate_key("invalid key")

def test_resolve_constants_undefined():
    translator = Translator('{"key": "[UNDEFINED]"}')
    translator.constants = {}
    data = {"key": "[UNDEFINED]"}
    with pytest.raises(ConfigSyntaxError, match="Undefined constant"):
        translator.resolve_constants(data)

def test_json_syntax_error():
    input_json = "invalid json"
    with pytest.raises(json.JSONDecodeError):
        Translator(input_json)

def test_main_function(monkeypatch, capsys):
    output_file = "output.txt"
    input_json = '{"key": "value"}'
    monkeypatch.setattr('sys.stdin', StringIO(input_json))
    monkeypatch.setattr('sys.argv', ['json_to_custom.py', output_file])
    main()
    with open(output_file, 'r') as file:
        content = file.read()
    assert content == "table(\n    key => 'value'\n)"
    captured = capsys.readouterr()
    # Игнорируем сообщение "Enter JSON data (press Ctrl+D to end input):"
    assert "Configuration written to output.txt.\n" in captured.out