import json
import re
import sys

class ConfigSyntaxError(Exception):
    pass

class Translator:
    def __init__(self, json_data):
        stripped_data = self.strip_comments(json_data)
        try:
            self.data = json.loads(stripped_data)
        except json.JSONDecodeError:
            self.data = {}
        self.constants = {}

    def strip_comments(self, json_data):
        json_data = re.sub(r'//.*', '', json_data)
        json_data = re.sub(r'/\*.*?\*/', '', json_data, flags=re.DOTALL)
        json_data = re.sub(r'\s+', ' ', json_data).strip()
        data = json.loads(json_data)
        return json.dumps(data, separators=(',', ':'))

    def validate_key(self, key):
        if not re.match(r'^[a-zA-Z_]+$', key):
            raise ConfigSyntaxError(f"Invalid key name: {key}")

    def process_constants(self, data):
        constants = {}
        for key in list(data.keys()):
            if "const_value->" in key:
                const_name = key.split("const_value->")[1]
                constants[const_name] = data.pop(key)
        self.constants = constants
        return data

    def resolve_constants(self, data):
        def replace_constants(value):
            if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                const_name = value[1:-1]
                if const_name in self.constants:
                    return self.constants[const_name]
                else:
                    raise ConfigSyntaxError(f"Undefined constant: {const_name}")
            elif isinstance(value, dict):
                return {k: replace_constants(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_constants(item) for item in value]
            else:
                return value
        return replace_constants(data)

    def convert_to_custom_config(self, data, indent=0):
        result = []
        indent_str = ' ' * (indent * 4)
        if isinstance(data, dict):
            result.append(f"{indent_str}table(")
            for key, value in data.items():
                formatted_value = self.format_value(value, indent + 1)
                result.append(f"{indent_str}    {key} => {formatted_value},")
            result[-1] = result[-1][:-1]
            result.append(f"{indent_str})")
        elif isinstance(data, list):
            result.append(f"{indent_str}list(")
            for item in data:
                formatted_value = self.format_value(item, indent + 1)
                result.append(f"{indent_str}    {formatted_value},")
            result[-1] = result[-1][:-1]
            result.append(f"{indent_str})")
        else:
            result.append(self.format_value(data, indent))
        return '\n'.join(result)

    def format_value(self, value, level):
        if isinstance(value, dict):
            return self.convert_to_custom_config(value, level)
        elif isinstance(value, list):
            return self.convert_to_custom_config(value, level)
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return '1' if value else '0'
        else:
            return str(value)

def main():
    if len(sys.argv) != 2:
        print("Usage: python json_to_custom.py <output_file>", file=sys.stderr)
        sys.exit(1)

    output_file = sys.argv[1]

    try:
        print("enter JSON data (press ctrl+z to exit):")
        input_json = sys.stdin.read()

        translator = Translator(input_json)

        translator.data = translator.process_constants(translator.data)
        resolved_data = translator.resolve_constants(translator.data)

        result = translator.convert_to_custom_config(resolved_data)

        with open(output_file, 'w') as file:
            file.write(result)
        print(f"Configuration written to {output_file}.")
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}", file=sys.stderr)
    except ConfigSyntaxError as e:
        print(f"Syntax error in configuration: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()