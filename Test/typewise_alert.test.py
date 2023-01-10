import unittest
import sys
import os, json
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import src.typewise_alert as typewise_alert 


class TypewiseTest(unittest.TestCase):

  def test_check_and_alert(self):
    root_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
    with open(os.path.join(root_dir, "inc", "test_case.json"), "r") as jsonread:
      json_data = json.load(jsonread)
    
    for dt in json_data["check_and_alert"]:
      self.assertTrue(typewise_alert.check_and_alert(dt["alertTarget"], 
                                                     dt["batteryChar"], 
                                                     dt["temperatureInC"] == dt["Result"]))



  # def test_infers_breach_as_per_limits(self):
  #   self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')


if __name__ == '__main__':
  unittest.main()
