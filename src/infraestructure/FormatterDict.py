
class FormatterDict:
    @classmethod
    def concatenate_dictionaries(cls, parameters, ret_val = None):
        if not isinstance(ret_val, dict):
            ret_val = dict()

        if isinstance(parameters, dict):
            for key, value in parameters.items():
                if isinstance(value, dict):
                    if not key in ret_val.keys():
                        ret_val[key] = dict()

                    ret_val[key] = cls.concatenate_dictionaries(parameters = value, ret_val = ret_val[key])
                else:
                    try:
                        if key in ret_val.keys() and isinstance(ret_val[key], list):
                            if not isinstance(value, list): value = [value]
                            ret_val[key] += value
                        else:
                            ret_val[key] = value
                    except Exception as e:
                        pass
                
        return ret_val    