import re
import constants
import helpers


class Pea():
    def __init__(self, filename: str, save_comments: bool = False):
        self.filename = filename
        self.file_content = []
        self.save_comments = save_comments
        self.existing_groups = []

        self.memory = {
            "variables": [], # Should be like: [{"name": "example", "type": "type", "value": "value"}]
            "groups": [], # Should be like: [{"name": "example", "variables": [index1, index2]}]
            "comments": [] # Should be like: [{"comment": "example", "line": 1}]
        }

        self.__prepare__()
        

    # Preparation for parsing
    def __prepare__(self):
        # Read file
        file_content = open(self.filename, "r").readlines()
        
        line_num = 0
        for line in file_content:
            line_num += 1

            line = helpers.remove_newlines(line)

            # Preparing line for future parsing
            parsed_line = {}

            # Check if the line is empty or starts with a comment
            if line == "":
                continue
            
            # Line checking
            if line.startswith(constants.COMMENT):
                if self.save_comments:
                    parsed_line["type"] = "comment"
                    parsed_line["name"] = ""
                    parsed_line["value"] = helpers.remove_prefix(line, constants.COMMENT)
                else:
                    continue
            elif line.startswith(constants.GROUP_CHAR): # If starts with group
                parsed_line["type"] = "group"
                parsed_line["name"] = helpers.remove_begin_end(line.replace(constants.GROUP_CHAR, ""), " ")
            else: # If doesn't start with group, it's certainly a variable.
                split_line = line.split(constants.VARIABLE_ASSIGN)
                parsed_line["type"] = "variable"
                parsed_line["name"] = helpers.remove_undesired_chars(split_line[0])
                parsed_line["value"] = helpers.remove_prefix(split_line[1], " ")

            # remove comment on non-commennts
            if parsed_line["type"] != "comment" and "value" in parsed_line.keys():
                parsed_line["value"] = self._remove_comment(parsed_line["value"])

            # Add parsed line
            parsed_line["line_num"] = line_num
            self.file_content.append(parsed_line)
    

    def _remove_comment(self, text: str, comment_char: str = constants.COMMENT) -> str:
        return helpers.remove_suffix(text.split(comment_char)[0], " ")


    def _parse_var(self, value: str) -> dict:
        return_dict = {}

        # Check if value is list
        if helpers.is_encapsuled_with(constants.LIST_IND, value):
            return_dict["type"] = "list"
            return_dict["value"] = []

            value = helpers.remove_begin_end(value, constants.LIST_IND)
            value_split = value.split(constants.LIST_SEP)

            for item in value_split:
                item = helpers.remove_suffix(item, " ")
                parsed_item = self._parse_var(item)
                return_dict["value"].append(parsed_item["value"])

            return return_dict

        if helpers.is_match(value, constants.NUMBER_REGEX):
            return_dict["type"] = "number"
            return_dict["value"] = float(value)
        else:
            return_dict["type"] = "string"
            return_dict["value"] = value

        return return_dict


    # Parsing
    def parse(self):
        current_group = ""
        for line in self.file_content:
            print(line)
            line_num = line["line_num"]
            name = line["name"]
            tp = line["type"] 
            # Add items to memory

            if tp == "group":
                # Check if group name is valid
                if not helpers.is_match(name, constants.NAMING_REGEX):
                    raise Exception(helpers.parsing_error("Invalid group name", line_num))
                
                current_group = name

                if current_group not in self.existing_groups:
                    self.existing_groups.append(current_group)
                    self.memory["groups"].append({"name": current_group, "variables": []})
                else:
                    raise Exception(helpers.parsing_error("Group already exists", line_num))

            # Case variable
            if tp == "variable":
                if not helpers.is_match(name, constants.NAMING_REGEX):
                    raise Exception(helpers.parsing_error("Invalid variable name", line_num))
                
                value = line["value"] # type: ignore

                value_parsed = self._parse_var(value)
                value = value_parsed["value"]
                value_type = value_parsed["type"]

                self.memory["variables"].append({"name": name, "type": value_type, "value": value})
                self.memory["groups"][-1]["variables"].append(len(self.memory["variables"]) - 1) # -1 is the current as there cannot be group redefinition


            print(self.memory)
