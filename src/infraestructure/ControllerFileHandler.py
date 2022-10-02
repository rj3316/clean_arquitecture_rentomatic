from json import load, dump
from os import path
from datetime import datetime

class FileHandler:
    @classmethod
    def read(cls, file):
        return cls._read_json(file)

    @classmethod
    def write(cls, file, data = None):
        if data is not None:            
            cls._write_json(file, data)

    # JSON INTERFACES
    @classmethod
    def _read_json(cls, file = None):
        ret_val = None

        if not file is None:
            try:
                # Comprobamos si el archivo existe
                if path.isfile(file):
                    # Leemos el archivo -> SIEMPRE EN FORMATO JSON
                    with open(file) as jsonfile:
                        ret_val = load(jsonfile)
            except Exception as e:
                if '/' in file: sep = '/'
                else: sep = '\\'

                filename = file.split(sep)[-1]
                print(f"Error reading JSON file {filename}: {e}")

        return ret_val

    @classmethod
    def _write_json(cls, file = None, data = None):
        ret_val = None

        if (not file is None) and (not data is None):
            if not isinstance(data, dict):
                data = {data}
                
            # Prepare data for writing
            data = cls._prepare_write_json_data(data)

            if data is not None:
                with open(file, 'w') as jsonfile:
                    dump(data, jsonfile)
                
                ret_val = True

        return ret_val
    
    @classmethod
    def _prepare_write_json_data(cls, data):
        # Prepare data for writing
        for key in data.keys():
            tmp = data[key]

            isdict = isinstance(tmp, dict)
            islist = isinstance(tmp, list)

            if isdict:
                tmp = cls._prepare_write_json_data(tmp)
            elif islist:
                tmp = list(map(cls._cast_datetime_to_string, tmp))
            else:
                tmp = cls._cast_datetime_to_string(tmp)

            data[key] = tmp
        
        return data

    @staticmethod
    def _cast_datetime_to_string(data):
        if isinstance(data, datetime):
            data = data.strftime("%Y/%m/%d %H:%M:%S")

        return data

    @staticmethod
    def _cast_string_to_datetime(data):
        return datetime.strptime(data, "%Y/%m/%d %H:%M:%S")

