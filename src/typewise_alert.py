import os
import json
import subprocess
import logging
import sys

class TypeWise_Alert:
  def __init__(self):
    self.cooling_stage_json_path = os.path.join("inc","cooling_stage.json")
    self.test_case_json_path = os.path.join("inc","test_case.json")
    self.alertTarget_type = ["TO_CONTROLLER","TO_EMAIL"]
    self.coolingType = ["PASSIVE_COOLING","HI_ACTIVE_COOLING","MED_ACTIVE_COOLING"]

  # Pure Function Inside Class
  def get_root_dir(self):
    root_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
    return root_dir

  def read_json_data(self, json_path):
    data = {}
    if not os.path.exists(json_path):
      logging.error("{} not present".format(json_path))
    else:
      with open(json_path, "r") as jsonread:
        data = json.load(jsonread)
    return data
  
  def character_check(self, check_list, check_val):
    if check_val in check_list:
      logging.info("{} parameter is acceptable".format(check_val))
    else:
      logging.error("{} parameter is not acceptable".format(check_val))
      sys.exit(1)

def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'


def classify_temperature_breach(temperatureInC, limit_data):
  return infer_breach(temperatureInC, limit_data['lowerLimit'], limit_data['upperLimit'])

def batteryChar_cooling_dict(batteryChar, data_list):
  limit_dict = {}
  for data_dict in data_list:
    if (list(data_dict.keys())[0] == batteryChar):
      limit_dict = data_dict[batteryChar]
  return limit_dict

def send_to_controller(breachType):
  header = 0xfeed
  print(f'{header}, {breachType}')

def send_to_email(breachType):
  recepient = "a.b@c.com"
  if breachType == 'TOO_LOW':
    print(f'To: {recepient}')
    print('Hi, the temperature is too low')
  elif breachType == 'TOO_HIGH':
    print(f'To: {recepient}')
    print('Hi, the temperature is too high')

def alert_target_selection(breachType, alertTarget):
  if alertTarget == 'TO_CONTROLLER':
    send_to_controller(breachType)
  elif alertTarget == 'TO_EMAIL':
    send_to_email(breachType)

def check_and_alert(alertTarget, batteryChar, temperatureInC):
  alert_obj = TypeWise_Alert()

  # Getting JSON data
  cooling_stage_path = os.path.join(alert_obj.get_root_dir(), alert_obj.cooling_stage_json_path)
  cooling_stage_json_data = alert_obj.read_json_data(cooling_stage_path)

  # Checking If batteryChar is exceptable
  alert_obj.character_check(alert_obj.coolingType, batteryChar)
  limit_json_data = batteryChar_cooling_dict(batteryChar, cooling_stage_json_data["Cooling_Stage"])
  breachType = classify_temperature_breach(temperatureInC, limit_json_data)

  # Checking If alertTarget is exceptable
  alert_obj.character_check(alert_obj.alertTarget_type, alertTarget)
  alert_target_selection(breachType, alertTarget)
  
  return breachType