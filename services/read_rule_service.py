import csv
import json
import logging
from typing import List

from businness_object.rule import Rule


class ReadRuleService:

    def read_rules_from_jsonl(self, path_to_file) -> List[Rule]:
        """
        Read all the rule from a jsonm file
        1. check if the file exist
        2. read the tule
        :param path_to_file: the path to the file (absolute or relative)
        :type path_to_file: str
        :return: all the rule from the file
        :rtype: list of Rule
        """
        logging.info(f'Read rules form csv file {path_to_file}')
        rules = []
        try:
            logging.info(f'Opening file {path_to_file}')
            with open(path_to_file, mode="r") as rule_file:
                line = rule_file.readline()
                while line:
                    dict = json.loads(line)
                    rules.append(Rule(expression=dict["expression"]
                                      , tag=dict["tag"]))
                    line = rule_file.readline()
        except IOError:
            logging.error(f'No file at {path_to_file}, will return empty rules')

        return rules
